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
email="aurorapazperez@hotmail.com"
contacto1="uid1"
contacto2="uid2"

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
        os.mkdir(email+'/contactos')
    except OSError:
        print ("Creation of the directory %s failed" % email)
    else:
        print ("Successfully created the directory %s " % email)

#for de contactos i=0
#si existe el paciente
try:
    #existe el contacto?
    print(pacientesJSON[email][contacto1])
    pacientesJSON[email][contacto1]="true"
except:
    print('no existe contacto= '+contacto1)
    #AÑADIR A JSON
    newPacienteString=newPacienteString+'{\"'+contacto1+'\":"true"'
    #CREAR DIRECTORIO DE UN CONTACTO
    try:
        os.mkdir(email+'/contactos/'+contacto1)
    except OSError:
        print ("Creation of the directory %s failed" % email+'/contactos/'+contacto1)
    else:
        print ("Successfully created the directory %s " % email+'/contactos/'+contacto1)
    #PARA TODAS LAS FOTOS
    storage.child(email+'/contactos/'+contacto1+'/triste.jpg').download("./"+email+'/contactos/'+contacto1+"/triste.jpg")


#for de contactos i!=0
try:
    #existe el contacto?
    print(pacientesJSON[email][contacto2])
    pacientesJSON[email][contacto2]="true"
except:
    print('no existe contacto= '+contacto2)
    #AÑADIR A JSON
    newPacienteString=newPacienteString+',\"'+contacto2+'\":"true"'
    print(newPacienteString)
    #CREAR DIRECTORIO DE UN CONTACTO
    try:
        os.mkdir(email+'/contactos/'+contacto2)
    except OSError:
        print ("Creation of the directory %s failed" % email+'/contactos/'+contacto2)
    else:
        print ("Successfully created the directory %s " % email+'/contactos/'+contacto2)
    #PARA TODAS LAS FOTOS
    storage.child(email+'/contactos/'+contacto2+'/triste.jpg').download("./"+email+'/contactos/'+contacto2+"/triste.jpg")

#end for de contactos
if newPacienteString!='':
    if email in newPacienteString:
        newPacienteString=newPacienteString+'}}'
        add=json.loads(newPacienteString)
        pacientesJSON.update(add)
        print(json.dumps(pacientesJSON))
    else:
        newPacienteString=newPacienteString+'}'
        add=json.loads(newPacienteString)
        pacientesJSON[email]=add
        print(json.dumps(pacientesJSON))

#RECORRER PARA BUSCAR FALSES
auxPacientesJSON = copy.deepcopy(pacientesJSON)
for pacienteSearchFalse in pacientesJSON.keys():
    print(pacienteSearchFalse)
    for contactoSearchFalse in pacientesJSON[pacienteSearchFalse].keys():
        print(contactoSearchFalse)
        if pacientesJSON[pacienteSearchFalse][contactoSearchFalse]=="false":
            #se elimino de Storage
            #ELIMINAR CARPETA
            try:
                for filename in os.listdir(email+'/contactos/'+contactoSearchFalse):
                    print(filename)
                    file_path = os.path.join(email+'/contactos/'+contactoSearchFalse, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                os.rmdir(email+'/contactos/'+contactoSearchFalse)
            except OSError:
                print ("Deletion of the directory %s failed" % email+'/contactos/'+contactoSearchFalse)
            else:
                print ("Successfully deleted the directory %s" % email+'/contactos/'+contactoSearchFalse)
            #ELIMINAR DE JSON
            auxPacientesJSON[pacienteSearchFalse].pop(contactoSearchFalse,None)
            print(json.dumps(auxPacientesJSON))

pacientesJSON= copy.deepcopy(auxPacientesJSON)
print(json.dumps(pacientesJSON))

#PONER A FALSE DE NUEVO
for pacienteSearchFalse in pacientesJSON.keys():
    print(pacienteSearchFalse)
    for contactoSearchFalse in pacientesJSON[pacienteSearchFalse].keys():
        print(contactoSearchFalse)
        pacientesJSON[pacienteSearchFalse][contactoSearchFalse]="false"

print(json.dumps(pacientesJSON))