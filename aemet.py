from matplotlib import pyplot as plt
import requests
import json
import pandas as pd
import numpy as npy
import locale
import datetime

# api de acceso a los datos
secret = open('aemet-key.txt', 'r').readline().strip('\n')
print(secret)
apikey = {"api_key": secret}
#apikey = {"api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYXJsb3MucGlxdWVyZXNAZ21haWwuY29tIiwianRpIjoiYjNhMDZiNzktMDgyZi00NjIyLWJkM2UtMmY2YmFlNzkwMjljIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE2MTA5MDYyNjYsInVzZXJJZCI6ImIzYTA2Yjc5LTA4MmYtNDYyMi1iZDNlLTJmNmJhZTc5MDI5YyIsInJvbGUiOiIifQ.Plkc4xz_j8cPbER3q8D06lh4aY8c4QSAXHMZ2qOuVak"}

#EMA Valencia
estacion = 8416
start = '2020-01-01T00:00:00UTC'
end = '2020-12-31T23:59:59UTC'

# ejemplo de llamada
# https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2020-01-01T00:00:00UTC/fechafin/2020-12-31T23:59:59UTC/estacion/8416/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYXJsb3MucGlxdWVyZXNAZ21haWwuY29tIiwianRpIjoiYjNhMDZiNzktMDgyZi00NjIyLWJkM2UtMmY2YmFlNzkwMjljIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE2MTA5MDYyNjYsInVzZXJJZCI6ImIzYTA2Yjc5LTA4MmYtNDYyMi1iZDNlLTJmNmJhZTc5MDI5YyIsInJvbGUiOiIifQ.Plkc4xz_j8cPbER3q8D06lh4aY8c4QSAXHMZ2qOuVak


base = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{ini}/fechafin/{fin}/estacion/{ema}/"

url = base.format(ini = start, fin = end, ema = estacion)
print(url)

headers = {
    'cache-control': "no-cache"
    }

dir = requests.request("GET", url, headers=headers, params=apikey)

datadir = json.loads(dir.text)["datos"]

data = requests.request("GET", datadir, headers=headers)

# this provides an list of dictionaries items. Each item being a station
vlcTemps = json.loads(data.text)

frame = pd.DataFrame(vlcTemps)

frame.shape
# 31 days, 10 data elements each

graph=pd.DataFrame(frame[['fecha','tmin', 'tmax']])

graph.tmin = graph.tmin.replace(',','.', regex=True).astype(float)
graph.tmax = graph.tmax.replace(',','.', regex=True).astype(float)
graph.fecha = pd.to_datetime(graph.fecha,format='%Y-%m-%d', errors='coerce')

graph.info()

plt.plot(graph.fecha, graph.tmin)
plt.plot(graph.fecha, graph.tmax)


