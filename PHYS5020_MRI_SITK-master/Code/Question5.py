# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 20:53:26 2023

@author: ywan3672
"""

import SimpleITK as sitk
import numpy as np
import common_functions
import matplotlib.image
import matplotlib.pyplot as plt



def get_ellipse_ax(area):
    # Use the formula for area of ellipse using the major and minor ax radii
    # area = pi * major_ax * minor_ax
    # HINT: What is the recommended ratio of major_ax/minor_ax in the ACR manual?

    k = 4 / 1  # major_ax/minor_ax ratio from ACR

    # Solving for minor_ax:
    minor_ax = np.sqrt(area / (np.pi * k))

    # Using the ratio to find major_ax:
    major_ax = k * minor_ax

    return major_ax, minor_ax


def get_ellipse_centres(img, rows, cols):
    # this function can be used as is :)

    image_centre = (int(np.round(rows / 2)), int(np.round(cols / 2)))

    # For each half of the profile, get length from min and max indices of all values along the line that
    # are smaller than the mean

    # left and right
    line_profile = img[image_centre[0], :]
    mean = np.mean(line_profile)

    left_profile = line_profile[: int(len(line_profile) / 2)]
    ind = np.where(left_profile < mean)
    length_in_pixels = np.max(ind) - np.min(ind)
    col_left = 0 + int(np.round(length_in_pixels / 2))
    centre_left = (image_centre[0], col_left)

    right_profile = line_profile[int(len(line_profile) / 2) :]
    ind = np.where(right_profile < mean)
    length_in_pixels = np.max(ind) - np.min(ind)
    col_right = cols - int(np.round(length_in_pixels / 2))
    centre_right = (image_centre[0], col_right)

    # top and bottom
    line_profile = img[:, image_centre[1]]
    mean = np.mean(line_profile)

    bottom_profile = line_profile[int(len(line_profile) / 2) :]
    ind = np.where(bottom_profile < mean)
    length_in_pixels = np.max(ind) - np.min(ind)
    row_bottom = rows - int(np.round(length_in_pixels / 2))
    centre_bottom = (row_bottom, image_centre[1])
    # for top, because there is an indent, assume phantom is centred
    # and use the bottom length to determine position of top ellipse centre
    row_top = 0 + int(np.round(length_in_pixels / 2))
    centre_top = (row_top, image_centre[1])

    return centre_left, centre_right, centre_top, centre_bottom


def get_percentage_ghosting(file_names, slice_num, area):
    # 1. Read the image and extract the specific slice
    # HINT: you will need to handle 4D and 3D image series differently

    img = sitk.ReadImage(file_names[slice_num])
    image_array = np.squeeze(sitk.GetArrayFromImage(img))

    # 2. From the image metadata, number of rows, number of columns, pixel size in x and y

    tags = ["0018|0024", "0018|0050", "0028|0010", "0028|0011", "0028|0030"]
    rows = int(img.GetMetaData(tags[2]))
    columns = int(img.GetMetaData(tags[3]))
    pixel_size_x = np.round(float(img.GetMetaData(tags[4]).split("\\")[0]), 3)
    pixel_size_y = np.round(float(img.GetMetaData(tags[4]).split("\\")[1]), 3)

    # 3. Extract the required slice from the image
    # !!! not implemented

    # 4. Create a large circular mask

    centre = [int(rows / 2), int(columns / 2)]
    radius = np.sqrt((area / (pixel_size_x**2)) / 3.141592)
    mask = common_functions.circular_mask(img, centre, radius)

    # 5. Get the mean image intensities within this ROI

    img_2d = image_array
    mean_intensity_large = img_2d[mask == 1].mean()

    # 6. Define the centres of the 4 (left, right, top, bottom) ellipse ROIs
    # HINT: use a tuple or list to contain x and y locations of the centre

    ellipse_centres = get_ellipse_centres(image_array, rows, columns)
    # ellipse_centres = [[256, 128], [256, 384], [128, 256], [384, 256]]

    print(ellipse_centres)
    # 7. Calculate the lengths of the major and minor axes required
    area = 100 / 4  # 10 cm^2 total split between 4 ROI?
    [major_ax, minor_ax] = get_ellipse_ax(area)
    # print(major_ax,minor_ax)

    # 8. Obtain the 4 ellipse masks
    ellipse_mean_intensities = []
    ellipse_masks = []
    for centre in range(4):
        # print(ellipse_centres[centre][1])
        Y, X = np.ogrid[:columns, :rows]
        if centre <= 1:
            ellipse_mask = ((X - ellipse_centres[centre][0]) ** 2 / major_ax**2) + (
                (Y - ellipse_centres[centre][1]) ** 2 / minor_ax**2
            ) <= radius
        else:
            ellipse_mask = ((X - ellipse_centres[centre][0]) ** 2 / minor_ax**2) + (
                (Y - ellipse_centres[centre][1]) ** 2 / major_ax**2
            ) <= radius

        ellipse_mean_intensities.append(image_array[ellipse_mask == 1].mean())
        ellipse_masks.append(ellipse_mask)


    # 9. Show the ellipse ROIs overlaid on the image
    full_mask = sum(ellipse_masks)
    matplotlib.image.imsave("image" + str(slice_num + 1) + ".png", img_2d,cmap='gray')
    arr=img_2d
    arr[arr > 100] = 100
    matplotlib.image.imsave("mask" + str(slice_num + 1) + ".png", mask+full_mask)
    matplotlib.image.imsave("arr" + str(slice_num + 1) + ".png", arr,cmap='gray')


    # 10. Get the mean image intensities within the 4 ellipse ROIs

    # i do this in 8
    # print(ellipse_mean_intensities)
    #
    # 11. Calculate the percentage ghosting ratio
    perc_ghost = ghosting_ratio = (
        abs(
            (
                (ellipse_mean_intensities[2] + ellipse_mean_intensities[3])
                - (ellipse_mean_intensities[0] + ellipse_mean_intensities[1])
            )
            / (2 * mean_intensity_large)
        )
        * 100
    )

    return perc_ghost
