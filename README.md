# ImgReg
This Jupiter notebook performs multimodal image registration using Elastix.
<br>
<br>
To get started, first download Elastix [Elastix 5.0.1 Release](https://github.com/SuperElastix/elastix/releases/tag/5.0.1) and extract the archive to a folder of your choice. Then, to make Elastix accessible to your $PATH environment, take the following steps: On Windows 7 and Windows 10, navigate to the control panel, select “System”, then “Advanced system settings”. From there, click “Environmental variables” and add the Elastix folder to the variable “path”.
<br>
<br>
We will register the images using both an affine and a nonlinear transformation. We will first perform affine registration, and then use the output of that registration as input for non-linear registration to obtain the final results.
<br>
<br>
You can mask out your image using ImageJ/FIJI by selecting 'Edit' > 'Selection' > 'Create Mask', or online with the [VGG Image Annotation Tool](https://www.robots.ox.ac.uk/~vgg/software/via/) 
<br>
<br>
To review the registration results, load the images from the output folder into ImageJ/FIJI. If needed, adjust the registration parameters by editing the text file. For more information, visit the [Elastix Model Zoo](https://elastix.lumc.nl/modelzoo/) 

