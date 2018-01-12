#!/usr/env python

import sys, os, string

import astropy
from astropy.io import fits
import numpy as np
#import pyfits
import scipy
from scipy import ndimage
from pyraf import iraf
from iraf import images,imgeom,blkrep,imutil,imcopy


#imagen=sys.argv[1]

def arma_soar(imagen_proc,out_name):
    
    """creates a single image for SOAR SAMI
    It add to the file the exposure time
    and the filter. It also copies the header
    of the PRIMARY extenssion."""
    
    output_tmp=imagen_proc[:-5]+'_tmp.fits'
    iraf.blkrep(input=imagen_proc+'[1]',output=output_tmp,b1=2,b2=2)
    iraf.imcopy(input=imagen_proc+'[1]',output=output_tmp+'[1:1024,1:1028]',verbose='yes')
    iraf.imcopy(input=imagen_proc+'[2]',output=output_tmp+'[1025:2048,1:1028]',verbose='yes')
    iraf.imcopy(input=imagen_proc+'[3]',output=output_tmp+'[1:1024,1029:2056]',verbose='yes')
    iraf.imcopy(input=imagen_proc+'[4]',output=output_tmp+'[1025:2048,1029:2056]',verbose='yes')
    iraf.imcopy(input=output_tmp,output=out_name,verbose='yes')
    
    iraf.imutil.imdelete(output_tmp)
    
    return




files= [imagen for imagen in os.listdir('.') if os.path.isfile(imagen)]
for imagen in files:
    if imagen.endswith(('proc.fits')):
        if imagen.startswith(('soar')):



            hdu=fits.open(imagen)
            FILTRO=hdu[0].header['FILTER1'].split()[1]
            NAME=hdu[0].header['OBJECT']
            EXPT=hdu[0].header['EXPTIME']
            print str(NAME)+str(FILTRO)+str(EXPT)+'s'+imagen[12:-5]
            NEW_NAME=str(NAME)+str(FILTRO)+str(EXPT)+'s'+imagen[12:-10]
            print NEW_NAME

            arma_soar(imagen,NEW_NAME)
        
           
