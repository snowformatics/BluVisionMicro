import os
import bluvisionmicro.czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing
import bluvisionmicro.segmentation
import bluvisionmicro.deep_learning_helpers
import bluvisionmicro.get_results


class ResultsPipeline(object):
    """
    """
    NAME = "invalid"

    def __init__(self):
        print ('start')

    def get_leaf_area(self, slides):
        self.slide_area_all = []
        for slide_name in slides:
            leaf_area = bluvisionmicro.czi_helper.get_polygon((os.path.join(self.source_path, self.experiment,
                                                                                     self.hai)), slide_name)
            for l in leaf_area:
                self.slide_area_all.append(l)

    def get_hyphae_area(self):
        self.hyphae_area_lst = bluvisionmicro.get_results.get_hyphae_area(self.destination_path)

    def get_hyphae_area_avg(self):
        self.hyphae_area_avg_lst = bluvisionmicro.get_results.calculate_avg_hyphae_area(self.hyphae_area_lst)


    def get_slide_labels(self, slides):
        for slide_name in slides:
            bluvisionmicro.czi_helper.get_label((os.path.join(self.source_path, self.experiment,self.hai)), None,
                                                slide_name)

    def write_data_csv(self, data, file_name, header):
        bluvisionmicro.io.write_csv(data, file_name, header)

    def start_pipeline(self, args):
        """Starts the Macrobot analysis pipeline."""
        images, source_path, destination_path, experiment, hai = args
        self.slides = images
        self.source_path = source_path
        self.destination_path = destination_path
        self.experiment = experiment
        self.hai = hai
        self.czi_format = None

        # Extract the leaf area for each leaf
        self.get_leaf_area(self.slides)

        # Extract Hyphae area
        self.get_hyphae_area()

        # Calculate average hyphae area per leaf
        self.get_hyphae_area_avg()

        # Write leaf area, hyphae area and average hyphae area to CSV file
        print (self.hyphae_area_avg_lst)
        result_lst = [[self.slide_area_all, 'test.csv', ['Slide_name', 'Region', 'Leaf_area']],
                      [self.hyphae_area_lst, 'test2.csv', ['Slide_name', 'Region', 'Prediction%', 'Leaf_area']],
                      [self.hyphae_area_avg_lst, 'test3.csv', ["slide_name", "Slide_region", "mean_area", "std_area", "nr_of_colonies"]]]
        for result in result_lst:
            self.write_data_csv(result[0], result[1], result[2])



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
