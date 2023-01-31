#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import modules
import numpy
import numpy as np
from pathlib import Path
import pandas as pd
import tempfile
from tifffile import tifffile
from PIL import Image
import PIL
import sys
import time
import os
import re
import matplotlib.pyplot as plt


# In[2]:


# Set the directory containing the registration parameter files
param_dir = r"C:\Users\nmjs16\Downloads\ImageReg"

# Set the names of the parameter files
affine_pars = "affine.txt"
nonlinear_pars = "nonlinear.txt"

# Construct the full path to each parameter file using the directory and file name
affine_pars_path = os.path.join(param_dir, affine_pars)
nonlinear_pars_path = os.path.join(param_dir, nonlinear_pars)

# Create a list of parameter file paths
param_files = [nonlinear_pars_path]


# In[3]:


# Set the directory containing the processed imaging data
data_dir = r"C:\Users\nmjs16\Downloads\ImageReg"

# Set the names of the fixed and moving images
fixed_image = "ResultSLIDE5-gs.tif"
#moving_image = "extracted_channels_maskout.tiff"
moving_image = "All_channel_transformed.tiff"
#moving_image = "channel9.tif"

# Construct the full path to each image file using the directory and file name
path_to_fixed = os.path.join(data_dir, fixed_image)
path_to_moving = os.path.join(data_dir, moving_image)

# Set the directory for the output images
output_dir = os.path.join(data_dir, "output")


# In[4]:


def RunElastix(command):
    """
    To use this, you must be able to call Elastix from your command shell and have your
    parameter text files set before running. (Refer to the Elastix parameter files for
    more information.)

    The input parameter 'command' is a string that is sent to the system for running Elastix
    (refer to the Elastix command line implementation for more information). The function
    returns the command that was executed as a string
    
    """
    print("Command: ", command)
    print("Running Elastix...")
    start_time = time.time()
    os.system(command)
    end_time = time.time()
    print("Elastix completed in {:.2f} seconds.".format(end_time - start_time))
    return command


# In[5]:


class Elastix():
    
    def __init__(self, fixed: str, moving: str, output_dir: str, p: list, fp: str = None,
                 mp: str = None, fMask: str = None):
    
        """
        This is the Elastix image registration class, which has the following parameters:

        'fixed' which is the path to the fixed (reference) image

        'moving' which is the path to the moving image (image to be transformed)

        'output_dir' which is the path to the output directory

        'p' which is a list of paths to Elastix image registration parameter files in the
        order they should be applied

        'fp' which is the path to fixed image landmark points for manual guidance
        registration

        'mp' which is the path to moving image landmark points for manual guidance
        registration

        'fMask' which is the path to fixed image mask that defines the region on the image
        to draw samples from during registration.

        """

        #Create pathlib objects and set class parameters
        self.fixed = Path(fixed)
        self.fixed_channels = []
        self.moving_channels = []
        self.multichannel = None
        self.moving = Path(moving)
        self.out_dir = Path(output_dir)
        self.temp_dir = None
        self.p = [Path(par_file) for par_file in p]
        self.fp = None if fp is None else Path(fp)
        self.mp = None if mp is None else Path(fp)
        self.fMask = None if fMask is None else Path(fMask)
        self.command = "elastix" 

        print('Loading images...')
        # Load images
        imagef = tifffile.imread(str(self.fixed))
        #imagef = np.array(imagef, dtype='uint8')
        #imagef = Image.fromarray(imagef)
        
        imagefm = tifffile.imread(self.moving)
        #imagefm = np.array(imagefm, dtype='uint8')
        #imagefm = Image.fromarray(imagefm)
        # Print update
        print('Done loading')

        # Add the parameter files to the command
        self.command = self.command + ' '.join([" -p " + str(self.p[par_file]) for par_file in range(len(self.p))])

        # Check that the registration includes both a fixed and moving set of corresponding points
        if self.fp and self.mp is not None:
            # Include corresponding points in the command.
            self.command = self.command + " -fp " + str(self.fp) + " -mp " + str(self.mp)

        # Check for fixed mask
        if fMask is not None:
            # Add the fixed mask to the command if it exists
            self.command = self.command + " -fMask " + str(fMask)

        # Add the output directory to the command
        self.command = self.command + " -out " + str(self.out_dir)

        if imagefm.ndim==2:
            
            
            with tempfile.TemporaryDirectory(dir=self.out_dir) as tmpdirname:
                print(f"Created temporary directory {tmpdirname}")
                print("Exporting single channel images for multichannel input...")
                # Read the images
                imagef = tifffile.imread(str(self.fixed))
                #imagef = np.array(imagef, dtype='uint8')
                #niiFixed = Image.fromarray(imagef) 
                imagefm = tifffile.imread(self.moving)
                #imagefm = np.array(imagefm, dtype='uint8')
                #niiMoving = Image.fromarray(imagefm)
                self.multichannel = True
                
                #fname = Path(os.path.join(tmpdirname, f"{self.fixed.stem}_channel{0}{self.fixed.suffix}"))
                fname = Path(os.path.join(tmpdirname, f"{self.fixed.stem}_channel{0}.jpg"))
                self.fixed_channels.append(fname)
                self.command += f" -f{0} {fname}"
                channel_image = imagef
                channel_image = Image.fromarray((channel_image*255).astype(numpy.uint8))
                #channel_image = Image.fromarray(numpy.uint8(channel_image))
                channel_image.save(fname)
                
                
                #mname = Path(os.path.join(tmpdirname, f"{self.moving.stem}_channel{0}{self.moving.suffix}"))
                mname = Path(os.path.join(tmpdirname, f"{self.moving.stem}_channel{0}.jpg"))
                self.moving_channels.append(mname)
                self.command += f" -m{0} {mname}"
                
                channel_image = imagefm
                #channel_image = Image.fromarray(numpy.uint8(channel_image))
                channel_image = Image.fromarray((channel_image*255).astype(numpy.uint8))
                channel_image.save(mname) 
                print('javad is runinng')


                # Run the command using the function created
                RunElastix(self.command)  

        else:
            # Use a context manager to create a temporary directory for storing channel-wise images.
            with tempfile.TemporaryDirectory(dir=self.out_dir) as tmpdirname:
                print(f"Created temporary directory {tmpdirname}")
                print("Exporting single channel images for multichannel input...")
                # Read the images
                imagef = tifffile.imread(str(self.fixed))
                #imagef = np.array(imagef, dtype='uint8')
                #niiFixed = Image.fromarray(imagef) 
                imagefm = tifffile.imread(self.moving)
                #imagefm = np.array(imagefm, dtype='uint8')
                #niiMoving = Image.fromarray(imagefm)
                self.multichannel = True

                #Export single channel images for each channel of fixed image
                for i in range(imagefm.shape[0]):
                    # Create a filename for each channel of the fixed image
                    fname = Path(os.path.join(tmpdirname, f"{self.fixed.stem}_channel{i}.jpg"))
                    
                    self.fixed_channels.append(fname)
                    self.command += f" -f{i} {fname}"
                    print (fname)

                    # Check if the file already exists, if not, save the channel as an image
                    if not fname.is_file():
                        #channel_image = imagef[:,:]
                        channel_image = imagef[:,:]
                        #channel_image = Image.fromarray(numpy.uint8(channel_image))
                        channel_image = Image.fromarray((channel_image*255).astype(numpy.uint8))
                        channel_image.save(fname)

                for i in range(imagefm.shape[0]):
                    # Create a filename for each channel of the moving image
                    mname = Path(os.path.join(tmpdirname, f"{self.moving.stem}_channel{i}.jpg"))
                   # mname = Path(os.path.join(tmpdirname,str(self.moving.stem+str(i)+self.moving.suffix)))
                    self.moving_channels.append(mname)
                    self.command += f" -m{i} {mname}"
                    print(mname)

                    # Check if the file already exists, if not, save the channel as an image
                    if not mname.is_file():
                        channel_image = imagefm[i,:,:]
                        #channel_image = Image.fromarray(numpy.uint8(channel_image))
                        channel_image = Image.fromarray((channel_image*255).astype(numpy.uint8))
                        channel_image.save(mname)   

# Run the command using the function created
                RunElastix(self.command)



# In[6]:


Elastix(path_to_fixed,
                path_to_moving,
                output_dir,
                param_files,
                fp=None,
                mp=None,
                fMask=None
                )


# In[ ]:




