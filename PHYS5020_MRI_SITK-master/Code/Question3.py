# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:54:20 2021

@author: siris
"""


import SimpleITK as sitk
import numpy as np
import common_functions
import matplotlib.image


def get_intensities(img, mask):
    # 1. Get the 99th percentile and the 1st percentile values in the image within the mask
    img_2d = np.squeeze(img)
    roi_values = img_2d[mask == 1]
    perc_99 = np.percentile(roi_values, 99)
    perc_1 = np.percentile(roi_values, 1)
    # 2. Get mean values from voxels with intensities >= 99th percentile
    # HINT: this is output argument 'high'
    high = roi_values[roi_values >= perc_99].mean()

    matplotlib.image.imsave("name.png", img_2d * mask)
    # 3. Get mean values from voxels with intensities <= 1st percentile
    # HINT: this is output argument 'low'
    low = roi_values[roi_values <= perc_1].mean()

    return high, low


def get_percent_image_uniformity(file_names, slice_num, area):
    # 1. Read the image and extract the specific slice
    # HINT: you will need to handle 4D and 3D image series differently
    img = sitk.ReadImage(file_names[slice_num])
    image_array = sitk.GetArrayFromImage(img)

    tags_2 = ["0018|0087"]
    field = int(img.GetMetaData(tags_2[0]))
    print("field strength is", field)

    # 2. From the image metadata, number of rows, number of columns, pixel size in x and y
    tags = ["0018|0024", "0018|0050", "0028|0010", "0028|0011", "0028|0030"]
    rows = int(img.GetMetaData(tags[2]))
    columns = int(img.GetMetaData(tags[3]))
    pixel_size_x = np.round(float(img.GetMetaData(tags[4]).split("\\")[0]), 3)
    pixel_size_y = np.round(float(img.GetMetaData(tags[4]).split("\\")[1]), 3)

    # 3. Extract the required slice from the image

    # 4. Create a large circular mask
    centre = [int(rows / 2), int(columns / 2)]
    radius = np.sqrt((area / (pixel_size_x**2)) / 3.141592)
    mask = common_functions.circular_mask(img, centre, radius) * 1

    # 5. Get the highest and lowest mean intensities within this ROI

    [high, low] = get_intensities(image_array, mask)

    # 6. Calculate percentage image uniformity
    percent_image_uniformity = (1 - ((high - low) / (high + low))) * 100

    return percent_image_uniformity
