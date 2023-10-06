# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 10:42:11 2021
Edited by Erin Wang, Aug 2022
@author: siris
"""
from glob import glob
from os import getcwd
import os
import SimpleITK as sitk
import numpy as np
from os.path import join, basename
import pickle

import common_functions
import Question1
import Question2
import Question3
import Question4
#import Question5

# %%
base_dir = join(getcwd(), "PHYS5020_MRI_SITK-master/Data")
list_folders = glob(join(base_dir, "*"))
print(list_folders)

print("'Data' folders found in", base_dir)
for each_folder in list_folders:
    print(basename(each_folder))

# %% ######## Question 1 #########
print()
print("Question 1:")

# HINT: complete the get_dicom_series function in common_functions.py in Question1.py
for each_folder in list_folders:
    print(basename(each_folder))
    files = common_functions.get_dicom_series(each_folder)
    Question1.get_tags(files)

# %% ######## Question 2 #########
print()
print("Question 2:")

# HINT: complete the functions read_image_series, get_phantom_length,
# get_diameter and get_length in Question2.py

# # Length measurement
series_idx = 3 - 1  # Enter the index of the image series needed for this measurement
slice_idx = 1 - 1  # Enter the index of the slice used for this measurement
file_names = common_functions.get_dicom_series(join(base_dir, list_folders[series_idx]))
length = Question2.get_phantom_length(file_names, slice_idx)
print("Phantom length (mm) = " + str(length) + "\n")
print(file_names)


# Diameter measurement
# -- probs wrong but gives numbers
series_idx = 4 - 1  # Enter the index of the image series needed for this measurement
slice_idx = 2 - 1  # Enter the index of the slice used for this measurement
file_names = common_functions.get_dicom_series(join(base_dir, list_folders[series_idx]))
length = Question2.get_diameter(file_names, slice_idx)
print("Diameter length (X,Y mm) = " + str(length) + "\n")
print(file_names[slice_idx])
# -- END probs wrong but gives numbers

# Diameter measurement
# slice_idx = 1 - 1  # Enter the indices of the slice used for this test
# series_idx = 1 - 1  # ????
# # Enter the list index of the image series needed for this measurement
# for i in series_idx:
#     files = common_functions.get_dicom_series(join(base_dir, list_folders[i]))
#     vertical_diameter, horizontal_diameter = common_functions.get_diameter(
#         files, slice_idx
#     )
#     print("\n" + basename(list_folders[i]))
#     print("\n" + "Vertical diameter (mm) \n")
#     for sl in range(0, len(slice_idx)):
#         print("Slice " + str(slice_idx[sl] + 1) + ":" + str(vertical_diameter[sl]))

#     print("\n" + "Horizontal diameter (mm) \n")
#     for sl in range(0, len(slice_idx)):
#         print("Slice " + str(slice_idx[sl] + 1) + ":" + str(horizontal_diameter[sl]))

# %% ######## Question 3 #########
print()
print("Question 3:")

# HINT: complete functions get_intensities get_percent_image_uniformity in Question3.py

series_idx = 1 - 1  # Enter the indices of the series used for this test
slice_idx = [0,1,2,3,4,5,6,7,8,9,10] # Enter the indices of the slice used for this test

files = common_functions.get_dicom_series(join(base_dir, list_folders[series_idx]))
for i in slice_idx:
    piu = Question3.get_percent_image_uniformity(files, slice_idx[i], 20000) # 200 cm^2 is 20,000 mm^2
    print("\n",files[slice_idx[i]])
    print("\n" + "Percent image uniformity (%) \n")
    print("Slice " + str(slice_idx[i] + 1) + ": " + str(piu))

# %% ######## Question 4 #########
print()
print("Question 4:")

#os.system('clear')

# HINT: complete functions get_te calculate_t2map show_maps in Question4.py

series_idx = 2-1
files = common_functions.get_dicom_series(list_folders[series_idx])


# T2_map_acr, series_reader = common_functions.read_image_series(files2)
# T2_map_acr_imgarr = sitk.GetArrayFromImage(T2_map_acr)

# this thing takes a while so i save it and open

# T2_map_calc = np.squeeze(Question4.calculate_t2map(files))
# with open("data.pkl", "wb") as f:
#     pickle.dump(T2_map_calc, f)
# print(T2_map_calc.shape)
with open("data.pkl", "rb") as f:
   T2_map_calc = pickle.load(f)
print(T2_map_calc.shape)

series_idx = 6-1
files2 = common_functions.get_dicom_series(list_folders[series_idx])


# Display the maps side-by-side in a single figure with appropriate labeling
slice_idx = 1-1  # Choose an image slice to display

#mashiespaghetti -T we are trying to avoid all this 3d 4d stuff and just do a slice

T2_map_acr = sitk.ReadImage(files2[slice_idx])

T2_map_acr_imgarr  = np.squeeze(sitk.GetArrayFromImage(T2_map_acr))

# end spaghetti
print(np.max(T2_map_acr_imgarr))
print(np.max(T2_map_calc))
print(np.size(T2_map_acr_imgarr))
print(np.size(T2_map_calc))

Question4.show_maps(T2_map_acr_imgarr, 'ACR T2 map', T2_map_calc[:,:], 'Calculated T2 map')

mask = common_functions.circular_mask2(T2_map_acr_imgarr[:, :], [80, 80], 5)  # [80, 80], 5
mask.astype(np.int32)

# Get ROI statistics in a circular region
mean, sd, median, iqr = common_functions.get_ROI_stats(T2_map_acr_imgarr[:, :], mask)
print('ACR T2: mean {0} sd {1} median {2} iqr {3}\n'.format(mean, sd, median, iqr))
# print stats

mean, sd, median, iqr = common_functions.get_ROI_stats(T2_map_calc[:, :], mask)
print('Calculated T2: mean {0} sd {1} median {2} iqr {3}\n'.format(mean, sd, median, iqr))
# print stats

# %% ######## Question 5 #########
print()
print("Question 5:")

# HINT: complete functions get_ellipse_ax and get_percentage_ghosting in Question5.py

series_idx = 5-1  # enter the index of the series needed for this measurement
slice_idx = [0,1,2,3,4,5,6,7,8,9,10]  # Enter the index of the slice used for this measurement
#slice_idx =  [6,6,6,6,6,6,6,6,6,6,6]
files = common_functions.get_dicom_series(join(base_dir, list_folders[series_idx]))

for i in slice_idx:
    perc_ghost = Question5.get_percentage_ghosting(files, slice_idx[i], 20000)
    print("\n",files[slice_idx[i]])
    print('\n' +
     'Percent-signal ghosting (%) \n')
    print('Slice ' + str(slice_idx[i] + 1) + ': ' + str(perc_ghost))
