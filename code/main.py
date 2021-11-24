import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import glob
from Stitcher import Stitcher
from code.cv_show import cv_show


bmp_path = r'D:\PCB\image\back'
bmp_list = glob.glob(bmp_path+"/*.bmp")
stitch = Stitcher()
image0 = cv2.imread(bmp_list[0])
image1 = cv2.imread(bmp_list[1])
for i in range(7):
    if i >0:
        image1 = cv2.imread(bmp_list[i])
        image0 = stitch.stitch([image1,image0],showMatches=False)

cv2.imwrite('image2.bmp', image0)
# cv_show('image', image0)




