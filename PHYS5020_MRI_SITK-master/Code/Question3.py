# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:54:20 2021

@author: siris
"""

<<insert required import statements here>>


def get_intensities(img, mask):
    # 1. Get the 99th percentile and the 1st percentile values in the image within the mask
    roi_values = img[mask == 1]
    perc_99 = np.percentile(roi_values, 99)
    perc_1 = np.percentile(roi_values, 1)
    # 2. Get mean values from voxels with intensities >= 99th percentile
    # HINT: this is output argument 'high'

    # 3. Get mean values from voxels with intensities <= 1st percentile
    # HINT: this is output argument 'low'

    return high, low


def get_percent_image_uniformity(files, slice_num):
    # 1. Read the image and extract the specific slice
    # HINT: you will need to handle 4D and 3D image series differently

    # 2. From the image metadata, number of rows, number of columns, pixel size in x and y

    # 3. Extract the required slice from the image

    # 4. Create a large circular mask

    # 5. Get the highest and lowest mean intensities within this ROI

    # 6. Calculate percentage image uniformity

    return percent_image_uniformity
