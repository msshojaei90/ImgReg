#!/usr/bin/env python
# coding: utf-8

# In[58]:


import tifffile
import numpy as np
import cv2
from PIL import Image


# In[59]:


import tifffile

# Load the mask image
mask = tifffile.imread("Mask.tif")

# Divide each pixel value by 255 to convert the range to 0-1
mask = mask / 255
mask = np.array(mask, dtype='float32')


# In[65]:


# Read the TIFF file
im = tifffile.imread("Leap009_010_011_004.tiff")

# Prompt the user to specify the indexes of the channels to extract
channel_indexes = input("Enter the indexes of the channels you want to extract separated by commas: ")
channel_indexes = channel_indexes.split(",")
channel_indexes = [int(x) for x in channel_indexes]


# In[66]:


# Initialize an empty list to store the extracted channels
channels = []

# Iterate through the specified channels
for i in channel_indexes:
    # Extract the specified channel from the TIFF file
    channel = im[i,:,:]
    channel = channel * mask

    # Append the extracted channel to the list of channels
    channels.append(channel)

    
channels=np.array(channels)
# Concatenate the extracted channels along the 3rd axis to create a new TIFF stac


# In[67]:


# Save the new TIFF stack
tifffile.imwrite("extracted_channels_maskout.tiff", channels)
#tifffile.imwrite("extracted_channels.tiff", channels)


# In[68]:


# Use numpy.sum to combine the six channels
combined_channels = np.sum(channels, axis=0)

# Save the new TIFF file
tifffile.imwrite("combined_channels.tiff", combined_channels)


# In[ ]:




