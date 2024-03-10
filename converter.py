import glob
import itertools
from shapely.geometry import Polygon, MultiPolygon
from src.create_annotations import *
from tqdm import tqdm
from config import category_ids

# Define which colors match which categories in the images
num_category = [1, 4, 9, 11, 9, 7]

category_colors = {}
category_colors['(255, 0, 0)'] = 0  # rain
for i in range(num_category[1]):  # num_umbrella
    p = (0 + i*10, 255, 0)
    category_colors[str(p)] = 1
for i in range(num_category[2]):  # num_person
    p = (0 + i*10, 0, 255)
    category_colors[str(p)] = 2
for i in range(num_category[3]):  # num_lightning
    p = (128 + i*10, 128, 255)
    category_colors[str(p)] = 3
for i in range(num_category[4]):  # num_cloud
    p = (255, 255, 0 + i*10)
    category_colors[str(p)] = 4
for i in range(num_category[5]):  # num_pool
    p = (255, 127, 39 + i*10)
    category_colors[str(p)] = 5


def images_annotations_info(maskpath):
    """Get images and annotation info
    Input : mask image(png)
    Output : images info, annotations info, annotation_id
    """

    # This id will be automatically increased as we go
    annotation_id = 0
    image_id = 0
    annotations = []
    annotation = []
    images = []

    for mask_image in tqdm(glob.glob(maskpath + "*.png")):
        # The mask image is *.png but the original image is *.jpg.
        # We make a reference to the original file in the COCO JSON file
        original_file_name = os.path.basename(
            mask_image).split(".")[0] + ".png"

        # Open the image and (to be sure) we convert it to RGB
        mask_image_open = Image.open(mask_image).convert("RGB")
        w, h = mask_image_open.size

        # "images" info
        image = create_image_annotation(original_file_name, w, h, image_id)
        images.append(image)

        sub_masks = create_sub_masks(mask_image_open, w, h)
        for color, sub_mask in sub_masks.items():
            if color != '(0, 0, 0)':
                try:
                    category_id = category_colors[color]
                except:
                    print("KeyError at", mask_image)

                # "annotations" info
                annotation = []

                polygons, segmentations = create_sub_mask_annotation(sub_mask)

                for i in range(len(polygons)):
                    # Cleaner to recalculate this variable

                    segmentation = [
                        np.array(polygons[i].exterior.coords).ravel().tolist()]
                    annotation.append(segmentation)

                segmentation = list(itertools.chain.from_iterable(annotation))
                segmentation = list(
                    itertools.chain.from_iterable(segmentation))
                an = create_annotation_format(
                    polygons[i], segmentation, image_id, category_id, annotation_id)

                temp = an['segmentation']
                temp = np.array(temp).reshape(-1, 2)
                x, y = np.min(temp, axis=0)
                mx, my = np.max(temp, axis=0)
                an['bbox'] = (x, y, mx-x, my-y)

                annotations.append(an)

                annotation_id += 1
        image_id += 1
    return images, annotations, annotation_id


def create_sub_mask_annotation(sub_mask):
    """Find contours (boundary lines) around each sub-mask
    Input : sub mask
    Output : contours polygons, segmentations
    """
    contours = measure.find_contours(
        np.array(sub_mask), 0.5, positive_orientation="low")

    polygons = []
    segmentations = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(1.0, preserve_topology=False)

        if(poly.is_empty):
            # Go to next iteration, dont save empty values in list
            continue
        if not isinstance(poly, MultiPolygon):
            polygons.append(poly)
            segmentation = np.array(poly.exterior.coords).ravel().tolist()
            segmentations.append(segmentation)

    return polygons, segmentations
