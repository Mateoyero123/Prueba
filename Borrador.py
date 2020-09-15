# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 11:26:25 2020

@author: mateo
"""


import pandas as pd
from fpdf import FPDF
from PIL import Image
import os
import json

pdf = FPDF()
imagelist = [] 

folder = "C:/Users/mateo/Desktop/Python/Crediluca/Face-Recognition/Test"                                                   # Folder containing all the images.
name = "cedula"

for dirpath, dirnames, filenames in os.walk(folder):
    for filename in [f for f in filenames if f.endswith(".jpg")]:
        full_path = os.path.join(dirpath, filename)
        imagelist.append(full_path)

imagelist.sort()                                               # Sort the images by name.
for i in range(0, len(imagelist)):
    print(imagelist[i])                                                     # Name of the output PDF file.

for i in range(0, len(imagelist)):
    im1 = Image.open(imagelist[i])                             # Open the image.
    width, height = im1.size                                   # Get the width and height of that image.
    if width > height:
        im2 = im1.transpose(Image.ROTATE_270)                  # If width > height, rotate the image.
        os.remove(imagelist[i])                                # Delete the previous image.
        im2.save(imagelist[i])                                 # Save the rotated image.
        # im.save

print("\nFound " + str(len(imagelist)) + " image files. Converting to PDF....\n")

for image in imagelist:
    pdf.add_page()
    pdf.image(image, 0, 0, 210, 297)                           # 210 and 297 are the dimensions of an A4 size sheet.

pdf.output(folder + name, "F")                                 # Save the PDF.

print("PDF generated successfully!")



##INDICADORES 

##Habitos
##Informacion de GPS 




##CONSUMO

##PATRON DE CONSUMO ONLINE## 

Base_general=pd.data_frame()

def comparar(tiempo_del, ciudad, ocupacion, sueldo):
    patron=0
    t=tiempo_del
    c=ciudad
    o=ocupacion
    s=float(sueldo)
    r=float(100)
    ##Abrir base
    base=Base_general
    ##Creacion de filtros de base
    sub_base= base[(base['Ciudad'] == c) & (base['Ocupacion'] == o) & (base['Sueldo']<=(s+r)) & (base['Sueldo']>=(s-r))]
    mean= sub_base["Tiempo_Del"].mean()
    std= sub_base["Tiempo_Del"].std()
    ## Comparacion 
    if t > mean + std:
        patron=2
    elif t<mean + std: 
        patron=0
    else:
        patron=1 
    return patron


##INGRESO Y PRODUCTIVIDAD

##RESIDUO DEL INGRESO

def res(ingreso, nh18, canastapc):
    ing= ingreso
    n18=nh18
    cpc=canastapc
    costos=0
    ##generar costos##
    costos=cpc*(1+n18)
    ##Residuo 
    res= ing-costos 
    return res

##PRODUCTIVIDAD 
    
def productividad(ingreso,horas_trabajo):
    ing=ingreso 
    horas_t=horas_trabajo
    horas_m= horas_t*4
    ##Calcular
    pro= ing/horas_m
    return pro

## NIVEL DE PRODUCTIVIDAD RELATIVO

def nivel_productvidad(productividad, ocupacion, ciudad, edad, educacion):
    pro=productividad 
    oc=ocupacion
    ci=ciudad
    edad= edad
    edu=educacion
    rango=
    ##Abrir Base General
    base=Base_general
    ##Sub_base 
    sub_base= base[(base['Ciudad'] == ci) & (base['Ocupacion'] == oc)]
    media= sub_base["Productividad"].mean()
    estan=sub_base["Productividad"].std()
    ##Cuartiles 
    q25= sub_base["Productividad"].quantile(q=0.25)
    
    
    

    
    
     
        


    
    
    
    

        
        
    