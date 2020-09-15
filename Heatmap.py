# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:40:16 2020

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

###Abrir base de excel

base=pd.read_excel("C:/Users/mateo/Documents/Prueba Tipti/2020-09-08-orders (1).xlsx",sheet_name="Sheet")
base.dropna()
base["Numero"]= 1
lista= list(base.columns.values)
print(base) 
print(lista) 

#conseguir latitud y longitud de 


def extraer_cordenadas (Ciudad):
    ci= Ciudad
    sub_base= base[(base['City'] == ci)]
    sub_base_1= sub_base.groupby('Sector',as_index=False).count()
    print(sub_base_1)
    d=[]
    count=0
    for a in zip(sub_base_1["Sector"]):
        count+=1
        address = a
        geolocator = Nominatim()
        if address is not None:
            location = geolocator.geocode(address)
        if location is not None and location.latitude is not None:
            latitude = location.latitude
        if location is not None and location.longitude is not None:
            longitude = location.longitude
        d.append((address,latitude,longitude))
        print(d)
        print(count)
    df=pd.DataFrame(d,columns=["Sector","Latitud","Longitud"])
    print(df)
    return df

bas=extraer_cordenadas("Quito")



        
    
