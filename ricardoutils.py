import cv2
import numpy as np
from matplotlib.image import imsave
from roifile import ImagejRoi
import os
import shutil
import tempfile

def create_mask_from_roi(image_path, roi_path, output_path=None):
    """ Cria imagem PNG binaria de um ImageJROI"""  
    img = cv2.imread(image_path)
    array = np.empty(img.shape)
    roi = ImagejRoi.fromfile(roi_path)
#    print(roi)
    cv2.fillPoly(array, pts =[roi.coordinates().astype(int)], color=(1,1,1))
    
    if output_path != None:
        imsave(output_path, array)

    return array

def create_mask_from_dir(raw_dir, roi_dir, mask_dir):   
    """ Cria imagem PNG binaria de um ImageJROI de todas as imagens em um diretório
    
    :param raw_dir: The folder were Raw files are located
    :param roi_dir: The folder were ROIs are located (*.ROI or *.ZIP accepted)
    :param mask_dir: The folder to write Mask files
    """   

    with tempfile.TemporaryDirectory(prefix="ricardoutils_") as tmpdir:
        missing = list()
        clean_folder(mask_dir)
        file_list = os.listdir(raw_dir)
        print("Processing...")
        for file in file_list:
            file_name = file.split(".")
            find_roi_file = os.path.join(roi_dir, file_name[0]) + ".roi"
            find_raw_file = os.path.join(raw_dir, file)
            create_mask_name = os.path.join(mask_dir, file_name[0]) + ".png"
            # Creating mask from a single ROI file        
            if os.path.exists(find_roi_file):              
                create_mask_from_roi(find_raw_file, find_roi_file, create_mask_name)
                print(file, "-> OK")
            # Multiple ROIs in a .ZIP file - Unpack all files in tempfolder
            elif os.path.exists(os.path.join(roi_dir, file_name[0]) + ".zip") :
                packed_folder = os.path.join(roi_dir, file_name[0])
                unpacked_folder = os.path.join(tmpdir, file_name[0])
                shutil.unpack_archive(packed_folder + ".zip", unpacked_folder)
                roi_list = os.listdir(unpacked_folder) 
                img = cv2.imread(find_raw_file)
                array = np.empty(img.shape)
                mask = np.empty(img.shape)
                num_roi = 0
                for roi in roi_list:
                    find_roi_file = os.path.join(unpacked_folder, roi)
                    roi2 = ImagejRoi.fromfile(find_roi_file)
                    cv2.fillPoly(array, pts =[roi2.coordinates().astype(int)], color=(1,1,1))
                    num_roi = num_roi + 1
                mask = cv2.bitwise_or(mask, array)
                imsave(create_mask_name, mask)
                print(file, "-> OK -", num_roi, "ROIs")
            # Ckeck for already unpacked files and use then to make files
            else:
                print(file, "-> Fail") 
                missing.append(file)
    print("Done!")
    print("The following Images have missing ROIs:", missing)

        
def clean_folder(folder_path):
    """Remove all files in a given folder
    
    :param folder_path: The folder to be cleaned
    """
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


