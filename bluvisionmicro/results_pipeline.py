import os
import bluvisionmicro.czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing
import bluvisionmicro.segmentation
import bluvisionmicro.deep_learning_helpers
import bluvisionmicro.roi_helpers


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
        self.hyphae_area_lst = bluvisionmicro.roi_helpers.get_hyphae_area(os.path.join(self.destination_path,
                                                                                       self.experiment, self.hai))

    def get_hyphae_area_avg(self):
        self.hyphae_area_avg_lst = bluvisionmicro.roi_helpers.calculate_avg_hyphae_area(self.hyphae_area_lst)

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

        result_lst = [[self.slide_area_all,
                       os.path.join(self.destination_path,self.experiment, self.hai, self.experiment + "_leaf_area.csv"),
                       ['Slide_ID', 'Slide_region', 'Leaf_area']],

                      [self.hyphae_area_lst,
                       os.path.join(self.destination_path, self.experiment, self.hai, self.experiment + "_colony_area.csv"),
                       ['Slide_ID', 'Slide_region', 'Colony_area', 'Prediction']],

                      [self.hyphae_area_avg_lst,
                       os.path.join(self.destination_path, self.experiment, self.hai,
                                    self.experiment + "_colony_mean_area.csv"),
                       ["Slide_ID", "Slide_region", "Colony_mean_area", "Colony_median_area", "Colony_std_area", "Nr_of_colonies"]]]

        for result in result_lst:
            self.write_data_csv(result[0], result[1], result[2])

