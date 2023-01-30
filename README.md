# ImgReg
This Jupiter notebook performs multimodal image registration which use Elastix library for computation.
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
<br>
<br>
This approach can be applied to register both single fixed and moving images, as well as multiple fixed and moving images, such as in the IMC dataset where multiple channels are necessary for image registration. The registration cost function for a single image is defined by the first equation, while the second equation is used as the cost function for multiple channels registration.


Single fixed and moving images
<br>

$$
\mathcal{C}\left(\boldsymbol{T}_{\boldsymbol{\mu}} ; I_F, I_M\right)=\arg \min _{\boldsymbol{T}} \mathcal{C}\left(\boldsymbol{T} ; I_F, I_M\right)
$$
$$

<br>
Multiple fixed and moving images
<br>

$$
\mathcal{C}\left(\boldsymbol{T}_{\boldsymbol{\mu}} ; I_F, I_M\right)=\arg \min _{\boldsymbol{T}} \frac{1}{\sum_{i=1}^N \omega_i} \sum_{i=1}^N \omega_i \mathcal{C}\left(\boldsymbol{T}_{\boldsymbol{\mu}} ; I_F^i, I_M^i\right)
$$

<br>
When registering multiple images, Elastix will only export the first channel when using the WriteResultImage option. However, the full image stack can be exported through Transformix. To transform the original moving image using the Elastix registration transform parameters, which are stored as TransformParameters.0.txt, the following steps are required:
<br>
1. Set the path to the image registration parameters
<br>
2. Set the path to the original moving image
<br>
3. Set the pad width
<br>
4. Set the target image size.
