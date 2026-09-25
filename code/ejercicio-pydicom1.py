#%% [markdown]
# # 1. Importación de librerías necesarias

import pydicom as dicom
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pydicom.dataelem import DataElement
from pydicom.sequence import Sequence
from pydicom.tag import Tag
from pydicom.tag import TupleTag
from pydicom.dataset import Dataset


path="/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/I720"
dc= dicom.dcmread(path)
print("="*40)
print("dataset:")
print(dc)   
print("="*40)
print("file_meta:")
print(dc.file_meta)
print("="*40)


# %% [markdown]
# # 2. Imprimir todos los tags del dataset
print("\n=== METADATOS DEL DATASET ===")
for elem in dc:
    # Excluir la matriz binaria de píxeles para evitar saturar la salida de texto
    if elem.tag == (0x7FE0, 0x0010):
        print(f"{elem.tag} {elem.keyword} OW/OB: <Datos de Píxel Omitidos - Tamaño: {len(elem.value)} bytes>")
    else:
        print(f"{elem.tag} {elem.keyword}  {elem.VR} {elem.value}")


# %% [markdown]
# # 3. Lectura rápida sólo de metadatos sin cargar la imagen
ds_meta = dicom.dcmread(path, stop_before_pixels=True)
print(f"Paciente: {ds_meta.get('PatientName', 'N/A')}")

# # 4. Lectura forzada extrayendo sólo etiquetas específicas
tags = ['PatientID', 'Modality', 'StudyDate']
ds_especifico = dicom.dcmread(path, force=True, specific_tags=tags)
print(f"Modalidad: {ds_especifico.Modality}")


#%% [markdown]
# # 5. dir() vs .dir()

#  1. dir(ds) -> Retorna métodos de Python, de PyDICOM y las etiquetas del archivo
todo = dir(dc)
print(f"todo lo que se puede hacer con el archivo: \n {todo}")

# 2. ds.dir() -> Retor na SÓLO las etiquetas DICOM
etiquetas_solas = dc.dir()
print(f"\n etiquetas del archivo: \n {etiquetas_solas}")

# 3. ds.dir("Patient") -> Retorna sólo las etiquetas DICOM que contengan la palabra "Patient"
etiquetas_filtradas = dc.dir("Patient")
print(f"\n etiquetas que contienen 'Patient': \n {etiquetas_filtradas}")

# 4. Filtrar etiquetas relacionadas con dosis o rayos X
print("etiquetas de KVP/Dosis:", dc.dir("KVP", "Exposure"))   
# %%
print(dc.PatientName)
print(dc.PatientID)
print(dc.Modality)
print(dc.StudyDate)
# %%
# Acceso seguro con .get()
id_paciente = dc.get('PatientID', 'ID_NO_ENCONTRADO')
print(id_paciente)
# Obtener la instancia completa de DataElement
elem = dc.get_item((0x0010, 0x0010)) # PatientName
print(elem)
print(f"VR: {elem.VR}, Valor: {elem.value}")

# %%  [markdown]
## 1. Cargar el archivo DICOM

# 2. Extraer ÚNICAMENTE las etiquetas del grupo del Paciente (0x0010)
dc_paciente = dc.group_dataset(0x0010)

print("=== MÓDULO PACIENTE (GRUPO 0x0010) ===")
print(dc_paciente)

# Comprobar que es un nuevo Dataset filtrado
if "PatientName" in dc_paciente:
    print(f"\nPaciente extraído: {dc_paciente.PatientName}")

# 3. Extraer ÚNICAMENTE las etiquetas del grupo de Parámetros de Imagen (0x0028)
dc_imagen = dc.group_dataset(0x0028)

print("\n=== MÓDULO GEOMETRÍA DE IMAGEN (GRUPO 0x0028) ===")
print(f"Matriz: {dc_imagen.Rows} x {dc_imagen.Columns}")
print(f"Pixel Spacing: {dc_imagen.get('PixelSpacing', 'No definido')}")

# Nota: El dataset original 'ds' no ha sido modificado
print(f"\nTotal etiquetas en ds original: {len(dc)}")
print(f"Total etiquetas en dc_paciente: {len(dc_paciente)}") 
#%%
print(dc.dir("Patient"))
# %%

print("=== RECORRIDO DE PRIMER NIVEL CON .elements() ===")
#print(dc.elements())
# %%
# Recorrer cada DataElement directo del dataset
for elem in dc.elements():
    # Evitar imprimir la matriz binaria de píxeles pesada
    if elem.VR in ['OB', 'OW'] and elem.keyword == 'PixelData':
        print(f"Tag: {elem.tag} | Keyword: {elem.keyword:<25} | VR: {elem.VR:<3} | <Datos de Imagen Binarios>")
    else:
        print(f"Tag: {elem.tag} | Keyword: {elem.keyword:<25} | VR: {elem.VR:<3} | Valor: {elem.value}")
# %%
dc.pixel_array
# %%
elem = dc.get_item((0x0010, 0x0010)) # PatientName
print(elem)
print(f"VR: {elem.VR}, Valor: {elem.value}")
# %%
dd = dicom.Dataset()
dd.PatientName = "Romero^Jesus"
dd.Modality = "MR"
dd.SliceThickness = 2.5

# 1. Convertir el dataset a una cadena de texto JSON
json_string = dd.to_json()

print("--- Cadena JSON generada ---")
print(json_string)

# 2. Guardar la cadena directamente en un archivo .json en disco
with open("metadatos_estudio.json", "w", encoding="utf-8") as f:
    f.write(json_string)
!ls
# %%

# 1. Crear o cargar un dataset
de = dicom.Dataset()
de.PatientName = "Romero^Jesus"
de.Modality = "CT"
de.PatientID = "12345"

# 2. Convertir a diccionario compatible con el estándar DICOM JSON
json_dict = de.to_json_dict()

# 3. Inspeccionar el diccionario devuelto
import pprint
pprint.pprint(json_dict)

# Salida obtenida:
# {
#   '00080060': {'Value': ['CT'], 'vr': 'CS'},
#   '00100010': {'Value': [{'Alphabetical': 'Romero^Jesus'}], 'vr': 'PN'},
#   '00100020': {'Value': ['12345'], 'vr': 'LO'}
# }

# Acceder al tag directamente dentro del diccionario de Python
print("\nVR del Paciente:", json_dict["00100010"]["vr"])
# %%
from pydicom.dataset import Dataset

# Cadena JSON que cumple con la norma DICOM JSON (recibida de una API o archivo)
json_entrada = '''
{
    "00080060": {"vr": "CS", "Value": ["RTSTRUCT"]},
    "00100010": {"vr": "PN", "Value": [{"Alphabetical": "Anonimizado^Paciente"}]},
    "00280010": {"vr": "US", "Value": [512]}
}
'''

# 1. Reconstruir el objeto Dataset desde el JSON string
ds_reconstruido = Dataset.from_json(json_entrada)

# 2. Trabajar con el objeto como cualquier dataset de PyDICOM
print("Modalidad:", ds_reconstruido.Modality)
print("Nombre:", ds_reconstruido.PatientName)
print("Filas:", ds_reconstruido.Rows)

# Comprobar la clase del objeto resultante
print("Tipo de objeto:", type(ds_reconstruido))
# Salida: <class 'pydicom.dataset.Dataset'>
# %%
diccionario_dicom = {
    "00080060": {"vr": "CS", "Value": ["CT"]}
}

ds_desde_dict = Dataset.from_json(diccionario_dicom)
print(ds_desde_dict.Modality)
# %%
from pydicom.dataelem import DataElement

# Crear un elemento para Modality (CS = Code String)
elem = DataElement((0x0008, 0x0060), 'CS', 'MR')

print(f"Nombre: {elem.name}")
print(f"Keyword: {elem.keyword}")
print(f"Multiplicidad (VM): {elem.VM}")
# %%


# 1. Crear datasets hijos (items de la secuencia)
item1 = Dataset()
item1.CodeValue = "121008"
item1.CodeMeaning = "Doctor Present"

# 2. Encapsular en Sequence
secuencia = Sequence([item1])

# 3. Asignar al dataset principal
dr = Dataset()
dr.PurposeOfReferenceCodeSequence = secuencia

print(dr.PurposeOfReferenceCodeSequence[0].CodeMeaning)

# %%
# 1. Por dos argumentos numéricos (Hexadecimal o Decimal)
t1 = Tag(0x0010, 0x0010)
t2 = Tag(16, 16)

# 2. Por Tupla de dos elementos
t3 = Tag((0x0010, 0x0010))

# 3. Por Entero Único de 32 bits (0x00100010 = 1048592)
t4 = Tag(0x00100010)

# 4. Por Cadena Hexadecimal limpia de 8 caracteres (DICOM JSON)
t5 = Tag("00100010")

# 5. Por Cadena o valores pasados como dos argumentos separados (sin coma interna)
t6 = Tag("0010", "0010")  # Dos cadenas hexadecimales de 4 caracteres

# 6. Por Keyword estándar (String)
t7 = Tag("PatientName")

# Comprobación: Todos generan exactamente el mismo objeto
print(t1 == t2 == t3 == t4 == t5 == t6 == t7)  # Imprime: True
print(f"Representación visual: {t1}")          # Imprime: (0010, 0010)
print(f"Valor entero real: {int(t1)}")         # Imprime: 1048592
print(f"Valor en hex 32-bit: {hex(t1)}")       # Imprime: 0x100010
# %%
tag_estudio = Tag("StudyInstanceUID")  # Tag (0x0008, 0x0013)
tag_privado = Tag(0x0019, 0x1010)      # Tag de grupo impar (Privado)

# Extraer componentes individuales
print("Grupo:", hex(tag_estudio.group))       # 0x8
print("Elemento:", hex(tag_estudio.element)) # 0x13

# Atributos booleanos de clasificación
print("¿Es privado?:", tag_privado.is_private) # True
print("¿Es privado?:", tag_estudio.is_private) # False

# Formato de clave para DICOM JSON (8 caracteres hex en mayúscula)
print("JSON Key:", tag_estudio.json_key)       # "00080013"
# %%
# RECIBE: tuple[int, int] -> DEVUELVE: BaseTag
tag_obj = TupleTag((0x0008, 0x0060))

print(type(tag_obj))  # <class 'pydicom.tag.BaseTag'>
print(tag_obj)        # (0008, 0060)

#%%
# 1. Crear el Tag de 32 bits
tag_obj = Tag("Modality")  # (0x0008, 0x0060)

# 2. Extraer la tupla de enteros (grupo, elemento)
tupla_tag = (tag_obj.group, tag_obj.element)

print("Tipo de tag_obj:", type(tag_obj))      # <class 'pydicom.tag.BaseTag'>
print("Tipo de tupla_tag:", type(tupla_tag))  # <class 'tuple'>
print("Valor de la tupla:", tupla_tag)        # (8, 96) -> En decimal (0x0008, 0x0060)

# 3. Formatear la tupla en Hexadecimal
grupo, elemento = tupla_tag
print(f"Grupo: {hex(grupo)}, Elemento: {hex(elemento)}")  # Grupo: 0x8, Elemento: 0x60

# %%

# 1. Cargar el archivo DICOM

# 2. Definir el grupo del Overlay (los overlays estándar usan grupos pares desde 0x6000 hasta 0x601E)
GRUPO_OVERLAY = 0x6000  # Primer canal de overlay

# 3. Comprobar si existe la etiqueta de datos de overlay (0x6000, 0x3000)
if (GRUPO_OVERLAY, 0x3000) in dc:
    # Extraer la matriz 2D del overlay
    overlay_mask = dc.overlay_array(GRUPO_OVERLAY)

    print("=== INFORMACIÓN DE LA MATRIZ OVERLAY ===")
    print("Tipo de objeto:", type(overlay_mask))
    print("Dimensiones (Shape):", overlay_mask.shape)
    print("Tipo de dato (Dtype):", overlay_mask.dtype)
    print("Valores presentes:", np.unique(overlay_mask))  # Retorna [0, 1]

    # 4. Visualización: Superpconer la máscara roja sobre la imagen médica (Pixel Data)
    pixel_array = dc.pixel_array

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Imagen médica original
    axes[0].imshow(pixel_array, cmap="gray")
    axes[0].set_title("Pixel Data (Imagen base)")
    axes[0].axis("off")

    # Imagen médica con el Overlay superpuesto en transparente
    axes[1].imshow(pixel_array, cmap="gray")
    # Creamos una máscara donde 1 se dibuja en rojo y 0 permanece transparente
    overlay_rojo = np.zeros((*overlay_mask.shape, 4))
    overlay_rojo[overlay_mask == 1] = [1, 0, 0, 0.5]  # RGBA: Rojo semitransparente
    axes[1].imshow(overlay_rojo)
    axes[1].set_title("Imagen + Overlay (Grupo 0x6000)")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()

else:
    print(f"El archivo no contiene un overlay en el grupo {hex(GRUPO_OVERLAY)}.")



# %% [markdown]




# Obtener la matriz de imagen
arr = dc.pixel_array

print(f"Dimensiones de la imagen: {arr.shape}")
print(f"Tipo de dato: {arr.dtype}")
print(f"Valor máximo de píxel: {arr.max()}")

# %%
import pydicom
from pydicom.uid import JPEG2000Lossless, RLELossless

# 1. Cargar archivo no comprimido
dc = pydicom.dcmread("/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/I720")
print("Sintaxis inicial:", dc.file_meta.TransferSyntaxUID.name)

# 2. Comprimir directamente a JPEG 2000 Lossless
dc.compress(JPEG2000Lossless)

print("Sintaxis comprimida:", dc.file_meta.TransferSyntaxUID.name)

# 3. Guardar el archivo comprimido
dc.save_as("estudio_j2k.dcm")
# %%
cruda=dicom.dcmread("/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/IMG-0002-00069.dcm")
procesada=dicom.dcmread("/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/IMG-0002-00069 (2).dcm")

print(procesada)
# %%
