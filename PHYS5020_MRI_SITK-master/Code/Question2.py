# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 10:54:04 2021

@author: siris
"""

import SimpleITK as sitk
import numpy as np
import common_functions
import matplotlib
from matplotlib import pyplot


def get_length(img, row, col, axis):
    # 1. Get the line profile along a row or a column.
    # HINT: Oblique lines not allowed. (oblique = straight but not horizontal or vert)
    image_array = sitk.GetArrayFromImage(img)
    print("image size: ", np.size(image_array))
    print("full array", image_array)  # full array

    if axis == "row":
        profile = image_array[:, row, :]

    elif axis == "col":
        profile = image_array[:, :, col]

    print("profile", profile)  # image col/row
    print("profile size: ", np.size(profile))

    # 2. Identify indices of all voxels along the line where values are greater than 50% of the mean

    # Calculate the mean value of the profile
    mean_value = np.mean(profile)
    half_of_mean = np.divide(mean_value, 2)
    # half_of_mean = 0
    print("half_of_mean", half_of_mean)

    # Identify indices
    # Get the indices of all voxels with values greater than 50% of the mean
    indexes = [
        index for index in range(len(profile[0])) if profile[0][index] > half_of_mean
    ]

    print("indexes: ", indexes)
    print("num indexes: ", np.size(indexes))

    # 3. Calculate length as the difference between the min and max indices (in pixels)

    indice_delta = np.max(indexes) - np.min(indexes)
    print("indice_delta ", indice_delta)

    length_in_pixels = indice_delta

    return length_in_pixels


def get_diameter(file_names, slice_num):
    # 1. Read in the image series
    # HINT: you will need to handle 4D and 3D series differently

    # !!!! THIS ISNT FINISHED

    vertical_diameter = []
    horizontal_diameter = []
    # for n in slice_num:
    # 2. Read the image and extract the specific slice
    img = sitk.ReadImage(file_names[slice_num])

    # 3. From the image metadata, get number of rows, number of columns, pixel size in x and y
    # HINT: getting metadata from an image series is different to a single image file
    # sequence name, slice thickness, rows, columns, pixel spacing
    tags = ["0018|0024", "0018|0050", "0028|0010", "0028|0011", "0028|0030"]
    rows = int(img.GetMetaData(tags[2]))
    columns = int(img.GetMetaData(tags[3]))
    pixel_size_x = np.round(float(img.GetMetaData(tags[4]).split("\\")[0]), 3)
    pixel_size_y = np.round(float(img.GetMetaData(tags[4]).split("\\")[1]), 3)

    # 4. Get the phantom diameter along a line drawn horizontally through the center of the image
    row_position = int(np.round(np.divide(rows, 2), 0))
    length_in_pixels_row = get_length(img, row_position, 0, "row")

    # 5. Get the phantom diameter along a line drawn vertically through the center of the image
    col_position = int(np.round(np.divide(columns, 2), 0))
    length_in_pixels_col = get_length(img, 0, col_position, "col")

    # 6. Convert length in pixels to mm
    horizontal_diameter = np.multiply(length_in_pixels_row, pixel_size_y)
    vertical_diameter = np.multiply(length_in_pixels_col, pixel_size_x)

    return vertical_diameter, horizontal_diameter


def get_phantom_length(file_names, slice_num):
    # 1. Read the image and extract the specific slice
    # HINT: you will need to handle 4D and 3D image series differently
    img = sitk.ReadImage(file_names[slice_num])

    # 2. From the image metadata, number of columns, pixel size in x
    # HINT: getting metadata from an image series is different to a single image file
    tags = ["0018|0024", "0018|0050", "0028|0010", "0028|0011", "0028|0030"]
    columns = int(img.GetMetaData(tags[3]))
    pixel_size_x = np.round(float(img.GetMetaData(tags[4]).split("\\")[0]), 3)

    # 3. Get the phantom length along a line drawn through nearly the center of the image
    # HINT: The best position of the line need not be right at the center of the image
    largest_length = 0
    itteration = 0
    for attempt in range(16):
        print(columns)
        col_position = int(np.round(np.divide(columns, 2), 0)) - (attempt * 5)
        length_in_pixels = get_length(img, 0, col_position, "col")
        print("length_in_pixels 1")
        print(length_in_pixels)
        if length_in_pixels > largest_length:
            largest_length = length_in_pixels
            itteration = attempt

    length_in_pixels = largest_length
    print("itteration: ", itteration)
    print("length_in_pixels")
    print(length_in_pixels)

    # 4. Calculate length in mm
    print("pixel_size_x")
    print(pixel_size_x)
    length = np.multiply(length_in_pixels, pixel_size_x)

    return length
