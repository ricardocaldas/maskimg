%load_ext autoreload
%autoreload 2

import cv2
import numpy as np
from matplotlib.image import imsave
from roifile import ImagejRoi
import os
import shutil
import ricardoutils as ru

#Add the directory of raw images, the directory of Rois and the directory to save masks. Raw and Rois should have same name.
raw_dir = "C:\\Users\\ricar\\OneDrive\\UFSC\\Projetos\\data\\ricteste\\raw"
roi_dir = "C:\\Users\\ricar\\OneDrive\\UFSC\\Projetos\\data\\ricteste\\roi"
mask_dir = "C:\\Users\\ricar\\OneDrive\\UFSC\\Projetos\\data\\ricteste\\processed"

ru.create_mask_from_dir(raw_dir, roi_dir, mask_dir) 
