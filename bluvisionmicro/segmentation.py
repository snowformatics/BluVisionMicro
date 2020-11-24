import cv2
import numpy as np
from skimage import img_as_ubyte, img_as_uint
from hyphae_cmd.helpers import auto_canny
from skimage.morphology import binary_closing, dilation
from skimage.filters import threshold_otsu, threshold_li, threshold_yen, threshold_isodata, threshold_mean, threshold_sauvola, threshold_niblack, threshold_triangle, threshold_minimum, threshold_local, threshold_multiotsu
from hyphae_cmd.color_spaces import rgb_to_yq1q2


def threshold_image(image_stacked):

    image = image_stacked
    image[np.where((image == [0, 0, 0]).all(axis=2))] = [255, 255, 255]

    # Convert RGB image into YQ1Q2
    # We need only the Q2 channel
    q2_channel = rgb_to_yq1q2(image).astype(np.uint8)
    # Image thresholding to get binary image
    binary_image = threshold_yen(q2_channel[q2_channel != 255])
    binary_image = q2_channel < binary_image
    binary_image = img_as_uint(binary_image)

    return binary_image


def get_all_rois(binary_image):
    (contours, _) = cv2.findContours(img_as_ubyte(binary_image), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filter_rois(all_rois):
    """Filter the contours by low level features like size and ration. Optimized for hyphea.
        Args:
          contours : The contours of the binary image_name.
        Returns:
          contours_filtered : A list of filtered contours as coordinates.
        Example:
        image_name[30:40,30:40] extract a 10x10 pixel sub-image_name at position x=30, y=30
        """

    # We store the contours which pass all criteria
    contours_filtered = []
    # Some fixed parameters
    max_hyphae_height = 800
    max_hyphae_width = 1400
    max_aspect_ratio = 10.0
    min_aspect_ratio = 0.5
    max_len_cnt = 50000
    min_len_cnt = 150

    for cnt in all_rois:
        x, y, width, height = cv2.boundingRect(cnt)
        # We apply a very simple rough filter with geometrical parameters, to exclude very large or small objects
        if len(cnt) > min_len_cnt and len(cnt) < max_len_cnt:
            if width < max_hyphae_width and height < max_hyphae_height:
                if float(width / height) < max_aspect_ratio or float(width / height) > min_aspect_ratio:
                    area = cv2.contourArea(cnt)
                    contours_filtered.append((y, y + height, x, x + width, area))

    return contours_filtered
