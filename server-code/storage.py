import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore_v1

import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

collection_ref = db.collection(u'storage').document(u'aurorapazperez@gmail.com')

def on_snapshot(collection_snapshot, changes, read_time):

    # for doc in collection_snapshot.documents:

    #     print(u'{} => {}'.format(doc.id, doc.to_dict()))
    for ch in changes:
        print(ch.document.to_dict())

collection_watch = collection_ref.on_snapshot(on_snapshot)
while True:
    time.sleep(1)
    print('procesando....')

# Terminate this watch collection_watch.unsubscribe()