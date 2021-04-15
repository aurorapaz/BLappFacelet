import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Datos estaticos
email="aurorapazperez@gmail.com"
contactoReconocido="Aurora Paz Pérez"
horaReconocimiento="15/04/2021 23:00"

#Set up
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

#Buscar el contacto reconocido
pacientes = db.collection('pacientes').get()
for paciente in pacientes:
    try:
        if email in paciente.get('email'):
            for contacto in db.collection('pacientes',paciente.id,'contactos').get():
                nombreCompleto=contacto.get('nombre')+' '+contacto.get('apellidos')
                if nombreCompleto==contactoReconocido:
                    db.collection('pacientes',paciente.id,'contactos').document(contacto.id).update({u'interacciones': firestore.ArrayUnion([horaReconocimiento])})
    except:
        print()
