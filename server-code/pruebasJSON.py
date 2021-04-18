import json
import copy
pacientesStringExample='{"aurora":{"uid1":"false","uid2":"false"}}'
pacientesJSON=json.loads('{}')
newPacienteString=''
creacion= False
try:
    #existe paciente?
    print(pacientesJSON['mariel'])
    creacion=False
except:
    print('no existe paciente= '+'mariel')
    creacion=True
    #añadir a json y CREAR CARPETA
    newPacienteString=newPacienteString+'{"mariel":'
    print(newPacienteString)

#for de contactos i=0
#si existe el paciente
try:
    #existe el contacto?
    print(pacientesJSON['mariel']['uid3'])
    pacientesJSON['mariel']['uid3']="true"
except:
    print('no existe contacto= '+'uid3')
    #AÑADIR A JSON
    newPacienteString=newPacienteString+'{"uid3":"true"'
    #CREAR CARPETA

#for de contactos i!=0
try:
    #existe el contacto?
    print(pacientesJSON['mariel']['uid4'])
    pacientesJSON['mariel']['uid4']="true"
except:
    print('no existe contacto= '+'uid4')
    #AÑADIR A JSON
    newPacienteString=newPacienteString+',"uid4":"true"'
    print(newPacienteString)
    #CREAR CARPETA

#end for de contactos
if newPacienteString!='':
    if 'mariel' in newPacienteString:
        newPacienteString=newPacienteString+'}}'
        add=json.loads(newPacienteString)
        pacientesJSON.update(add)
        print(json.dumps(pacientesJSON))
    else:
        newPacienteString=newPacienteString+'}'
        add=json.loads(newPacienteString)
        pacientesJSON['mariel']=add
        print(json.dumps(pacientesJSON))

#RECORRER PARA BUSCAR FALSES
auxPacientesJSON = copy.deepcopy(pacientesJSON)
for pacienteSearchFalse in pacientesJSON.keys():
    print(pacienteSearchFalse)
    for contactoSearchFalse in pacientesJSON[pacienteSearchFalse].keys():
        print(contactoSearchFalse)
        if pacientesJSON[pacienteSearchFalse][contactoSearchFalse]=="false":
            #se elimino de Storage
            #ELIMINAR CARPETA
            print('eliminando carpeta')
            #ELIMINAR DE JSON
            auxPacientesJSON[pacienteSearchFalse].pop(contactoSearchFalse,None)
            print(json.dumps(auxPacientesJSON))

pacientesJSON= copy.deepcopy(auxPacientesJSON)
print(json.dumps(pacientesJSON))

#PONER A FALSE DE NUEVO
for pacienteSearchFalse in pacientesJSON.keys():
    print(pacienteSearchFalse)
    for contactoSearchFalse in pacientesJSON[pacienteSearchFalse].keys():
        print(contactoSearchFalse)
        pacientesJSON[pacienteSearchFalse][contactoSearchFalse]="false"

print(json.dumps(pacientesJSON))