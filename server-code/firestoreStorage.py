import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore_v1
import time
import json
import threading

def on_snapshot_pacientes(collection_snapshot, changes, read_time):
    for ch in changes:
        print(ch.document.id)
        contacts=str(ch.document.to_dict()).split(',')
        for contact in contacts:
            print(contact.split('\'')[1])

def hilo():
    global pacientes_ref
    pacientes_watch = pacientes_ref.on_snapshot(on_snapshot_pacientes)

    while True:
        time.sleep(1)
        print('procesando....')

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

pacientes_ref = db.collection(u'storage')

hiloWatch = threading.Thread(target=hilo)
hiloWatch.setDaemon(True)
hiloWatch.start()

while True:
    print('main')

# Terminate watch --> pacientes_watch.unsubscribe()