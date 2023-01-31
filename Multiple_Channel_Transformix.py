#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import modules
import numpy
import numpy as np
from pathlib import Path
#import pandas as pd
import tempfile
from tifffile import tifffile
from PIL import Image
import PIL
import sys
import time
import os
import re
from skimage.transform import resize
import imageio


# In[2]:


data_dir=r"C:\Users\nmjs16\Downloads\ImageReg"

# Set the directory containing the moving images that should be transfered
moving_image = "extracted_channels_maskout.tiff"
movingImagePath = os.path.join(data_dir, moving_image)

# set the directory to transform parameter files
transformParameterFiles = [r"C:\Users\nmjs16\Downloads\ImageReg\TransformParameters.0.txt"]

# Set the directory for the output images
outputDirectory = os.path.join(data_dir, "output")

# set target size and padding 
target_size = (326,734)
pad = None


# In[3]:


#Define base component transformix
def RunTransformix(command):
    """To use this, you must be able to call Transformix from your command shell and have your
       parameter text files set before running. (Refer to the Transformix parameter files for
       more information.)
    ----------
    The input parameter 'command' is a string that is sent to the system for running Transformix

    """
    print(str(command))
    print('Running transformix...')
    #Start timer
    start = time.time()
    #Send the command to the shell
    os.system(command)
    #Stop timer
    stop = time.time()
    #Print update
    print('Finished -- computation took '+str(stop-start)+'sec.')
    #Return values
    return command


# In[4]:


def applyMultipleTransforms(movingImagePath: str, outputDirectory: str, transformParameterFiles: str):

    """Applies multiple transform files in sequence to an image"""

    # Ensure the input image is pathlib object
    movingImagePath = Path(movingImagePath)
    # Ensure the input tps are pathlib objects
    transformParameterFiles = [Path(t) for t in transformParameterFiles]
    # Ensure the out directory is a pathlib object
    outputDirectory = Path(outputDirectory)

    # Create transformix command
    command = "transformix"

    # Create a temporary folder within the outputDirectory
    with tempfile.TemporaryDirectory(dir=outputDirectory) as nestedDirectory:
        # Run the first transformation
        tmpCommand = command + ' -out ' + str(nestedDirectory)
        tmpCommand = tmpCommand + ' -tp ' + str(transformCalls[0])
        tmpCommand = tmpCommand + ' -in ' + str(movingImagePath)

        # Apply each transform file in succession using transformix on the image.
        runTransformix(tmpCommand)

        # Determine the output file name for the result of running transformix
        resultName = Path(os.path.join(str(nestedDirectory),"result"+".tif"))

        # Verify if the number of elements in the list is greater than 2 (if not, use only the last element of the list)
        if len(transformCalls) > 1:
            # Iterate through all additional transform parameter files and apply them using transformix
            for t in range(1, len(transformCalls)):
                # Generate the command for executing transformix on the temporary directory.
                tmpCommand = command

                # Check if the current iteration is the final one.
                if t == (len(transformCalls) - 1):
                    # Add the result name
                    tmpCommand = tmpCommand + ' -in ' + str(resultName)
                    # Set the final output directory as the outputDirectory.
                    tmpCommand = tmpCommand + ' -out ' + str(outputDirectory)
                    # Update output image name.
                    resultName = Path(os.path.join(str(nestedDirectory),"result"+".tif"))
                                     
                #Otherwise, leave the output directory as the temporary directory
                else:
                    #Add the result name to the command
                    tmpCommand = tmpCommand + ' -in ' + str(resultName)
                    #Run transformixs
                    tmpCommand = tmpCommand +' -out ' + str(resultName)
                    #Set the output file name for the result of running transformix
                    resultName = Path(os.path.join(str(nestedDirectory),"result"+".tif"))

                #Add the transform parameters
                tmpCommand = tmpCommand + ' -tp ' + str(trans_calls[t])
                #Iterate through each transform parameter file and run transformix
                RunTransformix(tmpCommand)


        else:
            #Just change the results to the output directory
            new_name = Path(os.path.join(str(outputDirectory),"result"+".tif"))
            #Get the resulting image to rename (so we don't overwrite results)
            resultName.rename(new_name)
            #Set back the res name
            resultName = new_name

    #Return the result name
    return resultName


# In[5]:


class Transformix():

    
    def __init__(self, moving_im, out_dir, tps, target_size = None, pad = None, trim = None, crops = None, out_ext = ".tif"):

        #Create pathlib objects and set class parameters
        self.moving_im = Path(moving_im)
        self.in_channels = []
        self.out_channels = []
        self.multichannel = None
        self.out_dir = Path(out_dir)
        self.tps = [Path(t) for t in tps]
        self.command = "transformix"
        self.intermediate = False
        self.out_ext = out_ext
        self.target_size = target_size
        self.pad = pad
        self.trim = trim
        self.crops = crops


        #Load images
        imagef = tifffile.imread(str(self.moving_im))
        
        self._multichannelTransformixArray(imagef)
        
    # Function that applies multiple transform files in sequence to an array of data using the transformix tool.    
    def _multichannelTransformixArray(self, imagef):
        
        #Utilize a context manager to create a temporary directory for channel-wise images
        with tempfile.TemporaryDirectory(dir=self.out_dir) as tmpdirname:
            
            ## Iterate through the channels
            for i in range(imagef.shape[0]):
                
                # Create a filename for a temporary image
                im_name = Path(os.path.join(tmpdirname, self.moving_im.stem + str(i) + ".tif"))
                # Update the list of names for image channels
                self.in_channels.append(im_name)
                # Set a temporary channel to work with throughout the data prep stage
                slice_in = imagef[i,:,:]

                if not im_name.is_file():
                    if self.target_size!=None:
                        slice_in = resize(slice_in,self.target_size)
                    # Create a tif image from this slice
                    channel_image = imagef[i,:,:]
                    channel_image=Image.fromarray((channel_image*255).astype(numpy.uint8))
                    # Save the nifti image
                    channel_image.save(im_name)
                
                #Create a temporary command to be sent to the shell
                tmp_command = self.command + ' -in ' + str(im_name) + ' -out ' + str(tmpdirname)
                #Add full tissue transform paramaeters
                tmp_command = tmp_command + ' -tp ' + str(self.tps[0])
                #Send the command to the shell
                RunTransformix(tmp_command)
                #Set the output file name for the result of running transformix
                resultName = Path(os.path.join(tmpdirname,"result"+".tif"))

                #Create a new name
                new_name = Path(os.path.join(tmpdirname,self.moving_im.stem+str(i)+'_result'+".tif"))
                #Get the resulting image to rename (so we don't overwrite results)
                resultName.rename(new_name)
                self.out_channels.append(new_name)

            image_list = [imageio.imread(path) for path in self.out_channels]            
            full_result = np.concatenate(image_list, axis=0)
            imageio.imwrite("concatenated_image.tif", full_result)

            channels = []
            for path in self.out_channels:
                channel = tifffile.imread(path)
                channels.append(channel) 
            channels = np.array(channels)
            tifffile.imwrite("All_channel_transformed.tiff", channels)


# In[6]:


Transformix(movingImagePath,
            outputDirectory,
            transformParameterFiles,
            target_size,
            pad,
            trim = None,
            crops = None,
            out_ext = ".tif"
            )


# In[ ]:





