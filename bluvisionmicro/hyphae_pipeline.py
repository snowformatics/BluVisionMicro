import os
#import joblib
#from czifile import CziFile
import cv2
import czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing

#from hyphae_cmd.helpers import min_ip_stacking, get_leaf_area, get_hyphae_area, calculate_avg_hyphae_area
#from hyphae_cmd.segmentation import segment, get_all_rois, filter_rois
#rom hyphae_cmd.prediction import predict_with_handcrafted_features, predict_cnn


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
        """Reading and the czi images."""
        self.image_array = czi_helper.read_czi_image(os.path.join(self.source_path, self.experiment, self.hai),
                                                     self.slide_name)

    def czi_meta_info(self):
        self.czi_format, self.z_level, self.regions = czi_helper.get_czi_meta_info(self.image_array)

    def stack_images(self):
        self.image_stacked = bluvisionmicro.image_processing.min_ip_stacking(self.image_array, self.region,
                                                                             self.z_level, self.czi_format)


    def segment_hyphae(self):
        self.gray_image, self.binary_image = segment(self.image_stacked, self.slide_name, self.region)

    def get_rois(self):
        self.all_rois = get_all_rois(self.binary_image)
        return self.all_rois

    def filter_roi(self, all_rois):
        self.filtered_rois = filter_rois(self.image_stacked, self.gray_image, all_rois, self.slide_name, self.region)
        return self.filtered_rois

    def predict_rois(self):
        """Features extraction. Different for each pathogen should be overridden"""
        #predict_with_handcrafted_features(self.filtered_rois, self.image_stacked, self.clf_har, self.clf_pftas, self.destination_path, self.slide_name, self.region, self.file_results_name)
        predict_cnn(self.filtered_rois, self.image_stacked, self.cnn_model, self.destination_path, self.slide_name, self.region, self.file_results_name)

    def create_report(self):
        orga.create_report(self.plate_id, self.report_path)

    # def process(self):
    #     # override in derived classes to perform an actual segmentation
    #     pass

    def start_pipeline(self, args):
        """Starts the Macrobot analysis pipeline."""
        slide_name, cnn_model, source_path, destination_path, experiment, hai = args
        self.slide_name = slide_name
        self.cnn_model = cnn_model
        self.source_path = source_path
        self.destination_path = destination_path
        self.experiment = experiment
        self.hai = hai
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

            #cv2.imwrite(str(self.slide_name) + str(self.region) + '.png', self.image_stacked)
        #
        #     self.segment_hyphae()
        #     #import cv2
        #     #cv2.imwrite(str(self.slide_name) + str(self.region) + '.png', self.image_stacked)
        #
        #     all_rois2 = self.get_rois()
        #     filtered_rois = self.filter_roi(all_rois2)
        #     self.predict_rois()
        #     self.czi.close()
        #
        # self.get_polygon()
        # #get_hyphae_area(os.path.join(self.destination_path_org, self.experiment), self.file_results_name)
        # #calculate_avg_hyphae_area(os.path.join(self.destination_path_org, self.experiment), self.file_results_name, self.file_results_hyphae_avg_name)
        #
