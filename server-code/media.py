data = [2,3,4]
for j in range(22):
    f = open("resultadosPruebas.txt", "a")
    f.write("Ronda " + str(8+j*2) + " carpetas= " + str(sum(data)/len(data)))
    f.close()
