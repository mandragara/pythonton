# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 10:54:04 2021

@author: siris
"""

<<insert required import statements here>>

def get_length(img, row, col):
    # 1. Get the line profile along a row or a column.
    # HINT: Oblique lines not allowed.

    # 2. Identify indices of all voxels along the line where values are greater than 50% of the mean
    # 3. Calculate length as the difference between the min and max indices (in pixels)

    return length_in_pixels


def get_diameter(files, slice_num):
    # 1. Read in the image series
    # HINT: you will need to handle 4D and 3D series differently

    vertical_diameter = []
    horizontal_diameter = []
    for n in slice_num:
        # 2. Read the image and extract the specific slice

        # 3. From the image metadata, get number of rows, number of columns, pixel size in x and y
        # HINT: getting metadata from an image series is different to a single image file

        # 4. Get the phantom diameter along a line drawn horizontally through the center of the image

        # 5. Get the phantom diameter along a line drawn vertically through the center of the image

        # 6. Convert length in pixels to mm

    return vertical_diameter, horizontal_diameter


def get_phantom_length(files, slice_num):
    # 1. Read the image and extract the specific slice
    # HINT: you will need to handle 4D and 3D image series differently

    # 2. From the image metadata, number of columns, pixel size in x
    # HINT: getting metadata from an image series is different to a single image file

    # 3. Get the phantom length along a line drawn through nearly the center of the image
    # HINT: The best position of the line need not be right at the center of the image

    # 4. Calculate length in mm

    return length
