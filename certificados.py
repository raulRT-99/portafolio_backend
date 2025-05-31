import os
import json
from flask import url_for

with open('static/info_json/constancias.json', 'r', encoding="utf-8") as file:
    data_constancia = json.load(file)

with open('static/info_json/certificados.json', 'r', encoding="utf-8") as file:
    data_certificado = json.load(file)

def getImagePaths(dir):
    images_paths = list_files(dir)
    return images_paths

def list_files(directorio):
    files = []
    try:
        for raiz, directorios, archivos in os.walk(directorio):
            for archivo in archivos:
                ruta_completa = archivo
                files.append(ruta_completa)
    except Exception as exp:
        print("error -- "+str(exp))
    return files

def info(images, lang, type):
    info_lang = data_constancia[lang] if type == 'cons' else data_certificado[lang]
    image_info = []
    for image in images:
        image_name = image.replace(".jpg",'').replace(".png",'').replace(".jpeg",'')
        for info in info_lang:
            if str(info['id']) == image_name:
                image_cert = info
                file_folder = 'constancias' if type == 'cons' else 'certifications'
                image_cert['image'] = url_for('static', filename=f'{file_folder}/{image}')
                image_info.append(image_cert)
    return image_info
