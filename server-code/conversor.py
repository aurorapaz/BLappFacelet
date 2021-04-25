import os
import cv2

old_path = "C:/Users/auror/app-extra/server-code/pruebas1"
new_path = "C:/Users/auror/app-extra/server-code/reconServerTiempos/p/pruebas"

for dirpath, dirnames, filenames in os.walk(old_path):
    #print(dirnames)
    for dirname in dirnames:
        dirr = old_path  + "/" + dirname
        for p, n, files in os.walk(dirr):
            for file in files:
                pathh = dirr + "/" + file
                img = cv2.imread(pathh)
                name= file.rsplit(".", 1)[0]
                
                diir = new_path + "/" + dirname
                print (diir)
                cv2.imwrite(diir + "/" + name + ".jpg", img)
