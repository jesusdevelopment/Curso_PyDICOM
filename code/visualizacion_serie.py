# %%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pydicom


def apply_windowing(
    image_hu: np.ndarray, window_center: float, window_width: float
) -> np.ndarray:
  """Aplica la ventana clínica (WC/WW) y normaliza a uint8 [0, 255]."""
  lower_bound = window_center - (window_width / 2.0)
  upper_bound = window_center + (window_width / 2.0)

  clipped_image = np.clip(image_hu, lower_bound, upper_bound)
  normalized = (clipped_image - lower_bound) / (upper_bound - lower_bound)
  return (normalized * 255.0).astype(np.uint8)


def load_sorted_ct_series(folder_path: str) -> np.ndarray:
  """Carga y ordena espacialmente en Z los 249 cortes DICOM sin importar que no tengan extensión .dcm."""
  folder = Path(folder_path)

  if not folder.exists():
    raise FileNotFoundError(f"La ruta no existe: {folder_path}")

  datasets = []

  # Recorrer todos los archivos independientemente de su nombre o extensión
  for file_path in folder.rglob("*"):
    if file_path.is_file():
      try:
        ds = pydicom.dcmread(file_path)
        # Validar que sea un corte tomográfico con datos de imagen y posición Z
        if "PixelData" in ds and "ImagePositionPatient" in ds:
          datasets.append(ds)
      except Exception:
        continue

  if not datasets:
    raise ValueError(
        f"No se pudieron decodificar archivos DICOM en: {folder_path}"
    )

  # Ordenar de inferior a superior usando la coordenada Z de ImagePositionPatient (0020, 0032)
  datasets.sort(key=lambda x: float(x.ImagePositionPatient[2]))

  # Convertir a matriz 3D en Unidades Hounsfield (HU)
  volume = []
  for ds in datasets:
    arr = ds.pixel_array.astype(np.float32)
    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    volume.append((arr * slope) + intercept)

  return np.stack(volume, axis=0)


def plot_slice_grid(volume_3d: np.ndarray, num_cols: int = 6, step: int = 4):
  """Muestra una cuadrícula con los cortes tomográficos usando ventana de Tejido Blando."""
  slices_to_show = volume_3d[::step]
  num_slices = len(slices_to_show)
  num_rows = int(np.ceil(num_slices / num_cols))

  fig, axes = plt.subplots(num_rows, num_cols, figsize=(14, 2.5 * num_rows))
  axes = axes.flatten()

  for i in range(num_slices):
    img_win = apply_windowing(
        slices_to_show[i], window_center=40, window_width=400
    )
    axes[i].imshow(img_win, cmap="gray")
    axes[i].set_title(f"Corte {i * step}", fontsize=8)
    axes[i].axis("off")

  for j in range(num_slices, len(axes)):
    axes[j].axis("off")

  plt.tight_layout()
  plt.show()


# Cargar el volumen completo de 249 cortes y mostrar cada 4to corte en una cuadrícula de 6 columnas
if __name__ == "__main__":
    volume_3d = load_sorted_ct_series("/home/jesusr/imgs/S2010")
    print(f"Volumen 3D cargado con éxito. Forma del arreglo: {volume_3d.shape}")

    plot_slice_grid(volume_3d, num_cols=6, step=4)
# %%