import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore_v1
import time
import json
import threading
import json
import copy
import os,shutil
import urllib
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCNogZeG46KnY95_0QL1oiBQDUSv0hPNcs",
    "authDomain": "facelet-40087.firebaseapp.com",
    "databaseURL": "https://facelet-40087-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "facelet-40087",
    "storageBucket": "facelet-40087.appspot.com",
    "messagingSenderId": "151362094829",
    "appId": "1:151362094829:web:627980cb93250b70716ee4",
    "measurementId": "G-XKW0ESME6S"
  }

firebase=pyrebase.initialize_app(firebaseConfig)

#define storage
storage=firebase.storage()

pacientesJSON=json.loads('{}')
newPacienteString=''
creacion= False

def on_snapshot_pacientes(collection_snapshot, changes, read_time):
    global pacientesJSON,newPacienteString,creacion,storage
    for ch in changes:
        newPacienteString=''
        print(ch.document.id)
        email=ch.document.id
        try:
            #existe paciente?
            print(pacientesJSON[email])
            creacion=False
        except:
            print('no existe paciente= '+email)
            creacion=True
            #añadir a json
            newPacienteString=newPacienteString+'{\"'+email+'\":'
            print(newPacienteString)
            #CREAR DIRECTORIO DEL PACIENTE
            try:
                os.mkdir(email)
                os.mkdir(email+'/Contactos')
            except OSError:
                print ("Creation of the directory %s failed" % email)
            else:
                print ("Successfully created the directory %s " % email)
        try:
            contacts=str(ch.document.to_dict()).split(',')
            print(ch.document.to_dict())
            i=0
            for contact in contacts:
                print(contact.split('\'')[1])
                contactoID=contact.split('\'')[1]
                if i==0:
                    try:
                        #existe el contacto?
                        print(pacientesJSON[email][contactoID])
                        pacientesJSON[email][contactoID]="true"
                        newPacienteString=newPacienteString+'{\"'+contactoID+'\":"true"'
                    except:
                        print('no existe contacto= '+contactoID)
                        #AÑADIR A JSON
                        newPacienteString=newPacienteString+'{\"'+contactoID+'\":"true"'
                        #CREAR DIRECTORIO DE UN CONTACTO
                        try:
                            os.mkdir(email+'/Contactos/'+contactoID)
                        except OSError:
                            print ("Creation of the directory %s failed" % email+'/Contactos/'+contactoID)
                        else:
                            print ("Successfully created the directory %s " % email+'/Contactos/'+contactoID)
                        #PARA TODAS LAS FOTOS
                        try:
                            storage.child(email+'/Contactos/'+contactoID+'/feliz.jpg').download("./"+email+'/Contactos/'+contactoID+"/feliz.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/feliz2.jpg').download("./"+email+'/Contactos/'+contactoID+"/feliz2.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/triste.jpg').download("./"+email+'/Contactos/'+contactoID+"/triste.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/serio.jpg').download("./"+email+'/Contactos/'+contactoID+"/serio.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/serio2.jpg').download("./"+email+'/Contactos/'+contactoID+"/serio2.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/sorpresa.jpg').download("./"+email+'/Contactos/'+contactoID+"/sorpresa.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/enfado.jpg').download("./"+email+'/Contactos/'+contactoID+"/enfado.jpg")
                        except:
                            print('no hay foto')
                    i=i+1
                else:
                    try:
                        #existe el contacto?
                        print(pacientesJSON[email][contactoID])
                        pacientesJSON[email][contactoID]="true"
                        newPacienteString=newPacienteString+',\"'+contactoID+'\":"true"'
                    except:
                        print('no existe contacto= '+contactoID)
                        #AÑADIR A JSON
                        newPacienteString=newPacienteString+',\"'+contactoID+'\":"true"'
                        print(newPacienteString)
                        #CREAR DIRECTORIO DE UN CONTACTO
                        try:
                            os.mkdir(email+'/Contactos/'+contactoID)
                        except OSError:
                            print ("Creation of the directory %s failed" % email+'/Contactos/'+contactoID)
                        else:
                            print ("Successfully created the directory %s " % email+'/Contactos/'+contactoID)
                        #PARA TODAS LAS FOTOS
                        try:
                            storage.child(email+'/Contactos/'+contactoID+'/feliz.jpg').download("./"+email+'/Contactos/'+contactoID+"/feliz.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/feliz2.jpg').download("./"+email+'/Contactos/'+contactoID+"/feliz2.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/triste.jpg').download("./"+email+'/Contactos/'+contactoID+"/triste.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/serio.jpg').download("./"+email+'/Contactos/'+contactoID+"/serio.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/serio2.jpg').download("./"+email+'/Contactos/'+contactoID+"/serio2.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/sorpresa.jpg').download("./"+email+'/Contactos/'+contactoID+"/sorpresa.jpg")
                            storage.child(email+'/Contactos/'+contactoID+'/enfado.jpg').download("./"+email+'/Contactos/'+contactoID+"/enfado.jpg")
                        except:
                            print('no hay foto')
            if not creacion:
                for contactoSearchFalse in pacientesJSON[email].keys():
                    print(contactoSearchFalse)
                    if pacientesJSON[email][contactoSearchFalse]=="false":
                        #se elimino de Storage
                        #ELIMINAR CARPETA
                        try:
                            for filename in os.listdir(email+'/Contactos/'+contactoSearchFalse):
                                print(filename)
                                file_path = os.path.join(email+'/Contactos/'+contactoSearchFalse, filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                            os.rmdir(email+'/Contactos/'+contactoSearchFalse)
                        except OSError:
                            print ("Deletion of the directory %s failed" % email+'/Contactos/'+contactoSearchFalse)
                        else:
                            print ("Successfully deleted the directory %s" % email+'/Contactos/'+contactoSearchFalse)

            #end for de contactos
            if newPacienteString!='':
                if email in newPacienteString:
                    newPacienteString=newPacienteString+'}}'
                    print(newPacienteString)
                    add=json.loads(newPacienteString)
                    pacientesJSON.update(add)
                    print(json.dumps(pacientesJSON))
                else:
                    newPacienteString=newPacienteString+'}'
                    add=json.loads(newPacienteString)
                    pacientesJSON[email]=add
                    print(json.dumps(pacientesJSON))
        except:
            print(email+'no tiene contactos')
            newPacienteString=newPacienteString+'{}}'
            print(newPacienteString)
            add=json.loads(newPacienteString)
            pacientesJSON.update(add)
            print(json.dumps(pacientesJSON))

    #PONER A FALSE DE NUEVO
    for pacienteSearchFalse in pacientesJSON.keys():
        print(pacienteSearchFalse)
        for contactoSearchFalse in pacientesJSON[pacienteSearchFalse].keys():
            print(contactoSearchFalse)
            pacientesJSON[pacienteSearchFalse][contactoSearchFalse]="false"

    print(json.dumps(pacientesJSON))

# def hilo():
#     global pacientes_ref
#     pacientes_watch = pacientes_ref.on_snapshot(on_snapshot_pacientes)

#     while True:
#         time.sleep(1)
#         print('procesando....')

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

pacientes_ref = db.collection(u'storage')
pacientes_watch = pacientes_ref.on_snapshot(on_snapshot_pacientes)

while True:
    time.sleep(2)
    print('procesando....')
# hiloWatch = threading.Thread(target=hilo)
# hiloWatch.setDaemon(True)
# hiloWatch.start()

# while True:
#     time.sleep(5)
#     print('hilo principal...')

# Terminate watch --> pacientes_watch.unsubscribe()