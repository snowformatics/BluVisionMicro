import os
import bluvisionmicro.czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing
import bluvisionmicro.segmentation
import bluvisionmicro.deep_learning_helpers


class HyphaePipeline(object):
    """Hyphae pipeline main class.

    :param slide: A list of all images names per plate (green channel, blue channel, red channel, backlight image, UVS image.
    :type slide: list
    :param path: The path which contains the raw images coming from the macrobot image acquisition.
    :type source_path: str
    :param destination_path: The path to store the final result images and csv file.
    :type destination_path: str
    :param file_results_name: The CSV file for each experiments which contains the pathogen prediction per leaf.
    :type file_results_name: file object
    :param experiment: The experiment name.
    :type experiment: str
    :param hai: Hours after inoculation.
    :type hai: str
    """
    NAME = "invalid"

    def __init__(self):
        print ('start')

    def read_images(self):
        self.image_array = bluvisionmicro.czi_helper.read_czi_image(os.path.join(self.source_path, self.experiment,
                                                                                 self.hai),
                                                                    self.slide_name)

    def czi_meta_info(self):
        self.czi_format, self.z_level, self.regions = bluvisionmicro.czi_helper.get_czi_meta_info(self.image_array)

    def stack_images(self):
        self.stacked_image = bluvisionmicro.image_processing.min_ip_stacking(self.image_array, self.region,
                                                                             self.z_level, self.czi_format)

    def create_binary_image(self):
        self.binary_image = bluvisionmicro.segmentation.threshold_image(self.stacked_image)

    def extract_contours(self):
        self.all_contour_objects = bluvisionmicro.segmentation.get_all_contours(self.binary_image)

    def filter_contours(self):
        self.filtered_contour_objects = bluvisionmicro.segmentation.filter_contours(self.all_contour_objects)

    def predict_hyphae(self):
        bluvisionmicro.deep_learning_helpers.classify_object(self.filtered_contour_objects, self.stacked_image,
                                                             self.cnn_model, os.path.join(self.source_path,
                                                                                          self.experiment, self.hai),
                                                             self.slide_name,
                                                             self.sensitivity)

    def start_pipeline(self, args):
        """Starts the Macrobot analysis pipeline."""
        slide_name, cnn_model, source_path, destination_path, experiment, hai, sensitivity = args
        self.slide_name = slide_name
        self.cnn_model = cnn_model
        self.source_path = source_path
        self.destination_path = destination_path
        self.experiment = experiment
        self.hai = hai
        self.sensitivity = sensitivity
        self.czi_format = None

        print('...Analyzing slide ' + self.slide_name)
        # We read the CZI file as numpy array in memory
        self.read_images()
        # Get some meta information about the file
        self.czi_meta_info()

        # We loop over all regions on the CZI image
        for self.region in range(self.regions):

            # We create the destination paths
            bluvisionmicro.io.create_folders(os.path.join(self.destination_path, self.experiment, self.hai,
                                                          self.slide_name, str(self.region)))

            # We create a stacked image from the z-stack
            self.stack_images()

            # We create a binary image
            self.create_binary_image()

            # We extract all contours objects as possible ROIs
            self.extract_contours()

            # We apply some simple geometric filters to remove some trash objects (to small, to large etc.)
            self.filter_contours()


            # We classify the objects with a CNN model
            self.predict_hyphae()


