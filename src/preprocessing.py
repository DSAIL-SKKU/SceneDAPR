import numpy as np
from xml.dom import minidom
import re


def svg_to_coordinate(file_path):
    '''Reads an SVG file and returns a numpy array of the contours.
    
    Args:
        file_path (str): The path of the SVG file.
        
    Returns:
        numpy.ndarray: A numpy array of the contours. The shape of the array is (number of strokes, number of points, 2).
                       Each point is represented as [x, y].
                       Example: [[[x1, y1], ..., [xn, yn]], ...]
    '''
    
    # Parse the SVG file
    doc = minidom.parse(file_path)
    countours = []
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()

    # Regular expression pattern to remove capital letters
    eng = re.compile('[A-Z]+')
    
    # Process each path string
    for path in path_strings:
        p = []
        point_list = path.split(' ')
        try:
            # Iterate over the list of points
            for point in point_list:
                if point == '':
                    continue
                point_ = eng.sub('', point)
                x, y = point_.split(',')
                p.append(np.array([float(x), float(y)]))
                
            # Add the contour to the list of contours
            countours.append(p)
        except:
            continue

    return countours
