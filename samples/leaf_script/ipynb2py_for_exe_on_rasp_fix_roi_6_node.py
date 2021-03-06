#-----------------------------------------------------------
# -*- coding: utf-8 -*-
"""ipynb2py_for_exe_on_rasp.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1uEV9GUuTPfUE_OEprWpov4yTff-MBO2l
# """

# # %tensorflow_version 1.x

# # !pip install keras==2.2.4
# # !pip install h5py==2.10.0
# # !!pip install plantcv #for display just histogram

# # !pip3 uninstall keras-nightly
# # !pip3 uninstall -y tensorflow
# # !pip3 install keras==2.1.6
# # !pip3 install tensorflow-gpu==1.15.0
# # !pip3 install h5py==2.10.0

# import tensorflow as tf #should be version 1.15.0
# import keras # should be version 2.1.6
#-----------------------------------------------------------

import os #ปัจจุบัน ก็ต้องมารันที่ตรงนี้อนยุ่แล้ว
pwd_current_leaf_script = os.getcwd()
os.chdir(pwd_current_leaf_script)
# os.chdir('/content/drive/My Drive/_Mask_RCNN_more2class/IDV_MaskRCNN_Image_Segmentation-master/IDV_MaskRCNN_Image_Segmentation-master/samples/leaf_script') #ย้าย path ไปในโฟเดอร์ mrcnn

import sys
import random
import math
import re
import time
import numpy as np
#ปิด warnning tf
# https://stackoverflow.com/questions/57381430/synonym-of-type-is-deprecated-in-a-future-version-of-numpy-it-will-be-underst
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf #แล้ว error ก็ มาตามนี้
#https://github.com/tensorflow/tensorflow/issues/38800
#import tensorflow._api.v2.compat.v1 as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")
#ROOT_DIR = '\________mask_rcnn________\mask_rcnn_find_area_leaf'

MODEL_DIR = ROOT_DIR + '\logs\leaf20211206T0903'# windows \


# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library

#os.chdir(ROOT_DIR)

from mrcnn import utils
from mrcnn import visualize
# from mrcnn.visualize import display_images
import mrcnn.model as modellib #https://careerkarma.com/blog/python-syntaxerror-non-default-argument-follows-default-argument/ 'new class mAP
from mrcnn.model import log

# --- for colab

# insert at 1, 0 is the script path (or '' in REPL)

#**# immport file from diff foloder
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder

# import new_add_dataset_more                 #path at samples cell Load Validation Dataset
# #--- for colab

# # %matplotlib inline
os.chdir(pwd_current_leaf_script)

import config_leaf_pc           #$ for import class LEAFconfig
config = config_leaf_pc.LEAFConfig()   #$ file main
# Override the training configurations with a few
# changes for inferencing.
class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
# config.display()

# Device to load the neural network on.
# Useful if you're training a model on the same 
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"

# https://towardsdatascience.com/mask-rcnn-implementation-on-a-custom-dataset-fd9a878123d4
# 6. setup 
# inference for test model

def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

# load weight
# Create model in inference mode
with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                              config=config)
    
# Set path to weights file
# Download file from the Releases page and set its path
# https://github.com/matterport/Mask_RCNN/releases

weights_path = MODEL_DIR+'/mask_rcnn_leaf_0013.h5'
# print(weights_path)
# Load weights
#print("Loading weights ", weights_path)
model.load_weights(weights_path, by_name=True)

import cv2
# from google.colab.patches import cv2_imshow # for colab
import numpy as np
import argparse

# detect image follow path do arg

#--
# file_image_test = '27.jpg'
# path = '/content/drive/My Drive/_Mask_RCNN_more2class/IDV_MaskRCNN_Image_Segmentation-master/IDV_MaskRCNN_Image_Segmentation-master/samples/leaf_script/new_add_dataset_more/mask_image'
# image_new = cv2.imread(os.path.join(path,file_image_test))
#--

#node-red 
# stdIN_args_filename = sys.stdin.readline()

# pwd_current_leaf_script = os.getcwd() # should be /../../leaf_script

# parser = argparse.ArgumentParser(description='Find Area Pixel from Image ***run at path leaf_script***', epilog='just use >>> python try.py --image "name_image.jpg" ')

# parser.add_argument("--Path_image2find_area", default=pwd_current_leaf_script +'/new_add_dataset_more/test_image/')
# parser.add_argument("--filename", default="3.jpg")

# args = parser.parse_args()
#print("check if path '/' it is windows")
#print("but path like this '\' is linux")
#print("path and image file =>"+args.Path_image2find_area+args.filename)

#cmd anaconda
# image_new = cv2.imread(args.Path_image2find_area+args.filename)
# print("1")
stdIN_filename_str_trimed = str(sys.stdin.readline()).strip()
# print(len(stdIN_filename))
# print(len('3.jpg'))
# print(stdIN_filename.strip())

path_ = r"D:/________mask_rcnn________2/find_area_pixel_leaf_/samples/leaf_script/new_add_dataset_more/test_image/"
path_name = path_+ stdIN_filename_str_trimed #'3.jpg' # stdIN_filename
# print(path_name)
image_new = cv2.imread(path_name)

image_new2rgb = cv2.cvtColor(image_new, cv2.COLOR_BGR2RGB)

results1 = model.detect([image_new2rgb], verbose=0) #1 for show detail

# Display results
# ax = get_ax(1)
r1 = results1[0]

if r1['rois'].shape[0] != 6:
  print("model detect wrong cause this image have more\less 6 roi \n   please change weight model this model can't find roi in right position with this image")
else: #do the same 
  #visualize.display_instances(image_new2rgb, r1['rois'], r1['masks'], r1['class_ids'], r1['scores'], ax=ax, title="Predictions1")

  os.chdir(pwd_current_leaf_script +'/mask_image_from_test_input')# ย้ายไปโฟเดอร์ที่จะเซฟภาพ

  # file_image_test = args.filename #
  file_image_test = stdIN_filename_str_trimed
  # Create directory
  dir_name_create = file_image_test.split('.')[0]
  try:
      # Create target Directory
      os.mkdir(dir_name_create)
     # print("Directory " , dir_name_create ,  " Created ") 
  except FileExistsError:
    # print("Directory " , dir_name_create ,  " already exists")
      pass


  #---each fn from vis file
  # import colorsys =>เพื่อที่จะใช้ fn hsv_to_rgb ก็สร้างให้เลย
  from PIL import Image, ImageDraw, ImageFont# save mode 

  def hsv_to_rgb(h, s, v):
      if s == 0.0: return (v, v, v)
      i = int(h*6.) # XXX assume int() truncates!
      f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
      if i == 0: return (v, t, p)
      if i == 1: return (q, v, p)
      if i == 2: return (p, v, t)
      if i == 3: return (p, q, v)
      if i == 4: return (t, p, v)
      if i == 5: return (v, p, q)

  def random_colors(N, bright=True):
      """
      Generate random colors.
      To get visually distinct colors, generate them in HSV space then
      convert to RGB.
      """
      brightness = 1.0 if bright else 0.7
      hsv = [(i / N, 1, brightness) for i in range(N)]
      colors = list(map(lambda c: hsv_to_rgb(*c), hsv))
      random.shuffle(colors)
      return colors

  def apply_mask(image, mask, color, alpha=0.5):
      """Apply the given mask to the image.
      """
      for c in range(3):
          image[:, :, c] = np.where(mask == 1,
                                    image[:, :, c] *
                                    (1 - alpha) + alpha * color[c] * 255,
                                    image[:, :, c])
      return image

  def save_mask_instance(image, image_name, boxes, masks, class_ids, scores, class_names, filter_classs_names=None,
                scores_thresh=0.1, save_dir=None, mode=0):
      """
          image: image array
          image_name: image name
          boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
          masks: [num_instances, height, width]
          class_ids: [num_instances]
          scores: confidence scores for each box
          class_names: list of class names of the dataset
          filter_classs_names: (optional) list of class names we want to draw
          scores_thresh: (optional) threshold of confidence scores
          save_dir: (optional) the path to store image
          mode: (optional) select the result which you want
                  mode = 0 , save image with bbox,class_name,score and mask;
                  mode = 1 , save image with bbox,class_name and score;
                  mode = 2 , save image with class_name,score and mask;
                  mode = 3 , save mask with black background;
      """
      mode_list = [0, 1, 2, 3]
      assert mode in mode_list, "mode's value should in mode_list %s" % str(mode_list)

      if save_dir is None:
          save_dir = os.path.join(os.getcwd(), "output")
          if not os.path.exists(save_dir):
              os.makedirs(save_dir)

      useful_mask_indices = []

      N = boxes.shape[0]
      if not N:
          print("\n*** No instances in image %s to draw *** \n" % (image_name))
          return
      else:
          assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

      for i in range(N):
          # filter
          class_id = class_ids[i]
          score = scores[i] if scores is not None else None
          if score is None or score < scores_thresh:
              continue

          label = class_names[class_id]
          if (filter_classs_names is not None) and (label not in filter_classs_names):
              continue

          if not np.any(boxes[i]):
              # Skip this instance. Has no bbox. Likely lost in image cropping.
              continue

          useful_mask_indices.append(i)

      if len(useful_mask_indices) == 0:
          print("\n*** No instances in image %s to draw *** \n" % (image_name))
          return

      colors = random_colors(len(useful_mask_indices))

      if mode != 3:
          masked_image = image.astype(np.uint8).copy()
      else:
          masked_image = np.zeros(image.shape).astype(np.uint8)

      if mode != 1:
          for index, value in enumerate(useful_mask_indices):
              masked_image = apply_mask(masked_image, masks[:, :, value], colors[index])

      masked_image = Image.fromarray(masked_image)

      if mode == 3:
          masked_image.save(os.path.join(save_dir, '%s.jpg' % (image_name))) #save mask
          return

      draw = ImageDraw.Draw(masked_image)
      colors = np.array(colors).astype(int) * 255

      for index, value in enumerate(useful_mask_indices):
          class_id = class_ids[value]
          score = scores[value]
          label = class_names[class_id]

          y1, x1, y2, x2 = boxes[value]
          if mode != 2:
              color = tuple(colors[index])
              draw.rectangle((x1, y1, x2, y2), outline=color)

          # Label
          font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
          draw.text((x1, y1), "%s %f" % (label, score), (255, 255, 255), font)

      masked_image.save(os.path.join(save_dir, '%s.jpg' % (image_name)))     

  #---
  # #---https://github.com/matterport/Mask_RCNN/pull/38
  #save in directory
  Path_keep_file_mask_test = pwd_current_leaf_script + '/mask_image_from_test_input/' + dir_name_create

  name_mask_in = '_mask_instance_segmentation'
  image_name = file_image_test.split('.')[0] + name_mask_in

  save_mask_instance(image_new2rgb, image_name, r1['rois'], r1['masks'],
    r1['class_ids'],r1['scores'],class_names=['BG', 'green', 'red'], # depen on class your name 
    filter_classs_names=['green', 'red'],scores_thresh=0.5,save_dir=Path_keep_file_mask_test,mode=3) #it's can save mask instance #

  #print('Save mask instance in folder "' + dir_name_create +'" successfully')

  # สร้างตัวแปรให้ fix ขนาดให้ขนาดเท่ากับข้อมูล ของ x,y ให้เหมือนกับ r1['rois'] >>> แต่ fix ขนาดให้เหลือ 6 roi <<<<

  sort_roi = np.zeros(( 6 , r1['rois'].shape[1])) # 6 roi กับ 4 ตัวแปร x,y

  # แปลงชนิด ของค่าที่ได้จาก DL ที่ยังไม่ได้เรียงจาก array มาอยู่ในรูปแบบ list 
  #โดย ทำ copy เหมือนสร้างตัวแปรใหม่ เพื่อนำค่าตัวแปรนี้ array_roi2list_copy จากค่าของ r1['rois'] ไปใส่ ใน sort_roi ให้ถูกลำดับเซ็นเตอร์ เพื่อที่จะใช้ sort_roi แทน r1['rois']
  array_roi2list_copy = r1['rois'].tolist().copy()

  # วน อ่านที่ละ roi และเก็บค่าในตัวแปร to_compare_center_
  to_compare_center_X = []
  to_compare_center_Y = []

  #เราต้องการวนหาทุกค่า center และหาค่าทั้งหมดที่ตัว DL ให้มา
  #ในที่นี้จะวนหาค่า center ทั้งหมด แล้วใส่ตัวแปรด้านบน
  for roi in range(0,r1['rois'].shape[0]): 
    x_start = array_roi2list_copy[roi][1]
    y_start = array_roi2list_copy[roi][0]
    x_end =  array_roi2list_copy[roi][3]
    y_end =  array_roi2list_copy[roi][2]

    center_x = (x_start + x_end) /2
    center_y = (y_start + y_end) /2
    
    to_compare_center_X.append(center_x)
    to_compare_center_Y.append(center_y)

  # ได้ centerของทั้ง x, y แล้วจะนำมาเปรียบเทียบ

  XY_center_zip = zip(to_compare_center_X,to_compare_center_Y)

  XY_center_zip_list = list(XY_center_zip)

  sorted_y_from_XY_center_zip_list = sorted(XY_center_zip_list,key=lambda XY_center_zip_list:XY_center_zip_list[1]) #Y

  #เลือก แค่3 roi บน ที่เรียงค่า Y มาแล้ว เพราะเรารู็ว่า y 3 อันแรก จะน้อยสุด จึงใช้ sort เลย
  # ได้ค่าของภาพด้านบน
  sorted_y_from_XY_center_zip_list_up = sorted_y_from_XY_center_zip_list[:3]

  # แล้วก็นำมาเรียงในแกน x อีกที เพื่อดูว่า x น้อยมาก่อน และตามลำดับ
  sorted_y_from_XY_center_zip_list_up_x = sorted(sorted_y_from_XY_center_zip_list_up,key=lambda sorted_y_from_XY_center_zip_list_up:sorted_y_from_XY_center_zip_list_up[0]) #X

  #เลือก แค่3 roi ล่าง ที่เรียงค่า Y มาแล้ว เพราะเรารู็ว่า y 3 อันท้าย จะมากสุด 
  sorted_y_from_XY_center_zip_list_down = sorted_y_from_XY_center_zip_list[3:]

  sorted_y_from_XY_center_zip_list_down_x = sorted(sorted_y_from_XY_center_zip_list_down,key=lambda sorted_y_from_XY_center_zip_list_down:sorted_y_from_XY_center_zip_list_down[0]) #X

  list_condition = sorted_y_from_XY_center_zip_list_up_x + sorted_y_from_XY_center_zip_list_down_x

  #รอบแรกๆ
  #มาทำเงื่อนไขได้ดังนี้ คือเทียบค่าที่เป็น center จริงๆ ของ array_roi2list_copy ถ้าตรงกับเงื่อนไข ใดใน
  for i in range(0,6):
    for j in range(0,6):                                                              # list_condition ก็ให้ตัว sort_roi ตัวนั้น คือค่าที่ตรงเงื่อนไข
      if( (array_roi2list_copy[i][1] + array_roi2list_copy[i][3])/2 == list_condition[j][0] and (array_roi2list_copy[i][0] + array_roi2list_copy[i][2])/2 == list_condition[j][1] ):
        sort_roi[j] = array_roi2list_copy[i]
  sort_roi = np.int32(sort_roi)

  os.chdir(pwd_current_leaf_script + '/mask_image_from_test_input/'+ dir_name_create)# ทำ apply mask จากmaskที่เซฟมา

  # apply_mask

  ##0  image_new is image input (check in Load image for Test Model)
  input_image_copy_for_apply_mask = image_new.copy()  #2

  #1 image_mask_instance
  image_mask_instance_cv = cv2.imread(file_image_test.split('.')[0]+'_mask_instance_segmentation.jpg') #1

  #ใช้ shape ของภาพต้นฉบับ 
  # dim = (width, height)
  dim_origin = image_new.shape[1], image_new.shape[0] 

  #--- Resizing the image_mask_instance_cv to the shape of image_new --- #1
  mask_instance_re = cv2.resize(image_mask_instance_cv, dim_origin)#มา resize image_mask_instance_cv ให้ shape เท่ากับต้นฉบับ                     # ซ่ึ่งภาพนี้มี background สีดำ

  # change #1 to gray scale
  mask_instance_re_binary = cv2.cvtColor(mask_instance_re, cv2.COLOR_BGR2GRAY) 

  # --- Apply THRESH_BINARY threshold of the logo binrary image ---
  ret, mask_instance_re_binary_th = cv2.threshold(mask_instance_re_binary, 5, 255, cv2.THRESH_BINARY) 
  # ถ้า ues _INV เพื่อที่จะสลับจาก mask_instance ที่มี ให้กลายเป็นให้เหลือพื้นที่ไว้ เพื่อเอาพื้นที่ของภาพต้นฉบับ

  #--- Copy pixel values of mask_instance_re to input_image_copy_for_apply_mask wherever the mask is black ---
  # input_image_copy_for_apply_mask #2
  input_image_copy_for_apply_mask[np.where(mask_instance_re_binary_th == 0)] = mask_instance_re[np.where(mask_instance_re_binary_th == 0)]    #$$
                # ในภาพต้นฉบับ ตามที่มีค่า 0 ของภาพ  mask_instance_re_binary_th    #นำสีดำมาทับ 

  #save apply mask
  Path_keep_file_mask_test = pwd_current_leaf_script + '/mask_image_from_test_input/'+ dir_name_create #real_test_2/'+ dir_name_create 

  name_apply_mask_ = '_apply_mask_'

  background = 'black_.jpg'
  file_name_apply_mask = file_image_test.split('.')[0] + name_apply_mask_ + background

  # Saving the image with name and path
  cv2.imwrite(os.path.join(Path_keep_file_mask_test  , file_name_apply_mask), input_image_copy_for_apply_mask)

  import pandas as pd
  from PIL import *
  # import seaborn as sns #ไม่จำเป็น
  # import matplotlib.pyplot as plt #แล้ว

  # จัดการกับพื้นหลัง 
  current = pwd_current_leaf_script + '/mask_image_from_test_input/' + dir_name_create #real_test_2/' + dir_name_create  #real_test_2
  os.chdir(current)

  path_apply = current +  "/"+file_image_test.split('.')[0]+"_apply_mask_black_.jpg"
  apply_cv = cv2.imread(path_apply)

  # Function to Detection Outlier on one-dimentional datasets.
  def find_anomalies(data):
  
      dataOject = data[data>1]
      
      # define a list to accumlate anomalies
      anomalies = []

      # Set upper and lower limit
      # For Normal distributions:
      # lower_limit
      # upper_limit
      
      # For Skewed distributions:
      percentile25 = dataOject.quantile(0.25)
      percentile75 = dataOject.quantile(0.75)
      iqr = percentile75 - percentile25
      lower_limit = percentile25 - (1.5 * iqr)
      upper_limit = percentile75 + (1.5 * iqr)

      # Generate outliers
      for outlier in data:
          if outlier > upper_limit or outlier < lower_limit:
              anomalies.append(0) # outlier
          else: anomalies.append(outlier) # object
      return np.array(anomalies)

  #test
  # apply_cv_ = cv2.imread('/content/drive/My Drive/_Mask_RCNN_more2class/IDV_MaskRCNN_Image_Segmentation-master/IDV_MaskRCNN_Image_Segmentation-master/samples/leaf_script/mask_image_from_test_input/500/500_apply_mask_black_.jpg')
  # rgb_image = cv2.cvtColor(apply_cv_, cv2.COLOR_BGR2RGB)

  #เนื่องจาก opencv อ่านภาพมาเป็น bgr ต้องการ mode rgb จึงต้อง convert
  rgb_image = cv2.cvtColor(apply_cv, cv2.COLOR_BGR2RGB)
  # แยก chanel สี ของ rgb 
  r, g, b = cv2.split(rgb_image)

  #เก็บอยู่ในรูปแบบ ตารางข้อมูล
  df = pd.DataFrame()
  df['red'] = r.reshape(-1)
  df['green'] = g.reshape(-1)
  df['blue'] = b.reshape(-1)

  # นำค่าแต่ละ chanel เข้าฟังชัน
  df.red = find_anomalies(df.red)
  df.blue = find_anomalies(df.blue)
  df.green = find_anomalies(df.green)

  df.loc[(df.red==0) | (df.green==0) | (df.blue==0), ['red', 'green', 'blue']] = [0,0,0] #ถ้าค่าที่ array ไหน ในแต่ละ channel มีค่า = 0 จะใส่สีดำ
  # print(type(df.red)) #<class 'pandas.core.series.Series'>
  # print(type(df.red.values)) #<class 'numpy.ndarray'>

  _r = df.red.values.reshape(apply_cv.shape[:2]).astype('uint8')
  _g = df.green.values.reshape(apply_cv.shape[:2]).astype('uint8')
  _b = df.blue.values.reshape(apply_cv.shape[:2]).astype('uint8')

  newImage_apply_rm_outliers = cv2.merge((_r, _g, _b))

  #save newImage_apply_rm_outliers with                           new file name                    image in rgb
  file_name_apply_mask_rm_outliers = file_image_test.split('.')[0] + name_apply_mask_ + "rm_outliers_" + background
  newImage_apply_rm_outliers_rgb = cv2.cvtColor(newImage_apply_rm_outliers, cv2.COLOR_BGR2RGB)

  cv2.imwrite(os.path.join(Path_keep_file_mask_test  , file_name_apply_mask_rm_outliers), newImage_apply_rm_outliers_rgb)

  #== นำที่ตัดพื้นหลังไปทำต่อ
  apply_cv_rm_outliers_lab = cv2.cvtColor(newImage_apply_rm_outliers, cv2.COLOR_BGR2LAB)

  # ทำเป็นฟังชัน เป็นการกรอง noise ออก โดยเลือก area ของ contour ที่มีค่ามากกว่ size2filter ที่ต้องการ ***
  def delete_noise_(blackAndWhiteImage, size2filter, height, width):
    blackAndWhiteImage_copy = blackAndWhiteImage.copy()
    #หา contour จาก mask
    # cnt_   = cv2.findContours(blackAndWhiteImage_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1] #in colab
    cnt_ ,hierarchy_ = cv2.findContours(blackAndWhiteImage_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #สร้าง ภาพสีดำตาม ขนาดภาพที่ผ่านเข้ามา
    filterNoise = np.zeros(blackAndWhiteImage.shape[:2], dtype="uint8")
      
    color_black = (0,0,0)
    color_white = (255,255,255)

    for i in range(len(cnt_)): # ต้องวนอ่าน ค่าพิกัด x,y จาก จำนวนคอนทัว ทั้งหมดก่อน
      area_ = cv2.contourArea(cnt_[i]) # หาพื้นที่ ทุกคอนทัว
      # print(area_)
      if area_ > size2filter: # พื้นที่ ที่มากกว่า size2filter ที่กำหนดมา
        cnt_filter = cnt_[i] # กำหนด ค่า cnt ใหม่ โดยในที่นี้จะเป็นค่าที่อยู้ในเงื่อนไขแล้ว ***
        # print(cnt_) # คือพิกัด 
        # print(i) #จำนวน คอนทัว ทั้งหมด
        # print(area) # พื้นที่
        cv2.drawContours(image=filterNoise, contours=[cnt_filter], contourIdx=-1, color=color_white, thickness=cv2.FILLED)  
    
    dim_origin = width, height  
    filterNoise_re = cv2.resize(filterNoise, dim_origin)
    return filterNoise_re

  count = 0 

  max_find_maxL = []

  min_find_min_a = [] 
  max_find_max_a = []

  #1. วนที่ละ rois ตามตำนวน rois ที่ deep detect ได้
  for i in range(6):#(r1['rois'].shape[0]):

    x_start = sort_roi[i][1] #
    y_start = sort_roi[i][0]
    x_end =  sort_roi[i][3]
    y_end = sort_roi[i][2]
    refPt = [(x_start, y_start), (x_end, y_end)]

    #--  นำค่าจาก rois จาก apply
    rois_apply = apply_cv_rm_outliers_lab[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]].copy() #for vs old=> #apply_cv_lab[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]] #intersection #applys for find valuse min max each rois in mode lab                                 #

    channel = ["l_channel","a_channel","b_channel"]

    #get min max in lab color space จากภาพ ใน mode lab จาก apply_mask โดยไปวนทีละ rois *อยู่ในลูป ค่าก็จะรีใหม่ ถ้าเปลี่ยนroi* 
    min_lab_threshold_apply_each = []
    max_lab_threshold_apply_each = []

    for j, lab in enumerate(channel):
      # print(np.max(apply_cv_lab[:,:,i]))
      min_each = np.min(rois_apply[:,:,j])
      max_each = np.max(rois_apply[:,:,j])

      min_lab_threshold_apply_each.append(min_each)
      max_lab_threshold_apply_each.append(max_each) #เก็บในตัวแปรmax_lab_threshold_apply_each แล้วเอาค่าที่อ่านได้มาใช้ใน inRange เลย ตาม index

    #-- นำค่า ต้นฉบับมา เพื่อเป็นตัวเลือกอีกที โดยใช้ค่าจาก mask_apply
    #  ซึ่งตัวมันเองจะต้องแปลงเป็น mode lab เพื่อที่จะให้ value ที่เราได้ค่ามาเป็น lab ไปเลือก labต้นฉบับ จะได้ถูกต้อง
    input_cv_lab = cv2.cvtColor(image_new, cv2.COLOR_BGR2LAB)
    
    rois_origin_lab = input_cv_lab[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]].copy() # orining rois                            # image to 8 color # สามารถเปลี่ยนภาพต้นนี้ เพื่อทำการเปรียบเทียบ mask ที่ได้

    #  #2. use min max range from apply_mask each
    #ทำ threshold -+ 10 เหมือนขยายช่วงเพิ่มอีก 10 ค่า
    thresh = 10
    
    #  ใช้ค่าจาก *mask_apply* ที่แปลงเป็นค่าของ lab แล้ว แต่ละ rois (แต่จะเขียนโค้ดไปดึงค่า 3 ตัวแรก เพราะค่า lab ที่ได้มา มันเท่ากันทั้งภาพ)
    # L เอาค่าที่น้อยสุด ที่ได้จาก apply_mask และมากสุด กำหนด L เท่ากับ 255 
    # ***a คือช่วงสี เขียวไปถึงแดง ช่วงที่เราสนมากที่สุด จึงใช้ค่าจาก ที่ได้ และขยายช่วงเพิ่ม * 
    # b ที่ต้องคูณ 2 ที่ min เพราะ จะ- 255 คือไม่เอาช่วงสีน้ำเงิน

    if rois_origin_lab.shape[0]*rois_origin_lab.shape[1] < 400*400 :
      minLAB_ = np.array([min_lab_threshold_apply_each[0] , min_lab_threshold_apply_each[1] - thresh , 135])  #ถ้าภาพเล็ก ควรจะมีค่าช่วงที่ b น้อย คือ 135ขึ้นไป ถึง 255 ถ้าภาพใหญ่ควรค่าน้อย เพราะเป็นเรื่องblack ground
      maxLAB_ = np.array([max_lab_threshold_apply_each[0] , max_lab_threshold_apply_each[1] + thresh , 255])
      size = 100 # size ที่ต้องการกรอง

    else : # ถ้าขนาด roi ของภาพใหญ่ขึ้น แสดงว่าวัตถุใน roi มีขนาดใหญ่ขึ้น (ไม่ค่อยเห้น พื้นหลัง) ก็ไม่ต้องกรองพื้นหลังละเอียด ใส่ค่าใน ch b ให้น้อย
      minLAB_ = np.array([min_lab_threshold_apply_each[0] , min_lab_threshold_apply_each[1] - thresh , 128])  #ถ้าภาพเล็ก ควรจะมีค่าช่วงที่ b น้อย คือ 135ขึ้นไป ถึง 255 ถ้าภาพใหญ่ควรค่าน้อย เพราะเป็นเรื่องblack ground
      maxLAB_ = np.array([max_lab_threshold_apply_each[0] , max_lab_threshold_apply_each[1] + thresh , 255])
      size = 2000

    if i == 0 :
      if maxLAB_[0] == 0:
        maxLAB_[0] = 210 
  #--------------------------------------------------------------------------------------------
    # can comment for check no mask instance
    # ทำการเก็บค่า min ของ channel a  จาก apply mask  ถ้ากรณี roi ที่ไม่มี mask instance ก็ให้ใช้ค่า min max ตรงนี้
    if minLAB_[1] != 0 : #a จะเท่ากับ 0 ก็ต่อเมื่อไม่มี apply mask 
      min_find_min_a.append(minLAB_[1])
    # ทำการเก็บค่า max ของ channel a
    max_find_max_a.append(maxLAB_[1])

    # ทำการเก็บค่า max ของ channel L 
    max_find_maxL.append(maxLAB_[0])

  # ถ้าเข้าเงื่อนไข ตรงนี้ แปลว่า ค่าที่มาจาก apply_mask ตัว DL detect ไม่เจอ จึงต้องกำหนดค่าใหม่ (ค่าจากตัวแปรด้านบน) ดังนั้น
    if minLAB_[0] == 0 : #ถ้า roi เข้าเงื่อนไข ก็ให้ใช้ค่าmin max ที่เก็บจากแต่ละ roi ด้านบน
      if maxLAB_[0] == 0 :

        # if minLAB_[0] == 0: # แสดงว่า ไม่มีแสง เพราะ DL detect ไม่เจอ
        minLAB_[:] = ([         0          , min(min_find_min_a)   , 133])

        # if maxLAB_[0] == 0: # แสดงว่า ไม่มีแสง เพราะ DL detect ไม่เจอ กำหนดให้เป็นทุกค่าความสว่าง ก้คือค่าที่ fix ว่าเป็น 255 
        maxLAB_[:] = ([max(max_find_maxL)  , max(max_find_max_a) , 255])

  # # ต่อยอดอีก คือ ถ้า 255 แล้วค่ามันเยอะกว่า benchmark มาก ก็ให้้ใช้ ค่าที่ได้จาก roi each mask apply
  #แสงเยอะ ภาพต้นยิ่งเล็ก => ผิดพลาดสูง แต่ถ้า ใช้ค่าทุกช่วงแสง ภาพต้นใหญ่ detect ดี

  # ทำเงื่อนไข 
    # ถ้ารูปใหญ่ b มีค่าน้อย 127-130
    # ถ้ารูปเล็ก ให้ค่าb มีค่ามาก 133-137

    # ## +++ add Seclect Range in image roi
    maskAll_test = cv2.inRange(rois_origin_lab, minLAB_, maxLAB_) # เลือกช่วงสีโดยใช้ค่าสีจาก apply mask ของเรา กับภาพต้นฉบับ (ลองเปลี่ยนภาพต้นฉบับให้มีค่าสีน้อย)

    #------------------#------------------#------------------#------------------#------------------#------------------#------------------#------------------
    maskAll_test_del_noise = delete_noise_(maskAll_test, size, maskAll_test.shape[1], maskAll_test.shape[0])                               ### fn noise new

  # #------------------
    #เอาที่กรองแล้ว ไปเซฟ เพื่อหา พื้นที่ต่อไป

    #เซฟรูป แต่ละ mask ของ แต่ละ roi  ใน folder ใหม่อีกที #@@
    #Create directory สำหรับเก็บ ไฟล์ roi แต่ละ mask
    dir_name_create_each_mask_lab =  file_image_test.split('.')[0] + '_roi_each_lab'# 49_roi_each_lab                     ************** ชื่อโฟเดอร์ ในpath cell above
    try:
        # Create target Directory
        os.mkdir(dir_name_create_each_mask_lab)
        # print("Directory " , dir_name_create_each_mask_lab ,  " Created ") 
    except FileExistsError:
        # print("Directory " , dir_name_create_each_mask_lab ,  " already exists")
        pass

  # #---https://github.com/matterport/Mask_RCNN/pull/38
  #save in directory
    Path_keep_file_each_mask_lab =  pwd_current_leaf_script + '/mask_image_from_test_input/' + dir_name_create + '/'  + dir_name_create_each_mask_lab #real_test_2/

    file_name_each_roi_mask_lab = file_image_test.split('.')[0] + '_roi_'+ str(count+1) + '.jpg'   # numberImage_roi_i.jpg
    cv2.imwrite(os.path.join(Path_keep_file_each_mask_lab , file_name_each_roi_mask_lab),  maskAll_test_del_noise)

    count = count + 1

  # เข้ามาใน folder ที่สร้าง mask แต่ละ roi เพื่อหาค่า area pixel
  os.chdir(Path_keep_file_each_mask_lab)

  import os , os.path # count file

  path_load_mask_each = Path_keep_file_each_mask_lab
  count = 0

  #count file in folder

  #path joining version for other paths
  DIR = pwd_current_leaf_script + '/mask_image_from_test_input/' + dir_name_create + '/'  + dir_name_create_each_mask_lab
  # print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])) #6 จำนวนไฟล์ภาพ roi

  #
  # https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python

  list_area_image_lab_ = [] # keep value area

  for i in range(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])):

    roi_look_like_binary = cv2.imread(os.path.join(path_load_mask_each , file_image_test.split('.')[0] + '_roi_'+ str(count+1)+ '.jpg'))

    # print("roi_"+str(count+1)) #name => image_n
    # print("after delete noise")

    hsv = cv2.cvtColor(roi_look_like_binary, cv2.COLOR_BGR2HSV)                                                             #
    # gray_image = cv2.cvtColor(roi_look_like_binary, cv2.COLOR_BGR2GRAY)                               ##

    lower_ = np.array([0,0,200] ,dtype = "uint8")  #  เลือกช่วงค่าในโหมด HSV 
    upper_ = np.array([255,255,255], dtype = "uint8") #

    mask = cv2.inRange(hsv, lower_, upper_)# down shape to binary # just hsv rgb lab                                   #

    # contours1  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]   #ถ้าไม่ใส่ [1] จะerror array is not a numerical tuple #จะเกิดใน colab น่าจะเป็นที่ เวอชั่น python
    contours1, hierarchy1  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours1) <1:
      print('this image have no mask')
      print("\n")
    else:
      for c in range(0,len(contours1)):
        cnt = contours1[c]
        m = cv2.moments(cnt)

        #---
        # if m['m00'] > 500:
        #   list_area_image_lab_.append(m['m00'])
        #   print("area of roi_"+ str(count+1) +" = "+ str(m['m00']) +'\n')
        #---
        
        if mask.shape[0] * mask.shape[1] <= 250000 :# 500*500  คือถ้าภาพmask shape น้อยกว่า 500*500 ก็ให้ปริ้นค่า 
          
          if m['m00'] > 3600: #60x60
              list_area_image_lab_.append(m['m00'])
              print("area of roi_"+ str(count+1) +" = "+ str(m['m00']) )
          else :
              # print(m['m00'])  # เป็น noise แต่ละจุด ที่ทำmask ได้ไม่ดีพอ ซึ่งก็ไม่ได้มารวมอยู่แล้ว
              pass
        else : # ภาพmask ที่ใหญ่ ก็ให้ใช้ค่ามาก
            
            if m['m00'] > 25000 : #7000: #50x100
              list_area_image_lab_.append(m['m00'])
              print("area of roi_"+ str(count+1) +" = "+ str(m['m00']) )
            else :
              # print(m['m00'])  # เป็น noise แต่ละจุด ที่ทำmask ได้ไม่ดีพอ ซึ่งก็ไม่ได้มารวมอยู่แล้ว
              pass
          
    count = count + 1