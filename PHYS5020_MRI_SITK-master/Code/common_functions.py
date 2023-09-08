# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 10:51:37 2021
Edited by Erin Wang, Aug 2022
@author: siris
"""

# To enable conditional logic, set 'DEBUG_THIS_FILE' to True
DEBUG_THIS_FILE = False

from os import listdir
from os.path import join
import numpy as np


def get_dicom_series(folder):
    # 1. Read the file names of the image series using SimpleITK
    # List all files in the folder
    file_list = listdir(folder)
    # Filter files by file extension
    dicom_names = [
        join(folder, file) for file in listdir(folder) if file.endswith(".dcm")
    ]

    if DEBUG_THIS_FILE:
        # Print the list of image file names
        for file in dicom_names:
            print(file)
            
    # 2. Reshape array of file names for 4D series
    if len(dicom_names) > 11:  # for multi-echo T2w
        dicom_names = np.array(dicom_names).reshape(4, 11)
    else:
        dicom_names = np.array(dicom_names)
    return dicom_names


# def read_image_series(files):
#     # 1. Read the image series into a SimpleITK image
#     << insert code here >>
#     return image, reader


# def circular_mask(img, centre, radius):
#     # 1. Obtain the number of rows and columns in the image
#     << insert code here >>
#     Y, X = np.ogrid[:columns, :rows]
#     # 2. Calculate the distance of each grid location (X,Y) from the centre
#     << insert code here >>
#     mask = dist_from_centre <= radius
#     return (mask)


# def ellipse_mask(img, centre, y_ax, x_ax):
#     # 1. Obtain the number of rows and columns in the image
#     << insert code here >>
#     mask = np.zeros_like(img)
#     for y in range(rows):
#         for x in range(columns):
#             # 2. If the location is within the ellipse, assign a value of 1 to the mask
#             <<insert code here>>
#     return mask


# def get_ROI_stats(img, mask):
#     # 1. Calculate the mean, standard deviation, median and inter-quartile range of
#     # voxel values within the mask
#     return mean, sd, median, iqr
