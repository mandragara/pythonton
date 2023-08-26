# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 10:42:11 2021
Edited by Erin Wang, Aug 2022
@author: siris
"""

from glob import glob
from os import getcwd
from os.path import join, basename

<<insert required import statements here >>

# %%
base_dir = join(getcwd(), 'Data')
list_folders = glob(join(base_dir, '*'))

for each_folder in list_folders:
    print(basename(each_folder))

# %% ######## Question 1 #########
# HINT: complete the get_dicom_series function in common_functions.py in Question1.py
for each_folder in list_folders:
    files = get_dicom_series(each_folder)
    get_tags(files)

# %% ######## Question 2 #########

# HINT: complete the functions read_image_series, get_phantom_length,
# get_diameter and get_length in Question2.py

# Length measurement
series_idx = ???? # Enter the index of the image series needed for this measurement
slice_idx = ???? # Enter the index of the slice used for this measurement
files = get_dicom_series(join(base_dir, list_folders[series_idx]))
length = get_phantom_length(files, slice_idx)
print('Phantom length (mm) = ' + str(length) + '\n')

# Diameter measurement
slice_idx = ????  # Enter the indices of the slice used for this test
series_idx = ????  # ????
# Enter the list index of the image series needed for this measurement
for i in series_idx:
    files = get_dicom_series(join(base_dir, list_folders[i]))
    vertical_diameter, horizontal_diameter = get_diameter(files, slice_idx)
    print('\n' + basename(list_folders[i]))
    print('\n' + 'Vertical diameter (mm) \n')
    for sl in range(0, len(slice_idx)):
        print('Slice ' + str(slice_idx[sl] + 1) + ':' + str(vertical_diameter[sl]))

    print('\n' + 'Horizontal diameter (mm) \n')
    for sl in range(0, len(slice_idx)):
        print('Slice ' + str(slice_idx[sl] + 1) + ':' + str(horizontal_diameter[sl]))

# %% ######## Question 3 #########

# HINT: complete functions get_intensities get_percent_image_uniformity in Question3.py

slice_idx = ????  # Enter the indices of the slice used for this test
series_idx = ????  # Enter the indices of the series used for this test
for i in series_idx:
    files = get_dicom_series(list_folders[i])
    piu = get_percent_image_uniformity(files, slice_idx)
    print('\n' + str(basename(list_folders[i])))
    print('\n' + 'Percent image uniformity (%) \n')
    print('Slice ' + str(slice_idx + 1) + ': ' + str(piu))

# %% ######## Question 4 #########

# HINT: complete functions get_te calculate_t2map show_maps in Question4.py

series_idx = ????
files = get_dicom_series(list_folders[series_idx])
T2_map_calc = calculate_t2map(files)

series_idx = ????
files = get_dicom_series(list_folders[series_idx])
T2_map_acr, series_reader = read_image_series(files)
T2_map_acr_imgarr = sitk.GetArrayFromImage(T2_map_acr)

# Display the maps side-by-side in a single figure with appropriate labeling
slice_idx = ????  # Choose an image slice to display
show_maps(T2_map_acr_imgarr[slice_idx, :, :], 'ACR T2 map', T2_map_calc[slice_idx, :, :], 'Calculated T2 map')

mask = circular_mask(T2_map_acr_imgarr[slice_idx, :, :], [128, 128], 10)  # [80, 80], 5
mask.astype(np.int32)

# Get ROI statistics in a circular region
mean, sd, median, iqr = get_ROI_stats(T2_map_acr_imgarr[slice_idx, :, :], mask)
print('ACR T2: mean {0} sd {1} median {2} iqr {3}\n'.format(mean, sd, median, iqr))
# print stats
mean, sd, median, iqr = get_ROI_stats(T2_map_calc[slice_idx, :, :], mask)
print('Calculated T2: mean {0} sd {1} median {2} iqr {3}\n'.format(mean, sd, median, iqr))
# print stats

# %% ######## Question 5 #########

# HINT: complete functions get_ellipse_ax and get_percentage_ghosting in Question5.py

series_idx = ????  # enter the index of the series needed for this measurement
slice_idx = ????  # Enter the index of the slice used for this measurement

for i in series_idx:
    files = get_dicom_series(list_folders[i])
    perc_ghost = get_percentage_ghosting(files, slice_idx)

    print('\n' + str(basename(list_folders[i])))
    print('\n' + 'Percent-signal ghosting (%) \n')
    print('Slice ' + str(slice_idx + 1) + ': ' + str(perc_ghost))
