import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import glob
from Stitcher import Stitcher
from code.cv_show import cv_show


bmp_path = 'D:\PCB\image'
bmp_list = glob.glob(bmp_path+"/*.bmp")

for i,j in enumerate(bmp_list):
    if i < 6:
        locals()['image' + str(i)] = cv2.imread(bmp_list[i])





