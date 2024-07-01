import os
import bluvisionmicro.czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing
import bluvisionmicro.segmentation
import bluvisionmicro.deep_learning_helpers
import bluvisionmicro.roi_helpers


class HyphaePipeline(object):
    """Hyphae pipeline main class.

    :param slide: A list of all images names .
    :type slide: list
    :param path: The path which contains the raw images.
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
        print ('')

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
        pass

    def remove_overlapping_contours(self):
        self.filtered_contour_objects2 = bluvisionmicro.roi_helpers.combine_boxes(self.filtered_contour_objects)

    def predict_hyphae(self, roi_path):
        self.positive_roi_lst = bluvisionmicro.deep_learning_helpers.classify_object(self.filtered_contour_objects, self.stacked_image,
                                                             self.cnn_model, roi_path, self.slide_name,
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

        print (self.regions)

        # We loop over all regions on the CZI image
        for self.region in range(self.regions):
            # Roi path
            roi_path = os.path.join(self.destination_path, self.experiment, self.hai, self.slide_name, str(self.region))
            # We create the destination paths
            bluvisionmicro.io.create_folders(roi_path)
            # We create a stacked image from the z-stack
            self.stack_images()
            #bluvisionmicro.io.save_image('D:/Mikroskop/Images/BluVisionHyphae/stacked/' +  self.slide_name + str(self.region) + '_stack.png', self.stacked_image)

            # We create a binary image
            self.create_binary_image()

            # We extract all contours objects as possible ROIs
            self.extract_contours()

            # We apply some simple geometric filters to remove some trash objects (to small, to large etc.)
            self.filter_contours()

            # We classify the objects with a CNN model
            self.predict_hyphae(roi_path)

            #imgage_rectangles = bluvisionmicro.io.draw_rectangle_on_image(self.stacked_image, self.positive_roi_lst)
            #bluvisionmicro.io.save_image('stacked' + self.slide_name + str(self.region) + '.png', self.stacked_image)
            #bluvisionmicro.io.save_image('D:/Mikroskop/Images/BluVisionHyphae/experiments/stacked_bbox' + self.slide_name + str(self.region) + '.png', imgage_rectangles)