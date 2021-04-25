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
    model=DeepFace.build_model('Facenet')
    for dirpath, dirnames, filenames in os.walk(dbPath):
        for dirname in dirnames:
            dir = dbPath + '/' + dirname
            print("*********" + dir)
            df = DeepFace.find(img_path=imgPath, db_path = dir, model_name="Facenet",model=model,enforce_detection=False)
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

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")
   return cv2.LUT(image, table)

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
        f = open("tiempos.txt", "a")
        f.write("Recepcion de foto= " + str(datetime.datetime.now().strftime('%d/%m/20%y %H:%M:%S')) + "\n")
        f.close()
        print(name['name'])
        email=name['name']
        npa= np.fromstring(bytes(photo['photo']),np.uint8)
        img = cv2.imdecode(npa,cv2.IMREAD_COLOR)
        img=adjust_gamma(img, gamma=2.0)
        if os.path.isdir('C:/Users/auror/app-extra/server-code/'+ name['name'] +'/Contactos'):
            contactoReconocido=recognize(img,'C:/Users/auror/app-extra/server-code/'+ name['name'] +'/Contactos')
            print(contactoReconocido)
            now = datetime.datetime.now()
            horaReconocimiento=now.strftime('%d/%m/20%y %H:%M')

            #Buscar el contacto reconocido
            pacientes = db.collection('pacientes').get()
            for contactoRecon in contactoReconocido:
                if contactoRecon!="unknown":
                    for paciente in pacientes:
                        try:
                            if email in paciente.get('email'):
                                for contacto in db.collection('pacientes',paciente.id,'contactos').get():
                                    if contacto.id==contactoRecon:
                                        db.collection('pacientes',paciente.id,'contactos').document(contacto.id).update({u'interacciones': firestore.ArrayUnion([horaReconocimiento])})
                                        f = open("tiempos.txt", "a")
                                        f.write("Actualizacion de interaccion= " + str(datetime.datetime.now().strftime('%d/%m/20%y %H:%M:%S')) + "\n")
                                        f.close()
                        except:
                            print()
            cv2.imwrite("./esp/imagen"+str(i)+".jpg",img)
            i+=1
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            result = False;
            if len(contactoReconocido) > 1 :
                result = contactoReconocido.count(contactoReconocido[0]) == len(contactoReconocido)
            else:
                if len(contactoReconocido) == 1:
                    if contactoReconocido == "unknown":
                        return web.Response(text=json.dumps({'status': 'unsuccess'}), status=200)
                else:
                    return web.Response(text=json.dumps({'status': 'unsuccess'}), status=200)
            if result:
                return web.Response(text=json.dumps({'status': 'unsuccess'}), status=200)
            else:
                return web.Response(text=json.dumps({'status': 'success'}), status=200)
        else:
            return web.Response(text=json.dumps({'status': 'unsuccess'}), status=200)
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

#Set up
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
app = web.Application()
app.router.add_get('/',apitest)
app.router.add_post('/save',checkPhoto)
if __name__ == '__main__':
    web.run_app(app)