#%%
import pydicom

path = "/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/I720"
ds = pydicom.dcmread(path)

# ==========================================
# A. INSPECCIÓN DEL DATASET PRINCIPAL (ds)
# ==========================================

# 1. dir(ds) -> Inspección completa del objeto
todo_ds = dir(ds)
print(f"Total de atributos/métodos en ds: {len(todo_ds)}")

# 2. ds.dir() -> Retorna SÓLO las etiquetas DICOM del dataset
etiquetas_ds = ds.dir()
print(f"\nEtiquetas DICOM en el dataset principal:\n{etiquetas_ds}")

# 3. ds.dir("Patient") -> Filtrado por una palabra clave
etiquetas_paciente = ds.dir("Patient")
print(f"\nEtiquetas que contienen 'Patient':\n{etiquetas_paciente}")

# 4. ds.dir("KVP", "Exposure") -> Filtrado múltiple (OR)
etiquetas_tecnica = ds.dir("KVP", "Exposure")
print(f"\nEtiquetas de Técnica (KVP o Exposure):\n{etiquetas_tecnica}")


# ==========================================
# B. INSPECCIÓN DEL ENCABEZADO (ds.file_meta)
# ==========================================

# 1. dir(ds.file_meta) -> Métodos de Python + etiquetas del Grupo 0002
todo_meta = dir(ds.file_meta)
print(
    f"\nTotal de atributos/métodos en ds.file_meta:"
    f" {len(todo_meta)}"
)

# 2. ds.file_meta.dir() -> Retorna SÓLO las etiquetas DICOM del Grupo 0002
etiquetas_meta = ds.file_meta.dir()
print(f"\nEtiquetas DICOM del Encabezado (Grupo 0002):\n{etiquetas_meta}")

# 3. ds.file_meta.dir("Syntax") -> Filtrado en el encabezado
sintaxis_meta = ds.file_meta.dir("Syntax")
print(
    f"\nEtiquetas del encabezado que contienen 'Syntax':\n{sintaxis_meta}"
)

# %%
# 1. Recuperación segura de factores de escala (si no existen, usa valores neutros)
slope = float(getattr(ds, "RescaleSlope", 1.0))
intercept = float(getattr(ds, "RescaleIntercept", 0.0))
print(f"\n la pendiente y la ordenada al origen son: \  n slope={slope}\n intercept={intercept}")
# 2. Lectura de ventanas clínicas opcionales
window_center = getattr(ds, "WindowCenter", None)
print(f"el window center es {window_center}")

# 3. Acceso dinámico a etiquetas mediante variables
atributos_interes = ["PatientID", "Modality", "StudyDate", "SliceThickness"]
datos_extraidos = {tag: getattr(ds, tag, "N/A") for tag in atributos_interes}
print(datos_extraidos)
# %%
# Formato 1: Tupla hexadecimal de dos enteros (Recomendado por claridad)
elem1 = ds[0x0010, 0x0010]
print(f"\n el primer formato es: {elem1}\n")
# Formato 2: Entero único de 32 bits que combina Grupo y Elemento
elem2 = ds[0x00100010]
print(f"el segundo formato es: {elem2}\n")
# Formato 3: Nombre de la Keyword como cadena de texto
elem3 = ds["PatientName"]
print(f"el tercer formato es: {elem3}\n")

# Los tres devuelven exactamente el mismo objeto DataElement
assert elem1 == elem2 == elem3
# %%
element = ds[0x0010, 0x0010]

print(type(element))  # <class 'pydicom.dataelem.DataElement'>
print(element.tag)  # (0010, 0010)
print(element.VR)  # PN
print(element.name)  # Patient's Name
print(element.value)  # DOE^JOHN
print(element.VM)  # Multiplicidad de Valor (Value Multiplicity)
# %%
# 1. Si la etiqueta existe, devuelve el DataElement
elem = ds.get((0x0010, 0x0010))  # Retorna DataElement (0010,0010)
patient_name = elem.value if elem else "Desconocido"

# 2. Si la etiqueta no existe, devuelve el valor por defecto asignado
elem_opcional = ds.get((0x0028, 0x1052), None)
if elem_opcional is None:
  intercept = 0.0
else:
  intercept = float(elem_opcional.value)
# %%
from pydicom.dataelem import DataElement

# 1. Creas el objeto DataElement por separado
elem = DataElement((0x0010, 0x0010), 'PN', 'Anonimizado^Paciente')

# 2. Lo agregas al dataset
ds.add(elem)
print("\n el nuevo paciente es:{ds.PatientName}")  
# %%
slope = getattr(ds, "RescaleSlope", 1.0)
intercept = getattr(ds, "RescaleIntercept", 0.0)
print(f"la pendiente y la ordenada al origen son: \n slope={slope}\n intercept={intercept}")
# %%