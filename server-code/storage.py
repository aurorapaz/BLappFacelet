import urllib
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCNogZeG46KnY95_0QL1oiBQDUSv0hPNcs",
    "authDomain": "facelet-40087.firebaseapp.com",
    "projectId": "facelet-40087",
    "storageBucket": "facelet-40087.appspot.com",
    "messagingSenderId": "151362094829",
    "appId": "1:151362094829:web:e1b1f4072525c9a0716ee4",
    "measurementId": "G-50RDMM4Q3V"
  }

firebase=pyrebase.initialize_app(firebaseConfig)

#define storage
storage=firebase.storage()

storage.child('gs://facelet-40087.appspot.com/aurorapazperez@gmail.com/contactos/uid1/enfado.jpg').download("enfado.jpg")