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
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# List of image extensions to look for
IMG_EXTENSIONS = ['.png', '.jpeg', '.jpg', '.bmp', '.tiff']

def scrape_images(url, depth, images_dict=None):
    """
    Recursively scrape images from a website up to a certain depth.
    
    Parameters:
    url (str): The URL to start the scraping from.
    depth (int): The depth of the recursion. If depth == 0, the function returns immediately.
    images_dict (dict): A dictionary containing the images found in previous calls to this function. 
                        This parameter is used for the recursion.
                        
    Returns:
    dict: A dictionary containing all the images found in the website.
    """
    # If the images_dict is not provided, create a new one
    if images_dict is None:
        images_dict = {}

    # If we have reached the maximum depth, return the images dictionary
    if depth == 0:
        return images_dict

    # Parse the URL to get the domain name
    domain_name = urlparse(url).netloc

    # Send a request to the URL and parse the response with BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags and add them to the images_dict
    for img in soup.find_all('img'):
        img_src = img.get('src')

        # Check if the image source ends with a valid extension
        if any(img_src.endswith(ext) for ext in IMG_EXTENSIONS):
            # If the image source is a relative URL, add the domain name to the beginning
            if not img_src.startswith('http'):
                img_src = f'{domain_name}/{img_src.lstrip("/")}'
            
            # Add the image source to the images_dict
            if img_src in images_dict:
                images_dict[img_src].append(img.get('alt', ''))
            else:
                images_dict[img_src] = [img.get('alt', '')]

    # Recursively scrape images from all links on the page
    for link in soup.find_all('a'):
        link_href = link.get('href')

        # If the link is a relative URL, add the domain name to the beginning
        if not link_href.startswith('http'):
            link_href = f'{domain_name}/{link_href.lstrip("/")}'
        
        # Check if the link domain matches the original domain and scrape images from it
        if urlparse(link_href).netloc == domain_name:
            scrape_images(link_href, depth - 1, images_dict)

    return images_dict


images_dict = scrape_images('https://www.example.com', 2)


