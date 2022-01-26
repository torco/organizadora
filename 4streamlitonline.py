# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 18:23:27 2022

@author: torque
"""

import pandas as pd
import streamlit as st
#import plotly.express as px
#from PIL import Image
import urllib.request
import re
#from dataclasses import dataclass

st.set_page_config(page_title='INICIATIVAS')
st.subheader('OBSERVATORIO DE INICIATIVAS DE NORMA')
st.caption('ORDENADAS DE MAS A MENOS APOYOS')

def getdata():
    fp = urllib.request.urlopen("https://plataforma.chileconvencion.cl/m/iniciativa_popular/")
    mybytes = fp.read()

    mystr = mybytes.decode("ISO-8859-1")
    fp.close()

    lista1 = re.split('<div class="card iniciativa', mystr)
    #print(lista1[1])

    class Iniciativa:
        nombre: str
        numero: int
        likes: int
        def __init__(
                self, 
                nombre: str, 
                numero: int,
                likes: int,
            ) -> None:
            self.nombre = nombre
            self.numero = numero
            self.likes = likes

    lista2 = []

    for i in lista1:
        left = "<h1>"
        right = "</h1>"
        titulo = i.partition(left)[2].partition(right)[0]
        left = ">"
        right = "</a>"
        titulo = titulo.partition(left)[2].partition(right)[0]
        #print(titulo)
        left = '<h2>Propuesta nº '
        right = '</h2>'
        numeropropuesta = i.partition(left)[2].partition(right)[0]
        #print(numeropropuesta)
        left = '<div class="opciones">'
        right = ' <i class="fa fa-heart"></i>'
        likes = i.partition(left)[2].partition(right)[0]
        likes = likes.strip()
        if likes == "":
            likes = '0'
        if "K" in likes:
            likes = likes[:-1]
            substring = "000"
            likes = likes + substring
        if "." in likes:
            likes = likes.replace(".","")
            likes = likes[:-1]
        #print(likes)
        
        init = Iniciativa(titulo, numeropropuesta, likes)
        
        lista2.append(init)
        
        
        
       #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


    lista2.sort(key=lambda x: int(x.likes), reverse=True)
                    
    listanombres=[]
    listanumeros=[]
    listalikes=[]
                
    for i in lista2:
        filter = False
        if int(i.likes) > 10:
            filter=True
        if filter:
            a = i.nombre
            b = ''
            if (int(i.likes)) > 14999:
                b='**APROBADO**:'
            c=b+a
            #print(c)
            listanombres.append(c)
            #print(i.numero)
            listanumeros.append(i.numero)
            #print(i.likes)
            listalikes.append(i.likes)
            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            
    listaurls=[]
    for i in listanumeros:
        a = '<a href="https://plataforma.chileconvencion.cl/m/iniciativa_popular/detalle?id='
        z = '"target="_blank" >ver</a>'
        b = a + str(i) + z
        listaurls.append(b)
            
    dataframe = pd.DataFrame.from_dict(dict([("NOMBRE", listanombres), ("LIKES", listalikes), ("LINK", listaurls)]))
    
    cantidad=len(lista2)
    
    myhash = dataframe
    #print(listaurls[2])
    return myhash, cantidad
    print("eine request")
            
#t.caption("una iniciativa se aprueba con 15000 votos, no tiene efecto que tenga más puntos.")



##pd.set_option('display.max_colwidth', -1)
myhash = getdata()
#st.caption(myhash[1])

##st.dataframe(myhash)

st.write(myhash[0].to_html(escape=False, index=False), unsafe_allow_html=True)

st.caption("nota: esta página no muestra las iniciativas que tienen 10 o menos votos.")
