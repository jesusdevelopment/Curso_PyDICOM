#%%
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import pydicom
import SimpleITK as sitk
from rt_utils import RTStructBuilder

source_dir = "/home/jesusr/imgs/TC-RS-RP-RD"
ct_only_dir = "/home/jesusr/imgs/CT_only"

# 1. Crear carpeta limpia para cortes CT
os.makedirs(ct_only_dir, exist_ok=True)

# 2. Copiar únicamente los archivos con Modality == 'CT'
for filename in os.listdir(source_dir):
  filepath = os.path.join(source_dir, filename)
  if os.path.isdir(filepath):
    continue
  try:
    ds_check = pydicom.dcmread(filepath, stop_before_pixels=True)
    if getattr(ds_check, "Modality", "") == "CT":
      shutil.copy(filepath, ct_only_dir)
  except Exception:
    continue

# 3. Cargar el volumen CT 3D completo con SimpleITK (Obtiene matriz Z, Y, X)
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(ct_only_dir)
reader.SetFileNames(dicom_names)
ct_image = reader.Execute()

# Convertir a arreglo NumPy con valores en Unidades Hounsfield (HU)
ct_volume = sitk.GetArrayFromImage(ct_image)  # Forma: (Z, Y, X)

# 4. Extraer la máscara con rt_utils
rtstruct = RTStructBuilder.create_from(
    dicom_series_path=ct_only_dir,
    rt_struct_path="/home/jesusr/imgs/TC-RS-RP-RD/RS.202600489.CT_2.dcm",
)

mask_raw = rtstruct.get_roi_mask_by_name("PTVTOTAL")  # Forma: (Y, X, Z)

# Reordenar ejes de la máscara de (Y, X, Z) a (Z, Y, X) para alinear con ct_volume
mask_3d = np.transpose(mask_raw, (2, 0, 1))

print(f"Forma del volumen CT (Z, Y, X): {ct_volume.shape}")
print(f"Forma de la máscara 3D (Z, Y, X): {mask_3d.shape}")

# 5. Visualización del Slice
slice_idx = 80  # Índice del corte a visualizar

plt.figure(figsize=(12, 5))

# Subplot 1: Imagen CT en escala de grises (Ventana de tejidos blandos: WC=40, WW=400)
plt.subplot(1, 2, 1)
plt.imshow(
    ct_volume[slice_idx], cmap="gray", vmin=40 - (400 / 2), vmax=40 + (400 / 2)
)
plt.title(f"Imagen CT - Slice {slice_idx}")
plt.axis("off")

# Subplot 2: Máscara superpuesta en rojo sobre el CT
plt.subplot(1, 2, 2)
plt.imshow(
    ct_volume[slice_idx], cmap="gray", vmin=40 - (400 / 2), vmax=40 + (400 / 2)
)

# Ocultar los píxeles False (0) para que el fondo sea transparente
mask_slice = mask_3d[slice_idx]
masked_overlay = np.ma.masked_where(~mask_slice, mask_slice)

plt.imshow(masked_overlay, cmap="autumn", alpha=0.5)
plt.title(f"PTVTOTAL sobre CT - Slice {slice_idx}")
plt.axis("off")

plt.tight_layout()
plt.show()
# %%
