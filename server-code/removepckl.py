import os
import cv2

old_path = "C:/Users/auror/app-extra/server-code/reconServerTiempos/p"

for dirpath1, dirnames1, filenames1 in os.walk(old_path):
    for dirname1 in dirnames1:
        print(dirname1)
        for dirpath, dirnames, filenames in os.walk("C:/Users/auror/app-extra/server-code/reconServerTiempos/p/"+ dirname1):
            print(dirnames)
            for dirname in dirnames:
                dirr = old_path  + "/" + dirname1 + "/" + dirname
                print(dirr)
                for p, n, files in os.walk(dirr):
                    for file in files:
                        pathh = dirr + "/" + file
                        print(pathh)
                        if file.startswith('representatio'):
                            os.remove(pathh)
