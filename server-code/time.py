import datetime
f = open("./reconServerTiempos/resultados/tempos8.txt", "a")
now = datetime.datetime.now()
data = []
for i in range(7000):
    value = datetime.datetime.now()-now
    secs = value.seconds
    data.append(secs)
    print(secs)
print(sum(data)/len(data))
