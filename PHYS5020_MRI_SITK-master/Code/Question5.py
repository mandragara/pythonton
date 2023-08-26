# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 20:53:26 2023

@author: ywan3672
"""

<<insert required import statements here>>

def get_ellipse_ax(area):
    # Use the formula for area of ellipse using the major and minor ax radii
    # area = pi * major_ax * minor_ax
    # HINT: What is the recommended ratio of major_ax/minor_ax in the ACR manual?
    
    
    
    return major_ax, minor_ax


def get_ellipse_centres(img, rows, cols):
    
    # this function can be used as is :)
    
    image_centre = (int(np.round(rows / 2)), int(np.round(cols / 2)))

    # For each half of the profile, get length from min and max indices of all values along the line that 
    # are smaller than the mean

    # left and right
    line_profile = img[image_centre[0], :]
    mean = np.mean(line_profile)

    left_profile = line_profile[:int(len(line_profile) / 2)]
    ind = np.where(left_profile < mean)
    length_in_pixels = np.max(ind) - np.min(ind)
    col_left = 0 + int(np.round(length_in_pixels / 2))
    centre_left = (image_centre[0], col_left)

    right_profile = line_profile[int(len(line_profile) / 2):]
    ind = np.where(right_profile < mean)
    length_in_pixels = np.max(ind) - np.min(ind)
    col_right = cols - int(np.round(length_in_pixels / 2))
    centre_right = (image_centre[0], col_right)

    # top and bottom
    line_profile = img[:, image_centre[1]]
    mean = np.mean(line_profile)

    bottom_profile = line_profile[int(len(line_profile) / 2):]
    ind = np.where(bottom_profile < mean)
    length_in_pixels = np.max(ind) - np.min(ind)
    row_bottom = rows - int(np.round(length_in_pixels / 2))
    centre_bottom = (row_bottom, image_centre[1])
    # for top, because there is an indent, assume phantom is centred 
    # and use the bottom length to determine position of top ellipse centre
    row_top = 0 + int(np.round(length_in_pixels / 2))
    centre_top = (row_top, image_centre[1])

    return centre_left, centre_right, centre_top, centre_bottom


def get_percentage_ghosting(files, slice_num):
    # 1. Read the image and extract the specific slice
    # HINT: you will need to handle 4D and 3D image series differently

    # 2. From the image metadata, number of rows, number of columns, pixel size in x and y

    # 3. Extract the required slice from the image

    # 4. Create a large circular mask

    # 5. Get the mean image intensities within this ROI

    # 6. Define the centres of the 4 (left, right, top, bottom) ellipse ROIs
    # HINT: use a tuple or list to contain x and y locations of the centre

    # 7. Calculate the lengths of the major and minor axes required

    # 8. Obtain the 4 ellipse masks

    # 9. Show the ellipse ROIs overlaid on the image

    # 10. Get the mean image intensities within the 4 ellipse ROIs

    # 11. Calculate the percentage ghosting ratio

    return perc_ghost
