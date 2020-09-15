# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:05:56 2020

@author: mateo
"""
### Import Libraries

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


############################### GENERAR BASE(Programadores)######################
##Unicamente con fin de evaluacion

file= "C:/Users/mateo/Desktop/Python/Crediluca/2019_SEPTEMBER.json"
with open(file, 'r') as fh:
    data = json.loads(fh.read())
    data = data['timelineObjects']
d=[]
count=0
##Extraer informacion
for locations in data[0:200]:
    if 'placeVisit' in locations:
        count+=1
        d.append((count,locations['placeVisit']['location']['latitudeE7'],
                  locations['placeVisit']['location']['longitudeE7'],
                  locations['placeVisit']['duration']['startTimestampMs'],
                  locations['placeVisit']['duration']['endTimestampMs']))
#print(d)
##  Armar un dataframe
df = pd.DataFrame(d, columns=["ID",'Latitud', 'Longitud', 'Startime','Endtime'])
#print(df)



##Cambiad e formato las variables


##Coordenadas
df["Latitud"]=df["Latitud"]/1e7
df["Longitud"]=df["Longitud"]/1e7
#print(df)
##Tiempo

df["Startime"] = [x[0:-3]for x in df["Startime"]]
df["Startime"] = pd.to_datetime(df["Startime"], unit='s')

##End
df["Endtime"] = [x[0:-3]for x in df["Endtime"]]
df["Endtime"] = pd.to_datetime(df["Endtime"], unit='s')

#print(df)



##Separar fecha y hora

##Start

df['new_date_start'] = [d.date() for d in df['Startime']]
df['new_time_start'] = [d.time() for d in df['Startime']]

##End
df['new_date_end'] = [d.date() for d in df['Endtime']]
df['new_time_end'] = [d.time() for d in df['Endtime']]


#print(df)

##Generar el tiempo en el lugar 

df['diference']=(df.Endtime-df.Startime)
#print(df)
#Tranformar a segundos la diferencia 

df['diference_s']=df["diference"].dt.total_seconds()

#print(df)

#df["time_star"] = pd.to_datetime(df['new_time_start'])
#date=datetime.date.today()
#df["time_start"] = datetime.datetime.combine(date, df['new_time_start'])
#df['duracion']= (df["new_time_end"]) + (df["new_time_start"])
#print(df) 

##Generar hora promedio en el que estuvo en el lugar 
df['media_tiempo']= df.Startime + (df.Endtime - df.Startime)/2
#print(df)
#Separar tiempo centrarl de la fecha
df['media_tiempo'] = [d.time() for d in df['media_tiempo']] 
print(df)
df['media_tiempo']=[(a.hour * 60 + a.minute) * 60 + a.second for a in df["media_tiempo"]]
print(df)
#print(df)


#df['media_tiempo'] = [d.time() for d in df['media_tiempo']] 
#df["media_tiempo"]= pd.to_datetime(df['media_tiempo'])




#################### GENERAR CLUSTERS POR UBICACION ###############

##Generar clustes utilización indicadores de ubicación, para clasificar las zonas mas concurridas 



#Find latitude and longitude of City
 
address = 'Quito'

geolocator = Nominatim(user_agent="quito_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
#print('The geograpical coordinate of Quito are {}, {}.'.format(latitude, longitude))

#map_quito = folium.Map(location=[latitude, longitude], zoom_start=10)
#map_quito
#map_quito.save("mymap.html")

##GENERAR 

###Cluster por ubicacion

def cluster_ubicacion (base, num):
    
    # set number of clusters
    kclusters = num
    
    # Establecer base
    ##Generar un cluster 
    base_0=base.copy()
    
    location_grouped_clustering = base.drop(['ID','new_date_end','new_date_start',
                                           'new_time_end','new_time_start','Startime'
                                           ,'Endtime','diference','diference_s','media_tiempo'], 1)
    #print(location_grouped_clustering)
    
    # run k-means clustering
    kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(location_grouped_clustering)
    
    # check cluster labels generated for each row in the dataframe
    kmeans.labels_[0:10] 
    
    #print(kmeans)
    
    base_0.insert(0,'Cluster',kmeans.labels_)
    
    #print(df) 
    
    ##Crear a base con las duracion media en cada cada cluster
    
    df_cluster= base_0.groupby("Cluster").agg({'diference_s':'mean'})
    df_cluster.reset_index(level=0, inplace=True)
    #print(df_cluster)
    
    ##Generar media de hora en cada cluster 
    
    #df['media_tiempo_s']=df["media_tiempo"].dt.total_seconds()
    #df_cluster_1 = pd.DataFrame(pd.to_datetime(df.groupby('Cluster').mean().media_tiempo_s))
    #print(df_cluster_1)
    ##Find the centers of each cluster and generate a new dataframe
    
    center=kmeans.cluster_centers_ 
    
    ##Generar indice de clusters
    
    index=[]
    for x in range(kclusters):
        index.append(str(x))
        
    centers_location= pd.DataFrame(center, columns=['Latitud', 'Longitud'])
    centers_location["ID"]=(index)
    
    return centers_location, base_0

## Cluster Tiempo
    
def cluster_tiempo (base, num):
    
    # set number of clusters
    kclusters = num
    
    # Establecer base
    ##Generar un cluster 
    base_1=base.copy()
    base_2= base_1[["ID","media_tiempo"]]
    
    time_grouped_clustering = base_1.drop(['ID','new_date_end','new_date_start',
                                           'new_time_end','new_time_start','Startime'
                                           ,'Endtime','diference','diference_s','Latitud','Longitud'], 1)
    print(time_grouped_clustering)
    # run k-means clustering
    kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(time_grouped_clustering)
    
    # check cluster labels generated for each row in the dataframe
    kmeans.labels_[0:10] 
    
    #print(kmeans)
    
    base_2.insert(0,'Cluster_Tiempo',kmeans.labels_)
    
    
    ##Crear a base con las duracion media en cada cada cluster
    
    #df_cluster= base_1.groupby("Cluster").agg({'diference_s':'mean'})
    #df_cluster.reset_index(level=0, inplace=True)
    #print(df_cluster)
    
    ##Generar media de hora en cada cluster 
    
    #df['media_tiempo_s']=df["media_tiempo"].dt.total_seconds()
    #df_cluster_1 = pd.DataFrame(pd.to_datetime(df.groupby('Cluster').mean().media_tiempo_s))
    #print(df_cluster_1)
    ##Find the centers of each cluster and generate a new dataframe
    
    #center=kmeans.cluster_centers_ 
    
    ##Generar indice de clusters
    
    #index=[]
    #for x in range(kclusters):
        #index.append(str(x))
        
    #centers_location= pd.DataFrame(center, columns=['Latitud', 'Longitud'])
    #centers_location["ID"]=(index)
    
    return base_2


##CLAVE DEL API 
##Google

api_key= 'AIzaSyAqPAekTTiPQcTdLjQkf25U9gxhKz37EAQ'

##foursquare

CLIENT_ID= 'ZHBXLOKXBDJTGTNGXV0QQYJEKWGQIWKIFSTT5J3LIAOR5XRA'
CLIENT_SECRET= 'GUWJT2S42JQ3ADJ5LZSKRXXHPPWQV5NCIC3RI45FMQEOL52I'
VERSION='20180605'



def getNearbyVenues(cluster, latitudes, longitudes, radius=500):   
    LIMIT=500
    venues_list=[]
    for clusters, lat, lng in zip(cluster, latitudes, longitudes):
        #print(clusters)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        venue_results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            clusters, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in venue_results])
    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Cluster', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)

##Llamar a la funcion  y extrar los venues

def venues_cluster(base,num):
    df=base
    num=num
    
    centers_location, df_clus= cluster_ubicacion(df,num)
        
    
    location_venues= getNearbyVenues(cluster=centers_location["ID"],
                                     latitudes=centers_location["Latitud"],
                                     longitudes=centers_location["Longitud"])
    
    #print(location_venues.shape)
    #location_venues.head()
    
    ##Agrupar por Clusters
    
    location_venues.groupby("Cluster").count()
    
    #print('There are {} unique categories.'.format(len(location_venues['Venue Category'].unique())))
    
    ##Generar dummies de categorias
    
    location_onehot = pd.get_dummies(location_venues[['Venue Category']], prefix="", prefix_sep="")
    
    location_onehot['Cluster'] = location_venues['Cluster'] 
    
    fixed_columns = [location_onehot.columns[-1]] + list(location_onehot.columns[:-1])
    location_onehot = location_onehot[fixed_columns]
    location_onehot.head(47)
    
    ##Agrupar por clusters
    
    location_grouped = location_onehot.groupby('Cluster').mean().reset_index()
    location_grouped
    
    ## Generar frequencias de categorias
    num_top_venues = 3
    for code in location_grouped['Cluster']:
        #print("----"+code+"----")
        temp = location_grouped[location_grouped['Cluster'] == code].T.reset_index()
        temp.columns = ['venue','freq']
        temp = temp.iloc[1:]
        temp['freq'] = temp['freq'].astype(float)
        temp = temp.round({'freq': 2})
        #print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
        #print('\n')
        
    ##Generar top de categorias
        
    ##Funcion de categorias comunes 
    
    def return_most_common_venues(row, num_top_venues):
        row_categories = row.iloc[1:]
        row_categories_sorted = row_categories.sort_values(ascending=False)
        
        return row_categories_sorted.index.values[0:num_top_venues]
        
    num_top_venues = 3
    
    indicators = ['st', 'nd', 'rd']
    
    columns = ['Cluster']
    for ind in np.arange(num_top_venues):
        try:
            columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
        except:
            columns.append('{}th Most Common Venue'.format(ind+1))
    
    location_venues_sorted = pd.DataFrame(columns=columns)
    location_venues_sorted['Cluster'] = location_grouped['Cluster']
    
    for ind in np.arange(location_grouped.shape[0]):
        location_venues_sorted.iloc[ind, 1:] = return_most_common_venues(location_grouped.iloc[ind, :], num_top_venues)
    
    location_venues_sorted 
    location_venues_sorted["Cluster"]= location_venues_sorted["Cluster"].astype(int)
    
    #print(location_venues_sorted)
    
    
    
    
    
    ## MERGE INFORMACIPON POR CLUSTERS ###
    
    sectores= pd.merge(location_venues_sorted,df_clus, on='Cluster')
    return sectores, df_clus


##Main
    
sector,df_clus= venues_cluster(df,10)

print(sector)

###

print(df_clus)


tiempo= cluster_tiempo(df,3)

print(tiempo) 

base_final= pd.merge(df_clus, tiempo,on="ID")

print(base_final)






##Generate Map 

#map_clusters = folium.Map(location=[latitude, longitude], zoom_start=12)



# set color scheme for the clusters
#x = np.arange(kclusters)
#ys = [i + x + (i*x)**2 for i in range(kclusters)]
#colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
#rainbow = [colors.rgb2hex(i) for i in colors_array]

#markers_colors = []
#for lat, lon, poi, cluster in zip(df['Latitud'], df['Longitud'], df['ID'], df['Cluster Labels']):
    #label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    #folium.CircleMarker(
        #[lat, lon],
        #radius=5,
        #popup=label,
        #color=rainbow[cluster-1],
        #fill=True,
        #fill_color=rainbow[cluster-1],
        #fill_opacity=0.7).add_to(map_clusters)

#map_clusters
#map_clusters.save("mymap.html")




