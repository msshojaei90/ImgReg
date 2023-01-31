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
When registering multiple images, Elastix only exports the first channel using the WriteResultImage option. To export the full image stack, first run <code style="color:yellow">Multiple_Channel_Elastix.py</code> and get the <code style="color:yellow">TransformParameters.0.txt</code> file as output. Then, use it as input for <code style="color:yellow">Multiple_Channel_Transformix.py</code> code. This will register all channels and produce the result as a stack TIFF file.
<br>
<br>
All IMC data channels are not filled by an actual protein, some are just metal tags with no information. Channel selection is necessary. To do so, run the code `<code style="color:yelow">Channel_Selection.py</code>` to choose relevant channels and create new stack TIFF files. The output can then be used for multimodal image registration.


