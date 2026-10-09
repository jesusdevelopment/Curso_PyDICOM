# %%
import os
import pydicom
from pathlib import Path

def inspect_complete_dicom_folder(folder_path: str):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Error: La ruta '{folder_path}' no existe.")
        return

    # Clasificador de archivos por modalidad DICOM
    dicom_data = {
        "CT": [],
        "RTSTRUCT": [],
        "RTPLAN": [],
        "RTDOSE": [],
        "RTIMAGE": [],
        "OTROS": []
    }

    # 1. Escanear toda la carpeta y subcarpetas recursivamente
    for file_path in folder.rglob("*"):
        if file_path.is_file():
            try:
                # Lectura rápida solo de cabeceras (sin cargar píxeles en memoria)
                ds = pydicom.dcmread(file_path, stop_before_pixels=True)
                modality = getattr(ds, "Modality", "OTROS")
                
                if modality in dicom_data:
                    dicom_data[modality].append((file_path, ds))
                else:
                    dicom_data["OTROS"].append((file_path, ds))
            except Exception:
                # Ignorar archivos del sistema que no sean DICOM
                continue

    print("=" * 65)
    print(f"RESUMEN DEL ESTUDIO DICOM-RT: {folder.resolve()}")
    print("=" * 65)

    # 2. Resumen de la Tomografía (CT)
    cts = dicom_data["CT"]
    print(f"\n[CT] IMÁGENES TOMOGRÁFICAS ({len(cts)} cortes detectados)")
    if cts:
        sample_ct = cts[0][1]
        print(f"  • ID Paciente:          {getattr(sample_ct, 'PatientID', 'N/A')}")
        print(f"  • StudyInstanceUID:     {getattr(sample_ct, 'StudyInstanceUID', 'N/A')}")
        print(f"  • SeriesInstanceUID:    {getattr(sample_ct, 'SeriesInstanceUID', 'N/A')}")
        print(f"  • FrameOfReferenceUID: {getattr(sample_ct, 'FrameOfReferenceUID', 'N/A')}")

    # 3. Resumen de Estructuras (RS)
    structs = dicom_data["RTSTRUCT"]
    print(f"\n[RS] RTSTRUCT / ESTRUCTURAS ({len(structs)} archivo(s))")
    for path, ds in structs:
        print(f"  • Archivo: {path.name}")
        print(f"    - SOPInstanceUID: {ds.SOPInstanceUID}")
        if hasattr(ds, "StructureSetROISequence"):
            rois = [roi.ROIName for roi in ds.StructureSetROISequence]
            print(f"    - Estructuras ({len(rois)}): {', '.join(rois)}")

    # 4. Resumen del Plan de Tratamiento (RP)
    plans = dicom_data["RTPLAN"]
    print(f"\n[RP] RTPLAN / PLAN DE TRATAMIENTO ({len(plans)} archivo(s))")
    for path, ds in plans:
        print(f"  • Archivo: {path.name}")
        print(f"    - Nombre/Label: {getattr(ds, 'RTPlanLabel', 'N/A')}")
        print(f"    - SOPInstanceUID: {ds.SOPInstanceUID}")
        if hasattr(ds, "BeamSequence"):
            beams = [f"{b.BeamNumber}:{getattr(b, 'BeamName', 'Haz')}" for b in ds.BeamSequence]
            print(f"    - Campos/Haces ({len(beams)}): {', '.join(beams)}")

    # 5. Resumen de la Matriz de Dosis (RD)
    doses = dicom_data["RTDOSE"]
    print(f"\n[RD] RTDOSE / DISTRIBUCIÓN DE DOSIS ({len(doses)} archivo(s))")
    for path, ds in doses:
        print(f"  • Archivo: {path.name}")
        print(f"    - SOPInstanceUID: {ds.SOPInstanceUID}")
        scaling = float(getattr(ds, "DoseGridScaling", 1.0))
        units = getattr(ds, "DoseUnits", "Gy")
        
        # Leemos los píxeles solo para calcular la dosis máxima
        ds_full = pydicom.dcmread(path)
        if hasattr(ds_full, "pixel_array"):
            max_dose = ds_full.pixel_array.max() * scaling
            print(f"    - Matriz 3D (Z, Y, X): {ds_full.pixel_array.shape}")
            print(f"    - Dosis Máxima:         {max_dose:.2f} {units}")

    # 6. Otras modalidades (RTIMAGE, etc.)
    other_mods = dicom_data["RTIMAGE"] + dicom_data["OTROS"]
    if other_mods:
        print(f"\n[OTROS] OTROS ARCHIVOS DICOM ({len(other_mods)} archivo(s))")
        for path, ds in other_mods:
            print(f"  • Archivo: {path.name} | Modality: {getattr(ds, 'Modality', 'UNKNOWN')}")

# ==========================================
# CÓMO EJECUTARLO:
# ==========================================
# Reemplaza esta variable por la ruta a tu carpeta con los archivos .dcm
RUTA_DE_TU_CARPETA = r"/home/jesusr/imgs/TC-RS-RP-RD/"

inspect_complete_dicom_folder(RUTA_DE_TU_CARPETA)
# %%
