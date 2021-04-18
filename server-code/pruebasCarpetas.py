import os,shutil

email="aurorapazperez@hotmail.com"
contactoReconocido="uid1"

#CREAR DIRECTORIO DEL PACIENTE
try:
    os.mkdir(email)
    os.mkdir(email+'/contactos')
except OSError:
    print ("Creation of the directory %s failed" % email)
else:
    print ("Successfully created the directory %s " % email)

#CREAR DIRECTORIO DE UN CONTACTO
try:
    os.mkdir(email+'/contactos/'+contactoReconocido)
except OSError:
    print ("Creation of the directory %s failed" % email+'/contactos/'+contactoReconocido)
else:
    print ("Successfully created the directory %s " % email+'/contactos/'+contactoReconocido)

#ELIMINAR DIRECTORIO DE UN CONTACTO Y TODOS LOS ARCHIVOS DENTRO
try:
    for filename in os.listdir(email+'/contactos/'+contactoReconocido):
        print(filename)
        file_path = os.path.join(email+'/contactos/'+contactoReconocido, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(email+'/contactos/'+contactoReconocido)
except OSError:
    print ("Deletion of the directory %s failed" % email+'/contactos/'+contactoReconocido)
else:
    print ("Successfully deleted the directory %s" % email+'/contactos/'+contactoReconocido)
