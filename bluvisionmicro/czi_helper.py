import os
from czifile import CziFile


def read_czi_image(source_path, slide_name):
    """Reading and the czi images."""
    with CziFile(os.path.join(source_path, slide_name)) as czi:
        # Loading the entire CZI file
        image_array = czi.asarray()
    return image_array


def get_czi_meta_info(image_array):
    # We check which CZI format we have
    # New CZI format
    if len(image_array.shape) == 6:
        czi_format = 'new'
        z_level = image_array.shape[2]
        regions = int(image_array.shape[0])
    # Old CZI format
    if len(image_array.shape) == 7:
        czi_format = 'old'
        z_level = image_array.shape[3]
        regions = int(image_array.shape[1])
    return czi_format, z_level, regions


def get_polygon(self):
    with CziFile(os.path.join(self.source_path, self.slide_name)) as self.czi:
        itemlist = self.czi.metadata()
        get_leaf_area(self.slide_name, itemlist, self.file_results_leaf_area)


