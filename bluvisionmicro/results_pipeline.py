import os
import bluvisionmicro.czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing
import bluvisionmicro.segmentation
import bluvisionmicro.deep_learning_helpers


class ResultsPipeline(object):
    """
    """
    NAME = "invalid"

    def __init__(self):
        print ('start')

    def get_leaf_area(self):
        self.leaf_area = bluvisionmicro.czi_helper.get_polygon((os.path.join(self.source_path, self.experiment,
                                                                                 self.hai)),
                                                                self.slide_name)



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
        self.get_leaf_area()
        print (self.leaf_area)
        # # Get some meta information about the file
        # self.czi_meta_info()
        #
        # # We loop over all regions on the CZI image
        # for self.region in range(self.regions):
        #
        #     # We create the destination paths
        #     bluvisionmicro.io.create_folders(os.path.join(self.destination_path, self.experiment, self.hai,
        #                                                   self.slide_name, str(self.region)))
        #
        #     # We create a stacked image from the z-stack
        #     self.stack_images()
        #
        #     # We create a binary image
        #     self.create_binary_image()
        #
        #     # We extract all contours objects as possible ROIs
        #     self.extract_contours()
        #
        #     # We apply some simple geometric filters to remove some trash objects (to small, to large etc.)
        #     self.filter_contours()
        #
        #     # We classify the objects with a CNN model
        #     self.predict_hyphae()
        #
        #
        #     #bluvisionmicro.io.save_image(str(self.slide_name) + str(self.region) + 'binary.png', self.binary_image)




        #     all_rois2 = self.get_rois()
        #     filtered_rois = self.filter_roi(all_rois2)
        #     self.predict_rois()
        #     self.czi.close()
        #
        # self.get_polygon()
        # #get_hyphae_area(os.path.join(self.destination_path_org, self.experiment), self.file_results_name)
        # #calculate_avg_hyphae_area(os.path.join(self.destination_path_org, self.experiment), self.file_results_name, self.file_results_hyphae_avg_name)
        #
