import os
import bluvisionmicro.czi_helper
import bluvisionmicro.io
import bluvisionmicro.image_processing
import bluvisionmicro.segmentation
import bluvisionmicro.deep_learning_helpers
import bluvisionmicro.roi_helpers
import pandas as pd


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


    def merge(self, data1, header1, data2, header2):
        # Merge mean colony with leaf area to normalize
        # ToDo add normalization per mm2
        df1 = pd.DataFrame(data1, columns=header1)
        data2.columns = header2
        data2["Slide_region"] = pd.to_numeric(data2["Slide_region"])
        df = pd.merge(df1, data2,  how='left', on=['Slide_ID', 'Slide_region'])

        # Important: In case leaf area is NaN, we impute the NaN values with mean
        df['Leaf_area'] = df['Leaf_area'].astype(float).fillna(df['Leaf_area'].astype(float).mean(skipna=True))
        df['Normalized_colonies'] = df['Nr_of_colonies'] / df['Leaf_area']*100000000

        return df


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

        header_avg = ["Slide_ID", "Slide_region", "Colony_mean_area", "Colony_median_area", "Colony_std_area", "Nr_of_colonies"]
        header_slide = ['Slide_ID', 'Slide_region', 'Leaf_area']
        df_merged = self.merge(self.slide_area_all, header_slide, self.hyphae_area_avg_lst, header_avg)

        result_lst = [[self.slide_area_all,
                       os.path.join(self.destination_path,self.experiment, self.hai, self.experiment + "_leaf_area.csv"),
                       header_slide],

                      [self.hyphae_area_lst,
                       os.path.join(self.destination_path, self.experiment, self.hai, self.experiment + "_colony_area.csv"),
                       ['Slide_ID', 'Slide_region', 'Colony_area', 'Prediction']],

                      [self.hyphae_area_avg_lst,
                       os.path.join(self.destination_path, self.experiment, self.hai,
                                    self.experiment + "_colony_mean_area.csv"), header_avg],
                      [df_merged,
                      os.path.join(self.destination_path, self.experiment, self.hai,
                                   self.experiment + "_colony_mean_area_normalized.csv"), None ]]


        for result in result_lst:
            self.write_data_csv(result[0], result[1], result[2])

