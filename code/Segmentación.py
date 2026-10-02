# %%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pydicom


def load_sorted_ct_series(folder_path: str) -> np.ndarray:
  """Carga y ordena espacialmente en Z la serie tomográfica en Unidades Hounsfield."""
  folder = Path(folder_path)

  if not folder.exists():
    raise FileNotFoundError(f"La ruta no existe: {folder_path}")

  datasets = []
  for file_path in folder.rglob("*"):
    if file_path.is_file():
      try:
        ds = pydicom.dcmread(file_path)
        if "PixelData" in ds and "ImagePositionPatient" in ds:
          datasets.append(ds)
      except Exception:
        continue

  if not datasets:
    raise ValueError(
        f"No se encontraron archivos DICOM válidos en: {folder_path}"
    )

  # Ordenar cortes por coordenada Z
  datasets.sort(key=lambda x: float(x.ImagePositionPatient[2]))

  # Convertir a volumen 3D en HU
  volume = []
  for ds in datasets:
    arr = ds.pixel_array.astype(np.float32)
    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    volume.append((arr * slope) + intercept)

  return np.stack(volume, axis=0)


def apply_windowing(
    image_hu: np.ndarray, window_center: float, window_width: float
) -> np.ndarray:
  """Aplica la ventana clínica (WC/WW) y normaliza a uint8 [0, 255]."""
  lower_bound = window_center - (window_width / 2.0)
  upper_bound = window_center + (window_width / 2.0)

  clipped_image = np.clip(image_hu, lower_bound, upper_bound)
  normalized = (clipped_image - lower_bound) / (upper_bound - lower_bound)
  return (normalized * 255.0).astype(np.uint8)


def plot_dicom_with_mask(
    image_hu: np.ndarray,
    mask: np.ndarray,
    wc: float = 40,
    ww: float = 400,
    alpha: float = 0.4,
):
  """Superpone una máscara de segmentación en color rojo sobre la imagen anatómica de fondo."""
  bg_image = apply_windowing(image_hu, window_center=wc, window_width=ww)

  # Crear máscara RGBA con canal rojo activo
  mask_rgba = np.zeros((mask.shape[0], mask.shape[1], 4), dtype=np.float32)
  mask_rgba[..., 0] = 1.0  # Canal Rojo
  mask_rgba[..., 3] = np.where(mask > 0, alpha, 0.0)  # Canal Alfa (Transparencia)

  fig, ax = plt.subplots(figsize=(7, 7))
  ax.imshow(bg_image, cmap="gray")
  ax.imshow(mask_rgba)  # Superposición
  ax.set_title("Anatomía con Contorno Superpuesto")
  ax.axis("off")
  plt.show()


# ==============================================================================
# FLUJO DE EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
  # 1. Cargar el volumen tomográfico en memoria
  dicom_folder = "/home/jesusr/imgs/S2010"
  volume_3d = load_sorted_ct_series(dicom_folder)

  # 2. Generar la máscara booleana (Tejido hiperdenso / Hueso > 250 HU)
  mask = volume_3d > 250.0

  # 3. Visualizar el corte seleccionado con la máscara superpuesta
  slice_idx = 20
  plot_dicom_with_mask(
      image_hu=volume_3d[slice_idx],
      mask=mask[slice_idx],
      wc=40,
      ww=400,
      alpha=0.4,
  )
