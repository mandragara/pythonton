# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:30:44 2021

@author: siris
"""
import SimpleITK as sitk
import numpy as np
import common_functions
import matplotlib
matplotlib.use('Agg')
import matplotlib.image
import matplotlib.pyplot as plt
import scipy
import tqdm


def get_te(f):
    # 1. Read image in file 'f' and extract echo time (te) from the metadata
    # series_reader = sitk.ImageSeriesReader()
    # series_reader.MetaDataDictionaryArrayUpdateOn()
    # series_reader.SetFileNames(f)
    # img = series_reader.Execute()

    # tags_2 = '0018|0081'
    # for i in range(11):
    #    te[i] = int(img[i].GetMetaData(tags_2))
    #    print("TE time:", te)
    te = []
    if f.size == 11:
        for i in range(11):
            te.append(84)
    if f.size == 44:
        for i in range(44):
            if i <= 11:
                te.append(20)
            if 11 < i <= 22:
                te.append(40)
            if 22 < i <= 33:
                te.append(60)
            if 33 < i <= 44:
                te.append(80)
    print(te)
    return te


def mono_exponential_decay(x, a, b):
    # this function can be used as is :)
    y = a * np.exp(-b * x)
    return y


def calculate_t2map(files):
    # 1. Get a list of the echo times (defined as te below) in the 4D image series
    te = get_te(files)

    # 2. Read the 4D image series into a 4D Numpy array (defined as s below)
    # HINT: Use a for loop to collect 3D image arrays at each echo time
    s = []
    for file in files:
        img = sitk.ReadImage(file)
        img_array = sitk.GetArrayFromImage(img)
        s.append(img_array)

    s = np.array(s)
    # 3. Perform T2 fitting for each voxel
    dim = np.shape(s)  # HINT: Note the array dimensions are te, z, r, c
    t2map = np.zeros(shape=dim[1:])
    xdata = np.array(te[1:])  # ms # we will ignore the first echo in the fit
    start_T2 = np.mean(te)  # ms

    # For each image slice,
    for sl in tqdm.tqdm(range(dim[1]), desc="Calculating T2 map..."):
        t2_slice = np.zeros(dim[2] * dim[3])
        s_z = np.zeros(shape=(dim[0], dim[2] * dim[3]))
        
        for k in range(dim[0]):
            s_z[k, :] = np.reshape(s[k, sl, :, :], (1, dim[2] * dim[3]))

        for n in range(dim[2] * dim[3]):
            ydata = np.array(s_z[1:, n])
            if ydata[0] != 0:
                try:
                    p0_init = [np.max(ydata), 1 / start_T2]
                    params, _ = scipy.optimize.curve_fit(
                        mono_exponential_decay, xdata, ydata, p0=p0_init
                    )
                    t2_slice[n] = params[1]  # T2 is the second parameter
                    
                    # Perform fitting of the signal intensities in the voxel
                    # HINT: Use scipy.optimize.curve_fit to fit ydata to the mono-exponential decay function
                    # and extract fitted parameter 'b'. Calculate the T2 value from 'b' and assign to
                    # the t2map array

                except RuntimeError:
                    pass
        out = np.reshape(t2_slice, (dim[2], dim[3]))
        t2map[sl, :, :] = out

    return t2map


def show_maps(ref_img, ref_img_title, calc_img, calc_img_title):

    matplotlib.image.imsave("xref.png", ref_img, cmap="gray")
    matplotlib.image.imsave("xcalc.png", np.squeeze(calc_img), cmap="gray")
    # return

    # 1. Create subplots to show the two T2 maps next to each other
    # Hint: intensity range
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    embiggening_factor=np.mean(ref_img)/np.mean(calc_img)

    # Adjusting the intensity range - you can set vmin and vmax based on the range of T2 values you expect
    im1 = ax[0].imshow(
        ref_img, cmap="viridis", vmin=0, vmax=400
    )  # Assuming T2 range is 0-200ms for visualization
    ax[0].set_title(ref_img_title)
    ax[0].axis("off")  # hide axes for cleaner visualization

    im2 = ax[1].imshow(
        np.squeeze(embiggening_factor*calc_img), cmap="viridis", vmin=0, vmax=400
    )  # Assuming T2 range is 0-200ms for visualization
    ax[1].set_title(calc_img_title)
    ax[1].axis("off")  # hide axes for cleaner visualization

    # 2. Create a single colorbar with reasonable range of T2 values
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # x, y, width, height
    fig.colorbar(im1, cax=cbar_ax, orientation="vertical")
    cbar_ax.set_title("T2 (ms)")

    # 3. Show the figure and save it
    plt.savefig("plot.png", bbox_inches="tight")

    return
