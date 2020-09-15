# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:42:16 2020

@author: mateo
"""


import json
import time
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import seaborn as sns
import warnings
import requests
from datetime import datetime
from sklearn.cluster import KMeans
from geopy.distance import vincenty
from matplotlib.collections import PatchCollection
from IPython.display import Image
import folium
from geopy.geocoders import Nominatim
from pandas.io.json import json_normalize
warnings.filterwarnings('ignore') 


##ID DE USUARIO



######## METODOS DE TRANSPORTE ###########

file= "C:/Users/mateo/Desktop/Python/Crediluca/2019_SEPTEMBER.json"
with open(file, 'r') as fh:
    data = json.loads(fh.read())
    data = data['timelineObjects']
w=[]
count=0
##Extraer informacion
for locations in data[0:200]:
    if "activitySegment" in locations:
        count+=1
        w.append((count,locations["activitySegment"]['startLocation']['latitudeE7'],
                  locations["activitySegment"]['startLocation']['longitudeE7'],
                  locations["activitySegment"]['endLocation']['latitudeE7'],
                  locations["activitySegment"]['endLocation']['longitudeE7'],
                  locations["activitySegment"]['duration']['startTimestampMs'],
                  locations["activitySegment"]['duration']['endTimestampMs'],
                  locations["activitySegment"]["duration"],
                  locations["activitySegment"]['activityType'],
                  locations["activitySegment"]['confidence'],
                  locations["activitySegment"]['activities'][0]['probability']))
print(w)
##  Armar un dataframe
drive = pd.DataFrame(w, columns=["ID",'Latitud_start', 'Longitud_start',
                              'Latitud_end','Longitud_end','Start_time',
                              "End_time",'Duracion',"Transporte","Confianza",
                              "Probabilidad"])
print(drive)

##Coordenadas
drive["Latitud_start"]=drive["Latitud_start"]/1e7
drive ["Longitud_start"]=drive["Longitud_start"]/1e7
drive["Latitud_end"]=drive["Latitud_end"]/1e7
drive ["Longitud_end"]=drive["Longitud_end"]/1e7


print(drive)

##Pasar variables a formato datetime########

drive["Start_time"] = [x[0:-3]for x in drive["Start_time"]]
drive["Start_time"] = pd.to_datetime(drive["Start_time"], unit='s')

##End
drive["End_time"] = [x[0:-3]for x in drive["End_time"]]
drive["End_time"] = pd.to_datetime(drive["End_time"], unit='s')

print(drive)

#### Pasara decimales la probabilidad 

drive["Probabilidad"]= drive["Probabilidad"]/100

### Generar dummies de confianza#### 
drive_dumm = pd.get_dummies(drive[['Confianza']], prefix="", prefix_sep="")
drive_dumm["ID"]=drive["ID"]

print(drive_dumm)
drive_raw= pd.merge(drive,drive_dumm, on='ID')
print(drive_raw)
##Generar Dummies de Transporte 
drive_trans = pd.get_dummies(drive[['Transporte']], prefix="", prefix_sep="")
drive_trans["ID"]=drive["ID"]

drive_final= pd.merge(drive_raw,drive_trans, on='ID')
print(drive_final)

####Generar procentaje de cada transporte sobre el total

walk= drive_final["WALKING"].mean() 

vehi=drive_final["IN_PASSENGER_VEHICLE"].mean()

moto= drive_final['MOTORCYCLING'].mean()

bus= drive_final["IN_BUS"].mean()

lista= [walk,vehi,moto,bus]
print(lista)

trans=pd.DataFrame(columns=["ID","WALKING","IN_PASSENGER_VEHICLE","MOTORCYCLING","IN_BUS"])
ID_1=101
print(ID_1)
trans["ID"]=ID_1


print(trans["ID"])













