# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 07:46:09 2020

@author: mateo
"""


import requests
import pandas as pd
import os 
from datetime import datetime
from datetime import date
import urllib
import xlrd


def encontrar_canasta():

    def canasta (year,mes):
        abre= mes[0:3]
        abre= abre.lower()
        #print(abre)
        year= str(year)
        
        url="https://www.ecuadorencifras.gob.ec/documentos/web-inec/Inflacion/canastas/Canastas_2020/" + mes + "-"+ year +"/4.%20Ipc_canastabasica_nacional_ciudades_"+ abre +"_"+ year +".xls"
        #print(url)
        file_name, headers = urllib.request.urlretrieve(url)
        #print (file_name)
        file = xlrd.open_workbook(file_name)
        sheet_names = file.sheet_names()
        #print('Sheet Names', sheet_names)
        xl_sheet = file.sheet_by_index(1)
        #print ('Sheet name: %s' % xl_sheet.name)
        row_encabezados= xl_sheet.row(12)
        row_valores= xl_sheet.row(15)
        #print(row_encabezados)
        #print(row_valores)
        nombre=[]
        for x in row_encabezados:
            x=str(x)
            name= x.split(":",1)[1]
            nombre.append(name)
        #print(nombre)
        valores=[]
        for y in row_valores:
            y=str(y)
            dato= y.split(":",1)[1]
            valores.append(dato)
        #print(valores)
        tabla= pd.DataFrame(valores)
        tabla["1"]= nombre
        tabla=tabla.transpose()
        tabla= tabla.rename(columns=tabla.iloc[1])
        tabla= tabla.drop(tabla.index[1])
        #print(tabla)
        canasta= tabla["'Costo Actual en Dólares'"].mean()
        
        
        
        return canasta
        
    
        
    now = datetime.now()
    
    ## FUncion Obetener fecha actual en palabras 
    
    def obtener_mes(mes):
        
        if mes==1 :
            mes_letras= 'Enero'
        elif mes==2 :
            mes_letras= 'Febrero'
        elif mes==3:
            mes_letras= 'Marzo'  
        elif mes==4 :
            mes_letras= 'Abril'  
        elif mes==5 :
            mes_letras= 'Mayo'  
        elif mes==6:
            mes_letras= 'Junio'  
        elif mes==7 :
            mes_letras= 'Julio'  
        elif mes==8 :
            mes_letras= 'Agosto'  
        elif mes==9 :
            mes_letras= 'Septiembre'  
        elif mes==10 :
            mes_letras= 'Octubre'  
        elif mes==11 :
            mes_letras= 'Noviembre'  
        elif mes==12 :
            mes_letras= 'Diciembre'  
            
        return mes_letras
    
    
    def year_canasta(year,month):
        year_ca=year
        month_ca=month
        
        if month_ca==1:
            year_ca-=1
        else:
            year_ca=year_ca
        return year_ca
        
    
    #### Main ####
    
    ####Obtener la fecha actual
    now=datetime.now()
    ##Obtener year y month 
    fecha = now.today()
    year= fecha.year
    meses=fecha.month
    ##Encontrar ano 
    year_1= year_canasta(year,meses)
    #print(year_1)
    ###Encontrar mes anterior
    meses_ant= meses-1
    ##Encontrar mes en palabras###
    mes_canasta= str(obtener_mes(meses_ant))
    #print (mes_canasta)
    
    valor_canasta= canasta(year_1,mes_canasta)
    
    return valor_canasta
    



    