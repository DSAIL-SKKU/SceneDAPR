import cv2
import json
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
import ujson as json
import pandas as pd
import numpy as np
from shapely.geometry import MultiLineString, Polygon, MultiPolygon


def get_image(strokes, stroke_color=(0, 0, 0), stroke_width=1, bg_color=(255, 255, 255), image_size=(448, 448)):
    """Get a `PIL Image <https://pillow.readthedocs.io/en/3.0.x/reference/Image.html>`_
    object of the drawing storkes.

    Input :
     strokes(List): A list of cordincate.
     stroke_color(Tuple): A list of RGB (red, green, blue) values for the stroke color,
        defaults to (0,0,0).
     stroke_width(int): A width of the stroke, defaults to 2.
     bg_color(Tuple): A list of RGB (red, green, blue) values for the background color,
        defaults to (255,255,255).
        A list of cordincate
     image_size(Tuple): A size of the image, defaults to (255,255).
    """
    image = Image.new("RGB", image_size, color=bg_color)
    image_draw = ImageDraw.Draw(image)

    for stroke in strokes:
        image_draw.line(stroke, fill=stroke_color, width=stroke_width)

    return image


def get_bbox_stroke(strokes):
    """Extract bounding box for the given strokes
    Input :
     img: an array of a image (h, w, ch)
    """

    line = MultiLineString(strokes)
    bbox = line.bounds  # minx, miny, maxx, maxy
    segmentations = [item for sublist in strokes for item in sublist]
    segmentations = np.array(segmentations).flatten().tolist()
    return bbox, segmentations


def get_bbox_image(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    ret, binary = cv2.threshold(gray, 240, 255, 0)

    contours, h = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

    poly_objs = []
    for i in range(len(contours)):
        if (i > 0) and (len(contours[i])) > 2:
            poly_objs.append(Polygon(np.squeeze(contours[i])))

    polygons = poly_objs

    bboxes = []  
    segmentations = []
    for poly in polygons:
        # cacluate the bounding box of the polygon
        bboxes.append(poly.bounds)

        # Simplify the polygon and extract the coordinates
        poly = poly.simplify(1.0, preserve_topology=False)
        if not isinstance(poly, MultiPolygon):
            segmentation = np.array(poly.exterior.coords).ravel()
            segmentations.append(segmentation)

    minx = min(bboxes, key=lambda x: x[0])[0]
    miny = min(bboxes, key=lambda x: x[1])[1]
    maxx = max(bboxes, key=lambda x: x[2])[2]
    maxy = max(bboxes, key=lambda x: x[3])[3]

    bbox = (minx, miny, maxx, maxy)

    segmentations = [item for sublist in segmentations for item in sublist]

    return bbox, segmentations


def get_cocobbox(segmentations):
    """Extract bounding box as a COCO format (min_x, min_y, width, height)
    """
    temp = np.array(segmentations).reshape(-1, 2)
    x, y = np.min(temp, axis=0)
    mx, my = np.max(temp, axis=0)
    cocobbox = (x, y, mx-x, my-y)

    return cocobbox


def get_stroke_alpha(strokes, stroke_color=(0, 0, 0), stroke_width=1, bg_color=(255, 255, 255), image_size=(535, 757)):
    """Get a `PIL Image <https://pillow.readthedocs.io/en/3.0.x/reference/Image.html>`_
    object of the drawing storkes.

    Args:
     strokes(List): A list of cordincate.
     stroke_color(Tuple): A list of RGB (red, green, blue) values for the stroke color,
        defaults to (0,0,0).
     stroke_width(int): A width of the stroke, defaults to 1.
     bg_color(Tuple): A list of RGB (red, green, blue) values for the background color,
        defaults to (255,255,255).
        A list of cordincate
     image_size(Tuple): A size of the image, defaults to (255,255).
    """
    bbox, segmentations = get_bbox_stroke(strokes)
    cocobox = [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]

    min_x, min_y, width, height = cocobox
    image_size = (int(width), int(height))
    image = Image.new("RGBA", image_size)
    image_draw = ImageDraw.Draw(image)

    for stroke in strokes:
        image_draw.line(stroke, fill=stroke_color, width=stroke_width)

    return image, cocobox, segmentations


def get_image_alpha(image_path, threshold=50):
    """Remove white background and convert to alpha image.
    Args:
        image_path(str) : a file path of the image
        threshold(int) : threshold of the white background
    Returns:
        image(PIL Image) : a image with alpha channel
    """
    image = Image.open(image_path).convert('RGB')
    im_inv = ImageOps.invert(image)

    im_inv_L = Image.eval(image, lambda p: 0 if p <= threshold else 255)
    im_inv_L = im_inv.convert('L')
    image.putalpha(im_inv_L)  # RGBA

    # Extract bounding box
    # bbox = (minx, miny, maxx, maxy)
    bbox, segmentations = get_bbox_image(image_path)
    # cocobox = (minx, miny, maxx-minx, maxy-miny)
    cocobox = get_cocobbox(segmentations)

    # Remove padding
    image = image.crop(bbox)

    return image, cocobox, segmentations


def load_ndjson(fname):
    """Load ndjson file
    """
    records = map(json.loads, open(fname))
    df = pd.DataFrame.from_records(records)
    raw_drawing = df['drawing'].values
    return raw_drawing


def get_strokes(image_data):
    """Covert a quick draw format as the sequence of coordincates.
    """
    _strokes = []
    for stroke in image_data:
        points = []
        xs = stroke[0]
        ys = stroke[1]

        if len(xs) != len(ys):
            raise Exception(
                "something is wrong, different number of x's and y's")

        for point in range(len(xs)):
            x = xs[point]
            y = ys[point]
            points.append((x, y))
        _strokes.append(points)

    return _strokes


def get_svg(svg_file):
    """Covert a svg format (e.g., Quickdraw dataet).
    Args:
     svg_file(str) : a file path of the svg file
                     ex) "example.svg"

    Returns:
     _quickdraw(List) :drawing(x,y,pen_state)
     >> [[[x1,x2...],[y1,y2...],[p1,p2...], #first stroke
          [x1,x2...],[y1,y2...],[p1,p2...]  #second stroke
                    ... ]]]
    """
    from xml.dom import minidom
    whole_drawing = []

    # read the SVG file
    doc = minidom.parse(svg_file)
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()
    whole_drawing = []
    for stroke in path_strings:
        x = []
        y = []
        stroke = stroke.split(" ")
        for point in stroke:
            split_point = point.split(",")
            if split_point[0][0] == 'M':
                x.append(float(split_point[0][1:]))
                y.append(float(split_point[1]))
            elif split_point[0][0] == 'C':
                x.append(float(split_point[0][1:]))
                y.append(float(split_point[1]))
            else:
                x.append(float(split_point[0]))
                y.append(float(split_point[1]))
        strokes = np.array(list(zip(x, y)))
        whole_drawing.append(strokes)

    return whole_drawing


def resize_image(image, cocobbox, segmentations, max_width, max_height, margin=10):
    """Resize image to max_width and max_height with the original ratio.

    """
    w, h = image.size
    resize_ratio_h = 1.0
    resize_ratio_w = 1.0

    # Step 1: resize image to max_height
    new_h = max_height - margin
    resize_ratio_h = new_h / h
    w = int(w * resize_ratio_h)
    new_size = (w, new_h)
    image = image.resize(new_size)

    # Step 2: resize image to max_width if new_w > max_width
    if (w >= max_width):
        new_w = max_width - margin
        resize_ratio_w = new_w / w
        h = int(new_h * resize_ratio_w)
        new_size = (new_w, h)
        image = image.resize(new_size)

    # Step 3: Apply resizing ratio to bounding box and coordinates
    resize_ratio = resize_ratio_w * resize_ratio_h
    cocobbox = [round(cord * resize_ratio, 1) for cord in cocobbox]
    segmentations = [round(cord * resize_ratio, 1) for cord in segmentations]

    return image, cocobbox, segmentations
