import os
from czifile import CziFile
from xml.dom.minidom import parseString


def read_czi_image(source_path, slide_name):
    """Reading and the czi images."""
    with CziFile(os.path.join(source_path, slide_name)) as czi:
        # Loading the entire CZI file
        image_array = czi.asarray()
    return image_array


def get_czi_meta_info(image_array):
    # We check which CZI format we have
    # New CZI format
    if len(image_array.shape) == 6:
        czi_format = 'new'
        z_level = image_array.shape[2]
        regions = int(image_array.shape[0])
    # Old CZI format
    if len(image_array.shape) == 7:
        czi_format = 'old'
        z_level = image_array.shape[3]
        regions = int(image_array.shape[1])
    return czi_format, z_level, regions


def calculate_area_polygon(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


def get_leaf_area(slide_name, czi_xml):
    xmldoc = parseString(czi_xml)
    tile_region= xmldoc.getElementsByTagName('TileRegion')
    leaf_area_lst = []
    for region in range(len(tile_region)):
        scan_region = tile_region.item(region).getElementsByTagName('Points')

        try:
            polygon = scan_region[0].firstChild.data
            polygon = polygon.split(' ')
            polygon_as_tuple = []
            for points in polygon:
                polygon_as_tuple.append((float(points.split(',')[0]), float(points.split(',')[1])))
            leaf_area = calculate_area_polygon(polygon_as_tuple)
            leaf_area_lst.append([slide_name, region, round(leaf_area, 0)])
        except IndexError:
            # Sometimes we can not extract a polygon from the czi file, we set leaf area to NaN
            leaf_area_lst.append([slide_name, region, 'NaN'])
    return leaf_area_lst


def get_polygon(source_path, slide_name):
    with CziFile(os.path.join(source_path, slide_name)) as czi:
        itemlist = czi.metadata()
        leaf_area_lst = get_leaf_area(slide_name, itemlist)
    return leaf_area_lst


def get_label(source_path, label_path, slide_name):
    with CziFile(os.path.join(source_path, slide_name)) as czi:
        czi.save_attachments(directory=label_path + slide_name)

