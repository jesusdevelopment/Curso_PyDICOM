# %%
def values_changes(dicom_path, ImageType=None, SOPClassUID=None, 
                        SOPInstanceUID=None, SeriesInstanceUID=None, 
                        SeriesNumber=None, InstanceNumber=None, 
                        PatientName=None, PatientID=None, 
                        AcquisitionDate=None, AcquisitionTime=None, 
                        StudyDate=None, StudyTime=None, 
                        StudyInstanceUID=None,
                        Modality=None, InstitutionName=None, 
                        Manufacturer=None, SeriesDescription=None, SeriesDate=None, SeriesTime=None , 
                        FrameOfReferenceUID=None, SliceLocation=None, 
                        ):  
    dicom_file = pydicom.dcmread(dicom_path)

    if ImageType:dicom_file.ImageType = ImageType
    if SOPClassUID:dicom_file.SOPClassUID = SOPClassUID
    if SOPInstanceUID:dicom_file.SOPInstanceUID = SOPInstanceUID
    if SeriesInstanceUID:dicom_file.SeriesInstanceUID = SeriesInstanceUID
    if SeriesNumber:dicom_file.SeriesNumber = SeriesNumber
    if InstanceNumber:dicom_file.InstanceNumber = InstanceNumber
    if PatientName:dicom_file.PatientName = PatientName
    if PatientID:dicom_file.PatientID = PatientID
    if AcquisitionDate:dicom_file.AcquisitionDate = AcquisitionDate
    if AcquisitionTime:dicom_file.AcquisitionTime = AcquisitionTime
    if StudyDate:dicom_file.StudyDate = StudyDate
    if StudyTime:dicom_file.StudyTime = StudyTime
    if StudyInstanceUID:dicom_file.StudyInstanceUID = StudyInstanceUID
    if Modality:dicom_file.Modality = Modality
    if InstitutionName:dicom_file.InstitutionName = InstitutionName
    if Manufacturer:dicom_file.Manufacturer = Manufacturer  
    if SeriesDescription:dicom_file.SeriesDescription = SeriesDescription
    if SeriesDate:dicom_file.SeriesDate = SeriesDate
    if SeriesTime:dicom_file.SeriesTime = SeriesTime
    if FrameOfReferenceUID:dicom_file.FrameOfReferenceUID = FrameOfReferenceUID
    if SliceLocation:dicom_file.SliceLocation = SliceLocation
    
    return dicom_file   