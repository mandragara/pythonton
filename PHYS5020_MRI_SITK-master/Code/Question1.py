# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 18:14:44 2021

@author: siris
"""

import SimpleITK as sitk
import numpy as np


def print_tags(img, tags):
    seq_name = img.GetMetaData(tags[0])
    slice_thickness = str(img.GetMetaData(tags[1]))
    rows = int(img.GetMetaData(tags[2]))
    columns = int(img.GetMetaData(tags[3]))
    pixel_size_x = np.round(float(img.GetMetaData(tags[4]).split('\\')[0]), 3)
    pixel_size_y = np.round(float(img.GetMetaData(tags[4]).split('\\')[1]), 3)
    fov_x = columns * pixel_size_x  # ????????
    fov_y = rows * pixel_size_y  # ????????

    print('Sequence Name: ' + seq_name)
    print('\nSlice Thickness (mm): ' + slice_thickness)
    print('\nMatrix Size: ' + str(rows) + 'x' + str(columns))
    print('\nFOV (mm): ' + str(fov_x) + 'x' + str(fov_y))
    print('\nSpatial resolution (mm x mm): ' + str(pixel_size_x) + 'x' + str(pixel_size_y))


def get_tags(files):
    # Get header information from first file in series
    if len(np.shape(files)) > 1:
        first_file = files[0, 0]
    else:
        first_file = files[0]
    img = sitk.ReadImage(first_file)

    # Get tag values for each file
    # sequence name, slice thickness, rows, columns, pixel spacing
    tags = ['0018|0024', '0018|0050', '0028|0010', '0028|0011', '0028|0030']

    print_tags(img, tags)
    print('\n')
