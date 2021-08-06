from bluvisionmicro.hyphae_pipeline import HyphaePipeline
import bluvisionmicro.segmentation


class MildewClassificationSmall(HyphaePipeline):
    """Hyphae analysis for blumeria graminis pathogen.
       Optimized for small size colonies, like 24-50 hai."""

    NAME = 'MildewSmall'

    def filter_contours(self):
        """Filter contour by size and other geometrical features.
        Optimized for 48hai"""
        max_hyphae_height = 800
        max_hyphae_width = 1400
        max_len_cnt = 50000
        min_len_cnt = 150
        self.filtered_contour_objects = bluvisionmicro.segmentation.filter_contours(self.all_contour_objects,
                                                                                    self.stacked_image,
                                                                                    max_hyphae_height, max_hyphae_width,
                                                                                    max_len_cnt, min_len_cnt)
        return self.filtered_contour_objects


class MildewClassificationLarge(HyphaePipeline):
    """Hyphae analysis for blumeria graminis pathogen.
       Optimized for large size colonies, like >= 50hai."""

    NAME = 'MildewLarge'

    def filter_contours(self):
        """Filter contour by size and other geometrical features.
        Optimized for >= 50hai"""
        max_hyphae_height = 1500
        max_hyphae_width = 2500
        max_len_cnt = 500000
        min_len_cnt = 500
        self.filtered_contour_objects = bluvisionmicro.segmentation.filter_contours(self.all_contour_objects,
                                                                                    self.stacked_image,
                                                                                    max_hyphae_height, max_hyphae_width,
                                                                                    max_len_cnt, min_len_cnt,
                                                                                    extent= 0.36)
        return self.filtered_contour_objects
