#!/usr/bin/env python

'''
El programa spider permitirá extraer todas las imágenes de un sitio web, de manera
recursiva, proporcionando una url como parámetro. Gestionarás las siguientes opciones
del programa:
    ./spider [-rlpS] URL
    
    •Opción -r : descarga de forma recursiva las imágenes en una URL recibida como
     parámetro.
     
    •Opción -r -l [N] : indica el nivel profundidad máximo de la descarga recursiva.
     En caso de no indicarse, será 5.
    
    •Opción -p [PATH] : indica la ruta donde se guardarán los archivos descargados.
     En caso de no indicarse, se utilizará ./data/.
    
    El programa descargará por defecto las siguientes extensiones:
        ◦.jpg/jpeg
        ◦.png
        ◦.gif
        ◦.bmp

BONUS:
    •Compatibilidad de ambos programas con .docx y .pdf.
    •Interfaz gráfica para la visualización y el manejo de los metadatos.
    •Eliminación de los metadatos
    •Modificación de los metadatos

'''

###############################
# ACCOUNT CLASS
###############################