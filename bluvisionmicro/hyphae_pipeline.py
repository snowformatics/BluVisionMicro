

from czifile import CziFile
import joblib
from keras.models import load_model
import os


from hyphae_cmd.helpers import min_ip_stacking, get_leaf_area, get_hyphae_area, calculate_avg_hyphae_area
from hyphae_cmd.segmentation import segment, get_all_rois, filter_rois
from hyphae_cmd.prediction import predict_with_handcrafted_features, predict_cnn


class HyphaePipeline(object):
    """Hyphae pipeline main class.

    :param slide: A list of all images names per plate (green channel, blue channel, red channel, backlight image, UVS image.
    :type slide: list
    :param path: The path which contains the raw images coming from the macrobot image acquisition.
    :type path_source: str
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

    #def __init__(self, slide, path_source, destination_path, experiment, hai, file_results_name, file_results_hyphae_avg_name, file_results_leaf_area):
    def __init__(self):
        print ('init)')

        # self.slide_name = slide
        # self.path_source = path_source
        # self.file_results_name = file_results_name
        # self.file_results_hyphae_avg_name = file_results_hyphae_avg_name
        # self.file_results_leaf_area = file_results_leaf_area
        #
        # self.experiment = experiment
        # self.h = hai
        # self.czi_format = None
        # self.destination_path_org = destination_path

    def create_folder_structure(self):
        """Create all necessary folders."""
        if not os.path.exists(os.path.join(self.destination_path)):
            os.makedirs(os.path.join(self.destination_path))

    def get_meta(self):
        # We check which CZI format we have
        # New CZI format
        if len(self.image_array.shape) == 6:
            self.czi_format = 'new'
            self.z_level = self.image_array.shape[2]
            self.regions = int(self.image_array.shape[0])
        # Old CZI format
        if len(self.image_array.shape) == 7:
            self.czi_format = 'old'
            self.z_level = self.image_array.shape[3]
            self.regions = int(self.image_array.shape[1])

    def get_polygon(self):
        with CziFile(os.path.join(self.path_source, self.slide_name)) as self.czi:
            itemlist = self.czi.metadata()
            get_leaf_area(self.slide_name, itemlist, self.file_results_leaf_area)

    def read_images(self):
        """Reading and the czi images."""

        with CziFile(os.path.join(self.path_source, self.slide_name)) as self.czi:
            # Loading the entire CZI file
            self.image_array = self.czi.asarray()
            print (self.image_array.shape)
            self.get_meta()

            print (self.slide_name, self.czi_format, self.image_array.shape, self.regions, self.z_level)

    def load_models(self):
        self.clf_har = joblib.load('har.pkl')
        self.clf_pftas = joblib.load('pftas.pkl')
        self.clf_cnn = load_model('09112020_1.h5')


    def stack_images(self, image_array, region, z_level):
        self.image_stacked = min_ip_stacking(image_array, self.region, z_level, self.czi_format)


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
        predict_cnn(self.filtered_rois, self.image_stacked, self.clf_cnn, self.destination_path, self.slide_name, self.region, self.file_results_name)

    def create_report(self):
        orga.create_report(self.plate_id, self.report_path)

    # def process(self):
    #     # override in derived classes to perform an actual segmentation
    #     pass

    def start_pipeline(self, args):
        """Starts the Macrobot analysis pipeline."""
        slide, path_source, destination_path, experiment, hai, file_results_name, file_results_hyphae_avg_name, file_results_leaf_area = args
        self.slide_name = slide
        self.path_source = path_source
        self.file_results_name = file_results_name
        self.file_results_hyphae_avg_name = file_results_hyphae_avg_name
        self.file_results_leaf_area = file_results_leaf_area

        self.experiment = experiment
        self.h = hai
        self.czi_format = None
        self.destination_path_org = destination_path

        print('...Analyzing slide ' + self.slide_name)
        self.read_images()
        self.load_models()
        for self.region in range(self.regions):
            print (self.region)
            self.destination_path = os.path.join(self.destination_path_org, self.experiment, self.h, self.slide_name, str(self.region))
            self.create_folder_structure()

            self.stack_images(self.image_array, self.region, self.z_level)

            self.segment_hyphae()
            #import cv2
            #cv2.imwrite(str(self.slide_name) + str(self.region) + '.png', self.image_stacked)

            all_rois2 = self.get_rois()
            filtered_rois = self.filter_roi(all_rois2)
            self.predict_rois()
            self.czi.close()

        self.get_polygon()
        #get_hyphae_area(os.path.join(self.destination_path_org, self.experiment), self.file_results_name)
        #calculate_avg_hyphae_area(os.path.join(self.destination_path_org, self.experiment), self.file_results_name, self.file_results_hyphae_avg_name)

