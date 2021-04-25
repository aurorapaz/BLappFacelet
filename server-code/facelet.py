import os
from deepface import DeepFace
from mtcnn.mtcnn import MTCNN
import cv2

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
        x1=y1=w1=h1=100
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
    if(verifyFace(img)):
        names = getFaces(image, path)
        return names
    else:
        names = []
        return names