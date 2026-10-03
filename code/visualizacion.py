#%%
import pydicom
import numpy as np
from PIL import Image

def normalize_visualize_dicom_2(dcm_file, max_v=None, min_v=None, show=True):
    dicom_file = pydicom.dcmread(dcm_file)
    dicom_array = dicom_file.pixel_array.astype(np.float32)

    if max_v: hounsfield_max = max_v
    else: hounsfield_max = np.max(dicom_array)

    if min_v: hounsfield_min = min_v
    else: hounsfield_min = np.min(dicom_array)

    dicom_array[dicom_array < hounsfield_min] = hounsfield_min
    dicom_array[dicom_array > hounsfield_max] = hounsfield_max
    
    hounsfield_range = hounsfield_max - hounsfield_min
    normalized_array = ((dicom_array - hounsfield_min) / hounsfield_range) * 255
    uint8_image = np.uint8(normalized_array)

    if show:
        pillow_image = Image.fromarray(uint8_image)
        pillow_image.show()

    return uint8_image

# Llamada a la función (celda inferior en la captura)
image_2 = normalize_visualize_dicom_2('/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/I720', show=True, max_v=0, min_v=-0)