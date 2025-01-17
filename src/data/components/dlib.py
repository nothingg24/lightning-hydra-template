from genericpath import isdir
from torch.utils.data import Dataset
from typing import Optional
# from torchvision.io import read_image
# import cv2
import albumentations as A
import matplotlib.pyplot as plt
# from matplotlib.patches import Circle, Rectangle
# import PIL
from PIL import Image, ImageDraw
import torchvision.transforms.functional as TF
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os
import tarfile
from tqdm import tqdm
import numpy as np
from math import sqrt

class DLIB(Dataset):
  def __init__(self, transform: Optional[A.Compose] = None):
    self.data_dir = None
    self.img_labels = None
    self.transform = transform
    self.url = 'http://dlib.net/files/data/ibug_300W_large_face_landmark_dataset.tar.gz'
    self.file_name = 'ibug_300W_large_face_landmark_dataset.tar.gz'
    self.origin_path = 'data/dlib'
    self.folder_dir = 'ibug_300W_large_face_landmark_dataset'
    self.labels_file = 'labels_ibug_300W.xml'
    self.class_labels = []

    self.prepare_data()
    self.prepare_labels()

  def download(self):
    response = requests.get(self.url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    if not os.path.isdir(self.origin_path):
        os.makedirs(self.origin_path)
    with open(os.path.join(self.origin_path, self.file_name), 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

  def unzip(self):
    file = tarfile.open(os.path.join(self.origin_path, self.file_name))
    members = file.getmembers()
    progress = tqdm(members)

    for member in progress:
      file.extract(member, self.origin_path)
      progress.set_description(f"Extracting {member.name}")
    file.close()

  def prepare_data(self):
    if not os.path.isfile(os.path.join(self.origin_path, self.file_name)):
        self.download()
    if not os.path.isfile(os.path.join(self.origin_path, self.folder_dir, self.labels_file)):
        self.unzip()
    if os.path.isdir(os.path.join(self.origin_path, self.folder_dir)):
        self.data_dir = os.path.join(self.origin_path, self.folder_dir)

  def prepare_labels(self):
    if self.data_dir is None:
      self.prepare_data()

    if self.img_labels is None:
      labels_dir = os.path.join(self.data_dir, self.labels_file)
      xml_data = open(labels_dir, 'r').read()
      root = ET.XML(xml_data)
      data = []

      for image in root.findall('images/image'):
          file_name = image.get('file')
          img_width = image.get('width')
          img_height = image.get('height')

          row = {
              'File name': file_name,
              'Image width': img_width,
              'Image height': img_height,
          }

          for box in image.findall('box'):
              top = box.get('top')
              left = box.get('left')
              box_width = box.get('width')
              box_height = box.get('height')
              row.update({
                  'top': top,
                  'left': left,
                  'box_width': box_width,
                  'box_height': box_height,
              })

              for part in box.findall('part'):
                  name = part.get('name')
                  x = part.get('x')
                  y = part.get('y')

                  row.update({
                      f"Point {name}": (x, y)
                  })
                  self.class_labels.append(name)

          data.append(row)

      df = pd.DataFrame(data)
      if not df.empty:
        self.img_labels = df

  def __len__(self):
    if self.img_labels is None:
      self.prepare_labels()
    return len(self.img_labels)
  
  def parse_roi_box_from_landmark(self, pts):
      """calc roi box from landmark"""
      x = [pt[0] for pt in pts]  # x-coordinates
      y = [pt[1] for pt in pts]  # y-coordinates
      bbox = [min(x), min(y), max(x), max(y)]
      center = [(float(bbox[0]) + float(bbox[2])) / 2, (float(bbox[1]) + float(bbox[3])) / 2]
      radius = max(float(bbox[2]) - float(bbox[0]), float(bbox[3]) - float(bbox[1])) / 2
      bbox = [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius]
      
      llength = sqrt((bbox[2] - bbox[0]) ** 2 + (bbox[3] - bbox[1]) ** 2)
      center_x = (bbox[2] + bbox[0]) / 2
      center_y = (bbox[3] + bbox[1]) / 2
      
      roi_box = [0] * 4
      roi_box[0] = center_x - llength / 2
      roi_box[1] = center_y - llength / 2
      roi_box[2] = roi_box[0] + llength
      roi_box[3] = roi_box[1] + llength
      
      return roi_box

  def __getitem__(self, index):
    if index < 0 or index >= len(self):
      raise IndexError(f"Index {index} is out of range")

    if self.data_dir is None:
      self.prepare_data()
    if self.img_labels is None:
      self.prepare_labels()
      
    if self.data_dir is not None and self.img_labels is not None:
      img_path = os.path.join(self.data_dir, self.img_labels.iloc[index, 0])
      bbox = self.img_labels.loc[index, 'top':'box_height']
      landmark = self.img_labels.iloc[index, -68:]
      image = Image.open(img_path).convert('RGB')
      roi_box = self.parse_roi_box_from_landmark(landmark)
      area = (roi_box[0], roi_box[1], roi_box[2], roi_box[3])
      # width = int(float(bbox['box_width']) + float(bbox['box_width']) * 0.1)
      # height = int(float(bbox['box_height']) + float(bbox['box_height']) * 0.1)
      # left = int(float(bbox['left']) - float(width) * 0.05)
      # top = int(float(bbox['top']) - float(height) * 0.05)
      # left, top, width, height = int(bbox['left']), int(bbox['top']), int(bbox['box_width']), int(bbox['box_height'])
      # right = left + width
      # lower = top + height
      # area = (left, top, right, lower)
      image = image.crop(area)

      # image = np.asarray(image)
      keypoints = []
      for i in range(68):
        #  x = int(landmark[i][0]) - int(bbox['left'])
        #  y = int(landmark[i][1]) - int(bbox['top'])
        x = int(landmark[i][0]) - int(roi_box[0])
        y = int(landmark[i][1]) - int(roi_box[1])
        keypoints.append((x, y))
      keypoints = np.array(keypoints)
      # image = TF.to_tensor(image)
      # image = image.permute(1,2,0)
      # image = read_image(img_path)
      # sample = {'image': image, 'bbox': bbox, 'landmark': landmark}
      # if self.transform:
      #   image = self.transform(image=image, keypoints=keypoints)['image']
      #   landmark = self.transform(image=image, keypoints=keypoints)['keypoints']
      # sample = {'image': image, 'bbox': bbox, 'landmark': landmark}
      sample = {'image': image, 'landmark': keypoints}
    return sample
  
  @staticmethod
  def visual_keypoints(image: Image, keypoints: np.ndarray) -> None:
      plt.imshow(image)
      x_values = [x for x, y in keypoints]
      y_values = [y for x, y in keypoints]
      plt.scatter(x_values, y_values, s=10, marker='.', c='r')
      plt.axis('off')
      plt.savefig('test.png')
      plt.show()

  @staticmethod
  def image_annotation(image: Image, keypoints: np.ndarray)->Image:
     draw = ImageDraw.Draw(image)
     for i in range(keypoints.shape[0]):
        draw.ellipse(xy=(keypoints[i][0]-1, keypoints[i][1]-1, keypoints[i][0]+1, keypoints[i][1]+1), fill=(0, 255, 0))
     return image
     

if __name__ == '__main__':
  dlib = DLIB()
  sample = dlib[20]
  print(np.array(sample['image']).shape, sample['landmark'].shape)
  dlib.visual_keypoints(sample['image'], sample['landmark'])
  # img = dlib.image_annotation(sample['image'], sample['landmark'])
  # crop_image = sample['image']
  # crop_image.save('crop.jpg')
  # img.save('test.jpg')
  # dlib.visualize(0)
