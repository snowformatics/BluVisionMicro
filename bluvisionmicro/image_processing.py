import numpy as np
import cv2

def rgb_to_yq1q2(image):
    """ RGB to YQ1Q2 color space conversion.
        Parameters
        ----------
        rgb : array_like
            The image in RGB format.
        Returns
        -------
        out : yq1q2 image, y, q1 and q2 channel as ndarray.
        ----------
        .. [1] DOI: 10.1109/72.554203
    """
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    r = np.asarray(r, dtype=float)
    b = np.asarray(b, dtype=float)
    #q1 = (r / (r + g)) * 255
    q2 = (r / (r + b)) * 255
    #y = (((r + g + b) / 3) / 255) * 255

    # # Merge channels
    # yq1q2_image = np.zeros((q1.shape[0], q1.shape[1], 3))
    # yq1q2_image[:, :, 0] = y
    # yq1q2_image[:, :, 1] = q1
    # yq1q2_image[:, :, 2] = q2

    return q2


def min_ip_stacking(image_array, region, z_level, czi_format):
    """Stacking method which extract the minimum pixel value for each position of all focal planes.
    Args:
      image_array : A czi image_name array with x focal planes.
      region : The region of the czi image_name array. One region means one leaf.

    Returns:
      image_stacked: The stacked image_name with one focal plane.
    """

    if czi_format == 'old':
        images = [image_array[0, region, 0, index] for index in range(z_level)]
        image_stacked = np.ones(image_array[0, region, 0, 0].shape, dtype=image_array[0, 0, 0, 0].dtype) * 255
    if czi_format == 'new':
        images = [image_array[region, 0, index] for index in range(z_level)]
        image_stacked = np.ones(image_array[region, 0, 0].shape, dtype=image_array[0, 0, 0].dtype) * 255

    for img in images:
        image_stacked = np.minimum(image_stacked, img)
    image_stacked = cv2.cvtColor(image_stacked, cv2.COLOR_BGR2RGB)
    return image_stacked


