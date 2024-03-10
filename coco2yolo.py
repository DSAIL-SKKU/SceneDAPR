from cgitb import text
import pandas as pd
import json
import shutil
import os
from pathlib import Path
from argparse import ArgumentParser
import cv2


class ConvertCOCOToYOLO:
    """
    - Modified from https://github.com/qwirky-yuzu/COCO-to-YOLO/blob/main/coco_to_yolo.py)
    """
    def __init__(self, img_folder, txt_folder, yolo_folder, json_path):
        self.img_folder = img_folder
        self.json_path = json_path
        self.txt_folder = txt_folder
        self.yolo_folder = yolo_folder

        data = json.load(open(self.json_path))
        self.imgid2file = {d['id']: d['file_name'] for d in data['images']}

    def get_img_shape(self, img_path):
        img = cv2.imread(img_path)
        try:
            return img.shape
        except AttributeError:
            print('error!', img_path)
            return (None, None, None)

    def convert_labels(self, img_path, x1, y1, x2, y2):
        """Parses label files to extract label and bounding box
        coordinates. Converts (x1, y1, x1, y2) KITTI format to
        (x, y, width, height) normalized YOLO format.
        """

        def sorting(l1, l2):
            if l1 > l2:
                lmax, lmin = l1, l2
                return lmax, lmin
            else:
                lmax, lmin = l2, l1
                return lmax, lmin

        size = self.get_img_shape(img_path)
        xmax, xmin = sorting(x1, x2)
        ymax, ymin = sorting(y1, y2)
        dw = 1./size[1]
        dh = 1./size[0]
        x = (xmin + xmax)/2.0
        y = (ymin + ymax)/2.0
        w = xmax - xmin
        h = ymax - ymin
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x, y, w, h)

    def convert(self, annotation_key='annotations', img_id='image_id', cat_id='category_id', bbox='bbox'):
        """Loop for running convert_labels with the given COCO format file.
        """
        # Enter directory to read JSON file
        data = json.load(open(self.json_path))

        check_set = set()

        # Retrieve data
        for i in range(len(data[annotation_key])):

            # Get required data
            image_id = data[annotation_key][i]['image_id']
            image_id = self.imgid2file[image_id].replace(
                '.png', '')
            category_id = f'{data[annotation_key][i][cat_id]}'
            bbox = data[annotation_key][i]['bbox']

            # Retrieve image.
            if self.img_folder == None:
                image_path = f'{image_id}.png'
            else:
                image_path = f'./{self.img_folder}/{image_id}.png'

            if not os.path.exists(image_path):
                continue

            # Convert the data
            kitti_bbox = [bbox[0], bbox[1],
                          bbox[2] + bbox[0], bbox[3] + bbox[1]]
            yolo_bbox = self.convert_labels(
                image_path, kitti_bbox[0], kitti_bbox[1], kitti_bbox[2], kitti_bbox[3])

            # Prepare for export

            filename = f'{self.txt_folder}/{image_id}.txt'
            content = f"{category_id} {yolo_bbox[0]} {yolo_bbox[1]} {yolo_bbox[2]} {yolo_bbox[3]}"

            # Export
            if image_id in check_set:
                # Append to existing file as there can be more than one label in each image
                file = open(filename, "a")
                file.write("\n")
                file.write(content)
                file.close()

            elif image_id not in check_set:
                check_set.add(image_id)
                # Write files
                file = open(filename, "w")
                file.write(content)
                file.close()


def data_split(img_folder, txt_folder, yolo_folder, split_file=None, test_ratio=0.4):
    """
    Splits the data into train and validation sets.
    """
    basepath = Path(img_folder)

    image_train_path = os.path.join(yolo_folder, "images/train")
    label_train_path = os.path.join(yolo_folder, "labels/train")

    if os.path.exists(image_train_path):
        shutil.rmtree(image_train_path)
    os.mkdir(image_train_path)

    if os.path.exists(label_train_path):
        shutil.rmtree(label_train_path)
    os.mkdir(label_train_path)

    if split_type != 'augmentation':
        image_val_path = os.path.join(yolo_folder, "images/val")
        label_val_path = os.path.join(yolo_folder, "labels/val")

        if os.path.exists(image_val_path):
            shutil.rmtree(image_val_path)
        os.mkdir(image_val_path)

        if os.path.exists(label_val_path):
            shutil.rmtree(label_val_path)
        os.mkdir(label_val_path)

    if split_type != 'augmentation':
        if split_file == '':
            print("No split file provided. Using default split.")
            images = list(basepath.iterdir())
            images = [str(img.stem) for img in images if img.suffix == '.png']
            print(len(images))
            train_size = int(len(images) * (1.0 - test_ratio))
            test_size = int(len(images) * test_ratio)
            train_index = images[:train_size]
            test_index = images[train_size:]
        else:
            df = pd.read_csv(split_file)
            train_index = df[df['dataset'] ==
                             'train']['id'].astype(str).tolist()
            test_index = df[df['dataset'] ==
                            'test']['id'].astype(str).tolist()
    else:
        images = list(basepath.iterdir())
        train_index = [str(img.stem) for img in images if img.suffix == '.png']

    # move labels
    for index in train_index:
        try:
            img = Path(os.path.join(img_folder, index + '.png'))
            txt = Path(os.path.join(txt_folder, index + '.txt'))
        except:
            pass
        else:
            if os.path.exists(img.resolve()) and os.path.exists(txt.resolve()):
                shutil.copy(img.resolve(), os.path.join(
                    image_train_path, img.name))
                shutil.copy(txt.resolve(), os.path.join(
                    label_train_path, txt.name))

    # summary train data
    images = Path(os.path.join(yolo_folder, f"images/train/"))
    images = [img for img in images.iterdir() if img.suffix == '.png']

    labels = Path(os.path.join(yolo_folder, f"labels/train/"))
    labels = [img for img in labels.iterdir() if img.suffix == '.txt']

    print("Train Images:", len(images))
    print("Train Labels:", len(labels))

    if split_type != 'augmentation':
        for index in test_index:
            try:
                img = Path(os.path.join(img_folder, index + '.png'))
                txt = Path(os.path.join(txt_folder, index + '.txt'))
            except:
                pass
            else:
                if os.path.exists(img.resolve()) and os.path.exists(txt.resolve()):
                    shutil.copy(img.resolve(), os.path.join(
                        image_val_path, img.name))
                    shutil.copy(txt.resolve(), os.path.join(
                        label_val_path, txt.name))

        # summary test data
        images = Path(os.path.join(yolo_folder, f"images/val/"))
        images = [img for img in images.iterdir() if img.suffix == '.png']

        labels = Path(os.path.join(yolo_folder, f"labels/val/"))
        labels = [img for img in labels.iterdir() if img.suffix == '.txt']

        print("Val Images:", len(images))
        print("Val Labels:", len(labels))


# To run in as a class
if __name__ == "__main__":
    ############## parameters ##############
    # Usage:
    #  python coco2yolo.py --img_folder dataset/png/ \
    #   --yolo_folder dataset/yolo/ \
    #   --coco_file dataset/230530-train_6_classes-1399.json \
    #   --split_file dataset/final-dataset-230530-dist-1399.csv
    parser = ArgumentParser()

    parser.add_argument('--img_folder',
                        help='Image path.', default='dataset/curation/png/', type=str)  # Don't skip the last slash
    parser.add_argument('--yolo_folder',
                        help='a path to save yolo format images.', default='dataset/curation/yolo/', type=str)  # Don't skip the last slash
    parser.add_argument('--coco_file',
                        help='COCO Format file name.', default='dataset/curation/train_6_classes.json', type=str)
    parser.add_argument('--split_file',
                        help='a meta data with train, test split', default='dataset/final-dataset-220525-dist.csv')
    parser.add_argument('--split_type',
                        help='original, augmentation', default='original')

    args = parser.parse_args()
    coco_file = args.coco_file
    yolo_folder = args.yolo_folder
    img_folder = args.img_folder
    split_file = args.split_file
    split_type = args.split_type

    txt_folder = '.tmp'

    ############## Result save path ##############
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)

    if not os.path.exists(yolo_folder):
        os.mkdir(yolo_folder)
        
    if not os.path.exists(yolo_folder + '/images'):
        os.mkdir(yolo_folder + '/images')
        
    if not os.path.exists(yolo_folder + '/labels'):
        os.mkdir(yolo_folder + '/labels')

    if os.path.exists(txt_folder):
        shutil.rmtree(txt_folder)
    os.mkdir(txt_folder)

    ConvertCOCOToYOLO(img_folder, txt_folder, yolo_folder, coco_file).convert()

    data_split(img_folder, txt_folder, yolo_folder, split_file)
