from aiohttp import web
import json
from PIL import Image
import io
import numpy as np
import cv2
import os
from deepface import DeepFace
from mtcnn.mtcnn import MTCNN
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

def getName(imgPath, dbPath):
    distance = 100
    name = "unknown"
    for dirpath, dirnames, filenames in os.walk(dbPath):
        for dirname in dirnames:
            dir = dbPath + '/' + dirname
            print("*********" + dir)
            df = DeepFace.find(img_path=imgPath, db_path = dir, model_name="Facenet")
            if not (df.size == 0):
                if(distance > df.at[0,'Facenet_cosine']):
                    distance = df.at[0,'Facenet_cosine']
                    name = dirname
    return name

def detectFaces(data):
    detector = MTCNN()
    faces = detector.detect_faces(data)
    return faces


def verifyFace(img):
    faces = detectFaces(img)
    if (len(faces)==0):
        return False
    else:
        return True

def getFaces(img, file):
    names = []
    faces = detectFaces(img)
    H,W,_ = img.shape
    for face in faces:
        x1=y1=w1=h1=500
        x,y,w,h = face['box']
        if (x<x1): x1=x
        if (y<y1): y1=y
        if (y+h+h1>H): h1=H-h-y
        if (x+w+w1>W): w1=W-w-x
        face_img = img[y-y1:y+h+h1, x-x1:x+w+w1]
        name = getName(face_img, file)
        names.append(name)
    return names

def recognize(image, path):
    if(verifyFace(image)):
        names = getFaces(image, path)
        return names
    else:
        names = []
        return names

i = 0
async def apitest(request):
    print("request")
    result ={"status":"200"}
    return web.Response(text=json.dumps(result), status=200)

async def checkPhoto(request):
    global i
    try:
        j = await request.json()
        dicts = [{k:v} for k,v in j.items()]
        name = dicts[0]
        photo = dicts[1]
        print(name['name'])
        email=name['name']
        npa= np.fromstring(bytes(photo['photo']),np.uint8)
        img = cv2.imdecode(npa,cv2.IMREAD_COLOR)
        contactoReconocido=recognize(img,'C:/Users/auror/app-extra/server-code/'+name['name']+'/contactos')
        print(contactoReconocido)
        now = datetime.datetime.now()
        horaReconocimiento=now.strftime('%d/%m/20%y %H:%M')

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
                        if contacto.id==contactoReconocido:
                            db.collection('pacientes',paciente.id,'contactos').document(contacto.id).update({u'interacciones': firestore.ArrayUnion([horaReconocimiento])})
            except:
                print()
        # cv2.imshow("foto",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return web.Response(text=json.dumps({'status': 'success'}), status=200)
    except Exception as e:
        print (e)
        response_obj = {'status': 'failed', 'reason': str(e)}
        web.Response(text=json.dumps(response_obj), status=500)

async def show(request):
    try:
        print("request")
        return web.Response(text=json.dumps({'data': 'success'}), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        web.Response(text=json.dumps(response_obj), status=500)
app = web.Application()
app.router.add_get('/',apitest)
app.router.add_post('/save',checkPhoto)
if __name__ == '__main__':
    web.run_app(app)