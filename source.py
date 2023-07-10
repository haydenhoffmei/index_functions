import rasterio
from rasterio import plot
from rasterio.plot import show_hist
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

def ndvi_func(red,nir):
    """
    parameters
        red (rasterio array): raster of your red band
        nir (rasterio array): raster of your nir band
    """
    ndvi = np.where(
        (nir+red)==0.,
        0,
        (nir-red)/(nir+red)
    )
    return ndvi

def evi_func(red,blue,nir):
    """
    parameters
        red (array): raster of your red band
        blue (array): raster of your red band
        nir (array): raster of your nir band
    """
    evi = np.where(
        (nir+red)==0.,
        0,
        2.5*((nir-red)/(nir+6*red-7.5*blue+1))
    )
    return evi

def savi_func(red,nir):
    """
    parameters
        red (array): raster of your red band
        nir (array): raster of your nir band
    """
    savi = np.where(
        (nir+red)==0.,
        0,
        ((nir-red)/(nir+red+0.5))*(1.5)
    )
    return savi

def gci_func(green,nir):
    """
    parameters
        green (array): raster of your green band
        nir (array): raster of your nir band
    """
    gci = np.where(
        (nir+green)==0.,
        0,
        ((nir/green)-1)
    )
    return gci

def write_raster(raster, directory, sample, name):
    """
    parameters
        raster (array): rasterio array you want to write as a .TIF
        directory (str): file path of where you want the raster to be written to
        sample (str): .TIF with teh crs, height, width, and transformation of the
                raster you want to make
        name (str): the name you want to uniquely identify the raster
    """
    if 'rasterImage.TIF' in os.listdir(directory):
        os.remove(directory+'rasterImage.TIF')
    rasterImage = rasterio.open(
        directory+'rasterImage'+'_'+name+'.TIF',
        'w',
        driver='Gtiff',
        width=sample.width,height=sample.height,
        count=1,
        crs=sample.crs,
        transform=sample.transform,
        dtype='float64'
    )
    rasterImage.write(raster,1)
    rasterImage.close()
    return


if __name__=="__main__":
    # get path
    dirname = input('What is the full directory path you are working in?\n')
    dirlist = os.listdir(dirname)

    # assign variables to band signifiers
    # in this case, band signifiers should be a string unique to the band you're using
    # bandsigs need to be common across all scenes
    bluebandsig = input('What signifies the blue band?\n')
    greenbandsig = input('What signifies the green band?\n')
    redbandsig = input('What signifies the red band?\n')
    nirbandsig = input('What signifies the NIR band?\n')

    # get user index choice
    index = input('What index are you running?\nOptions: ndvi, evi, savi, gci\n')

    # set template to first tif found in directory
    # passed to write_raster func to generate tiff class values
    for i in os.listdir(dirname+dirlist[0]+'/'):
        if '.TIF' in i:
            template = rasterio.open(dirname+dirlist[0]+'/'+i)

    # read in bands based on bandsig
    # if bands are combined, us rasterio.read(x) for bands
    # read astype(float64) to execute array algebra properly
    for i in dirlist:
        for x in os.listdir(dirname+i+'/'):
            if redbandsig in x:
                redBand = rasterio.open(dirname+i+'/'+x).read(1).astype('float64')
            elif nirbandsig in x:
                nirBand = rasterio.open(dirname+i+'/'+x).read(1).astype('float64')
            elif greenbandsig in x:
                greenBand = rasterio.open(dirname+i+'/'+x).read(1).astype('float64')
            elif bluebandsig in x:
                blueBand = rasterio.open(dirname+i+'/'+x).read(1).astype('float64')
        
        # select index function
        if index == 'ndvi':
            image = ndvi_func(redBand,nirBand)
        elif index == 'evi':
            evi_func(redBand,blueBand,nirBand)
        elif index == 'savi':
            image = savi_func(redBand, nirBand)
        elif index == 'gci':
            image = gci_func(greenBand,nirBand)
        
        # write output to tif
        write_raster(image,dirname+i+'/',template,i)

        # open and show output
        rasterImage = rasterio.open(dirname+i+'/rasterImage'+'_'+i+'.TIF') # uses convention determined in write_raster()
        plot.show(rasterImage)
