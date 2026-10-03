# %%
import matplotlib.pyplot as plt
import numpy as np
import pydicom


def apply_windowing(
    image_hu: np.ndarray, window_center: float, window_width: float) -> np.ndarray:
  """Aplica una ventana clínica (WC/WW) a una matriz en Unidades Hounsfield

  y la normaliza al rango [0, 255] de tipo uint8.
  """
  lower_bound = window_center - (window_width / 2.0)
  upper_bound = window_center + (window_width / 2.0)

  # Acotar la matriz entre los límites de la ventana
  clipped_image = np.clip(image_hu, lower_bound, upper_bound)

  # Normalizar linealmente a [0, 255]
  normalized = (clipped_image - lower_bound) / (upper_bound - lower_bound)
  uint8_image = (normalized * 255.0).astype(np.uint8)

  return uint8_image


def visualize_dicom(
    dcm_path: str,
    window_center: float = None,
    window_width: float = None,
    cmap: str = "gray",):
  """Lee un archivo DICOM, procesa la escala de grises y lo despliega con Matplotlib."""
  ds = pydicom.dcmread(dcm_path)

  # 1. Extracción y casting
  pixel_array = ds.pixel_array.astype(np.float32)

  # 2. Manejo de MONOCHROME1
  if getattr(ds, "PhotometricInterpretation", "") == "MONOCHROME1":
    pixel_array = np.max(pixel_array) - pixel_array

  # 3. Conversión a HU
  slope = float(getattr(ds, "RescaleSlope", 1.0))
  intercept = float(getattr(ds, "RescaleIntercept", 0.0))
  hu_array = (pixel_array * slope) + intercept

  # 4. Determinación de WC/WW (usar metadatos del archivo si no se especifican)
  if window_center is None or window_width is None:
    if "WindowCenter" in ds and "WindowWidth" in ds:
      # Manejar casos donde WC/WW vienen como listas de múltiples valores
      wc = ds.WindowCenter
      ww = ds.WindowWidth
      window_center = (
          float(wc[0]) if isinstance(wc, pydicom.multival.MultiValue) else float(wc)
      )
      window_width = (
          float(ww[0]) if isinstance(ww, pydicom.multival.MultiValue) else float(ww)
      )
    else:
      # Si no hay metadatos de ventana, usar min/max reales de la imagen
      window_center = float(np.mean(hu_array))
      window_width = float(np.max(hu_array) - np.min(hu_array))

  # 5. Aplicar ventana
  final_image = apply_windowing(hu_array, window_center, window_width)

  # 6. Despliegue gráfico
  plt.figure(figsize=(7, 7))
  plt.imshow(final_image, cmap=cmap)
  plt.title(f"WC: {window_center} | WW: {window_width}")
  plt.axis("off")
  plt.tight_layout()
  plt.show()

  return final_image
# %%
if __name__ == "__main__":
    visualize_dicom("/home/jesusr/Cursos_Deep_Learning/Curso_PyDICOM/imgs/I720", window_center=0, window_width=400)   
# %%
