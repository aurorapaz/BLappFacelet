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

storage.child('aurorapazperez@gmail.com/contactos/uid1/triste.jpg').download("./aurorapazperez@gmail.com/contactos/uid1/triste.jpg")