import os
from czifile import CziFile


def read_czi_image(source_path, slide_name):
    """Reading and the czi images."""
    with CziFile(os.path.join(source_path, slide_name)) as czi:
        # Loading the entire CZI file
        image_array = czi.asarray()
        print (image_array.shape)


