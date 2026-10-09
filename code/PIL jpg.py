# %%
import numpy as np
import pydicom
from PIL import Image


def dicom_to_pil(
    ds: pydicom.Dataset, window_center: float = 40, window_width: float = 400) -> Image.Image:
  """Convierte un Dataset de pydicom a un objeto Image de PIL aplicando ventaneo."""
  # 1. Extracción y reescalado HU
  pixels = ds.pixel_array.astype(np.float32)
  slope = float(getattr(ds, "RescaleSlope", 1.0))
  intercept = float(getattr(ds, "RescaleIntercept", 0.0))
  hu_array = (pixels * slope) + intercept

  # 2. Manejo de polaridad MONOCHROME1
  if getattr(ds, "PhotometricInterpretation", "") == "MONOCHROME1":
    hu_array = np.max(hu_array) - hu_array

  # 3. Ventaneo
  lower = window_center - (window_width / 2.0)
  upper = window_center + (window_width / 2.0)
  clipped = np.clip(hu_array, lower, upper)

  # 4. Normalización a [0, 255] de tipo uint8
  normalized = (clipped - lower) / (upper - lower)
  uint8_array = (normalized * 255.0).astype(np.uint8)

  # 5. Crear objeto PIL (Modo 'L' = Grayscale 8-bit)
  return Image.fromarray(uint8_array, mode="L")


# Ejemplo de guardado
ds = pydicom.dcmread("/home/jesusr/imgs/I90")
img_pil = dicom_to_pil(ds, window_center=40, window_width=400)

# Guardar en diferentes formatos
img_pil.save("/home/jesusr/imgs/corte1.png")  # Sin pérdida
img_pil.save("/home/jesusr/imgs/corte2.jpg", quality=95)  # Con compresión JPEG
# %%