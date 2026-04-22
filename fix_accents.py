import os
import re

words_to_fix = {
    "estadistica": "estadística",
    "Estadistica": "Estadística",
    "matematico": "matemático",
    "Matematico": "Matemático",
    "matematica": "matemática",
    "Matematica": "Matemática",
    "tecnologia": "tecnología",
    "Tecnologia": "Tecnología",
    "investigacion": "investigación",
    "Investigacion": "Investigación",
    "Analisis": "Análisis",
    "analisis": "análisis",
    "gestion": "gestión",
    "Gestion": "Gestión",
    "informacion": "información",
    "Informacion": "Información",
    "comunicacion": "comunicación",
    "Comunicacion": "Comunicación",
    "optimizacion": "optimización",
    "Optimizacion": "Optimización",
    "cientifico": "científico",
    "Cientifico": "Científico",
    "biologica": "biológica",
    "Biologica": "Biológica",
    "agricola": "agrícola",
    "Agricola": "Agrícola",
    "agroalimentaria": "agroalimentaria", # No accent
    "metodos": "métodos",
    "Metodos": "Métodos",
    "tecnicas": "técnicas",
    "Tecnicas": "Técnicas",
    "algoritmo": "algoritmo",
    "aplicacion": "aplicación",
    "Aplicacion": "Aplicación",
    "proposito": "propósito",
    "Proposito": "Propósito",
    "ultimo": "último",
    "Ultimo": "Último",
    "demografico": "demográfico",
    "Demografico": "Demográfico",
    "geografico": "geográfico",
    "Geografico": "Geográfico",
    "economico": "económico",
    "Economico": "Económico",
    "dinamica": "dinámica",
    "Dinamica": "Dinámica",
    "practica": "práctica",
    "Practica": "Práctica",
    "basico": "básico",
    "Basico": "Básico",
    "sistematica": "sistemática",
    "Sistematica": "Sistemática",
    "evaluacion": "evaluación",
    "Evaluacion": "Evaluación",
    "clasificacion": "clasificación",
    "Clasificacion": "Clasificación",
    "exito": "éxito",
    "Exito": "Éxito",
    "introduccion": "introducción",
    "Introduccion": "Introducción",
    "construccion": "construcción",
    "Construccion": "Construcción",
    "resolucion": "resolución",
    "Resolucion": "Resolución",
    "solucion": "solución",
    "Solucion": "Solución",
    "extencion": "extensión", # Also fixing extra spelling errors
    "Extencion": "Extensión",
    "produccion": "producción",
    "Produccion": "Producción"
}

files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('<!DOCTYPE')]
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    for wrong, right in words_to_fix.items():
        # Match word boundaries to avoid replacing parts of other words
        # but handle Spanish correctly (- is word boundary in regex? \b works for simple ascii)
        pattern = r'\b' + wrong + r'\b'
        if re.search(pattern, content):
            content = re.sub(pattern, right, content)
            modified = True
            print(f"Fixed {wrong} -> {right} in {f}")
    
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
