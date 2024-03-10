from __future__ import annotations
import os
from argparse import ArgumentParser
import shutil
from converter import *
from src.create_annotations import *
from config import category_sample_paths, category_ids, category_keys
from tqdm import tqdm
from src.synthesize_scene import *
from PIL import Image
import glob
import random
from copy import deepcopy

def annotations_groupby_image(mask_path):
    """Get images and annotation info
    Input : a path of the COCO format file (.json)
    Output : 
        images(dict): image infomation with the associated annotations information
        images_info(dict): image information retrieved from the mask_path file
        annotations_info(dict): annotation information retrieved from the mask_path file
    """
    mask_info = json.load(open(mask_path))
    images_info = deepcopy(mask_info['images'])
    annotations_info = deepcopy(mask_info['annotations'])

    images = {}  # image_id : image_info
    annotations = {}  # image_id : [annotation_info]

    image_id = None

    for an in annotations_info:
        an_data = {
            "image_id": an["image_id"],
            "bbox": an["bbox"],
            "category_id": an["category_id"]
        }

        if image_id != an["image_id"]:
            # initialize
            image_id = an["image_id"]
            annotations[image_id] = []

        if not annotations[image_id]:
            annotations[image_id] = [an_data]
        else:
            annotations[image_id].append(an_data)

    for im in images_info:
        image_id = im['id']
        images[image_id] = im
        images[image_id]['annotations'] = annotations[image_id]

    return images, images_info, annotations_info


class ReplaceObject:
    def __init__(self, category_ids, category_keys, category_sample_paths, save_dir, png_save_dir):
        self.category_ids = category_ids
        self.category_keys = category_keys
        self.category_sample_paths = category_sample_paths
        self.save_dir = save_dir
        self.category_data = self.prepare_data()
        self.png_save_dir = png_save_dir

    def prepare_data(self):
        """Prepare data for augmenting by loading external dataset
        If an image format is "ndjson", the ouput will be an array of strokes.
        If an image format is "png" or "jpg", the output will be an array of the given image path.
        Output : 
            external_images(dict): infomation (stroke information or image path) from the external dataset
        """
        print("Preparing data for augmenting...")
        external_images = {}  # key: category_id, value: list of image paths and types
        for category_key in self.category_sample_paths:
            category_id = category_ids[category_key]
            data_array = []
            for sample in self.category_sample_paths[category_key]:
                image_format = sample["format"]
                image_path = sample["path"]
                if image_format == "ndjson":
                    raw_drawing = load_ndjson(
                        image_path)  # an array of strokes
                    strokes = [get_strokes(stroke) for stroke in raw_drawing]
                    for s in strokes:
                        data_array.append({"type": "stroke", "strokes": s})
                elif image_format in ["png", "jpg"]:
                    image_paths = glob.glob(
                        image_path + f"**/*.{image_format}")
                    for i in image_paths:
                        data_array.append({"type": "image", "images": i})
                else:
                    raise ValueError(
                        f"Unsupported image format: {image_format}")
            external_images[category_id] = data_array
        return external_images

    def replace_object(self, image_id, image_size, object_cocobox_info, object_category_ids):
        """Replace an object image from sample images
        Input :
            image_id(int): image id for the COCO format
            image_size(tuple): height, width
            object_cocobox_info(tuple): (min_x, min_y, width, height)
            object_category_ids(dict): category ids for the object to be replaced
        Output :
            new_image(PIL.Image): new image with the replaced objects
            annotations(List): annotation information for the new image
            class_layer(List): image layers of the replaced objects
        """
        # Step 1: Initialize a new image
        image_size = (535, 757)
        new_image = Image.new("RGBA", image_size, (255, 255, 255, 0))
        layers = []
        class_layer = []
        annotations = []
        class_list = []
        for cid, cocobbox in zip(object_category_ids, object_cocobox_info):
            class_list.append(cid)
            # Step 2: Sample an object image to be replaced in a layer
            category_sample_paths = self.category_data[cid]
            sample = random.choice(category_sample_paths)

            # Initialize a new layer
            layer = Image.new("RGBA", image_size)
            min_x, min_y, width, height = [int(item) for item in cocobbox]
            bbox_start = (min_x, min_y)

            while True:
                try:
                    if sample["type"] == "stroke":
                        strokes = sample["strokes"]
                        object, object_cocobbox, segmentations = get_stroke_alpha(
                            strokes)
                    elif sample["type"] == "image":
                        image = sample["images"]
                        object, object_cocobbox, segmentations = get_image_alpha(
                            image)
                    # Step 3: Resize the object image to the size of the original object
                    object, object_cocobbox, segmentations = resize_image(
                        object, object_cocobbox, segmentations, width, height, margin=0)

                    # Step 4: Paste the object image to the new image
                    object_cocobbox = [
                        bbox_start[0], bbox_start[1], object.size[0], object.size[1]]

                    layer.paste(object, bbox_start)

                except Exception as e:
                    print("Retry replacement", e)
                    sample = random.choice(category_sample_paths)
                    continue
                else:
                    annotation = {
                        "segmentation": segmentations,
                        "area": object.size[0] * object.size[1],
                        "iscrowd": 0,
                        "image_id": image_id,
                        "bbox": object_cocobbox,
                        "category_id": cid,
                    }

                    layers.append(layer)
                    annotations.append(annotation)
                    break

        # Step 5: Merge layers with alpha composition
        for layer in layers:
            class_layer.append(layer)
            new_image = Image.alpha_composite(new_image, layer)

        new_image = new_image.convert('RGB')
        return new_image, annotations, class_layer

    def run(self, image_info, new_image_id, synthesize_id):
        """Save new images and the correspunding COCO format with the replaced objects 
        for the given image information
        Input : 
            image_info(dict): image information with annotation information from the COCO format file
            new_image_id(int): id of the given image from the COCO format file
            synthesize_id(int): id of the newly synthesized image
        Output :
            new_image_info: "images" information of the synthesized image. This information will be saved in the COCO format file.
            new_annotations: "annotations" information of the synthesized image. This information will be saved in the COCO format file.
        """
        num_objects = len(image_info['annotations'])
        image_size = (image_info['height'], image_info['width'])

        bbox_size_info = []
        object_category_info = []

        # Aggreate the information of an object image
        for idx in range(num_objects):
            bbox_size_info.append(image_info['annotations'][idx]['bbox'])
            object_category_info.append(
                image_info['annotations'][idx]['category_id'])

        # Create a new image
        new_image, new_annotations, layers = self.replace_object(
            new_image_id, image_size, bbox_size_info, object_category_info)
        
        # Save a new image
        file_name = image_info['file_name'].replace(
            '.png', '') + f"_{synthesize_id}.png"
        new_image_path = self.save_dir + file_name
        new_image.save(new_image_path)

        new_image_info = {
            "file_name": file_name,
            "height": image_size[0],
            "width": image_size[1],
            "id": new_image_id
        }

        # Save a layer of the synthesized single object for the future use
        idx = 0
        for object_info, object_layer in zip(new_annotations, layers):
            # Add a layer for each object            
            new = Image.new("RGBA", (535, 757), (255, 255, 255, 0))
            new = Image.alpha_composite(new, object_layer)
            new = new.convert('RGB')
            
            cid = object_info['category_id']
            cname = category_keys[cid]
            file_name = image_info['file_name'].replace(
                '.png', f'-{cname}') + str(idx) + f"_{synthesize_id}.png"
            new_image_path = self.png_save_dir + file_name
            new.save(new_image_path)
            
            idx += 1

        return new_image_info, new_annotations


if __name__ == "__main__":
    root_dir = './' # your-project-path

    ############## parameters ##############
    # Usage:
    #  python scene_augmentator.py -N 10 \
    #   --save_dir dataset/augmentation/png/ \
    #   --mask_info_dir dataset/230530-train_6_classes-1399.json \
    #   --save_info_dir dataset/augmentation/230530-train_6_classes-1399-aug.json \
    #   --png_save_dir dataset/augmentation/object_png/
    parser = ArgumentParser()
    parser.add_argument('--save_dir',
                        help='Save path.', default='dataset/augmentation/curation/png/')
    parser.add_argument('--mask_info_dir',
                        help='Mask information path.', default='dataset/curation/train_6_classes.json')
    parser.add_argument('--save_info_dir',
                        help='Save COCO information path.', default='dataset/augmentation/curation/train_6_classes.json')
    parser.add_argument('--num_new_images', '-N',
                        help='Number of synthesized images.', default=10, type=int)
    parser.add_argument('--png_save_dir',
                        default='dataset/augmentation/curation/object_png',
                        help='Save path of a layer of the synthesized single object.'
                        )
    args = parser.parse_args()

    ############## Result save path ##############
    result_save_path = args.save_dir
    if os.path.exists(result_save_path):
        shutil.rmtree(result_save_path)
    os.mkdir(result_save_path)
    
    if os.path.exists(args.png_save_dir):
        shutil.rmtree(args.png_save_dir)
    os.mkdir(args.png_save_dir)

    ############## Get the standard COCO JSON format ##############
    mask_path = root_dir + args.mask_info_dir

    images, images_info, annotations_info = annotations_groupby_image(
        mask_path)

    ############## Image Augmentation ##############
    replace_object = ReplaceObject(
        category_ids, category_keys, category_sample_paths, result_save_path, args.png_save_dir)

    new_image_id = 0
    new_annotation_id = 0
    new_images = []
    new_annotations = []
    print("Start image augmentation")
    for image_id in tqdm(images):
        # Get image information
        image_info = images[image_id]
        
        # Synthesize new images
        for synthesize_id in range(args.num_new_images):
            new_image_info, new_annotation_info = replace_object.run(
                image_info, new_image_id, synthesize_id)
            if new_image_info is None:
                continue
            new_images.append(new_image_info)
            for an in new_annotation_info:
                an['image_id'] = new_image_info['id']
                an['id'] = new_annotation_id
                new_annotation_id += 1
            new_annotations.extend(new_annotation_info)
            new_image_id += 1

    ############## Save the new COCO JSON format ##############
    print("Saving the new COCO JSON format...")
    save_path = root_dir + args.save_info_dir
    mask_info = json.load(open(mask_path))

    mask_info['images'] = new_images
    mask_info['annotations'] = new_annotations
    json.dump(mask_info, open(save_path, 'w'))
