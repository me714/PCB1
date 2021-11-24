import cv2
from matplotlib import pyplot as plt


image0 = cv2.imread('D:\PCB\code\image.bmp')
image1 = cv2.imread('D:\PCB\code\image_c.bmp')
b0, g0 ,r0 = cv2.split(image0)
b1, g1 ,r1 = cv2.split(image1)
res0 = cv2.pyrDown(g0)
res1 = cv2.pyrDown(g1)

x0 = cv2.Sobel(res0, cv2.CV_16S, 1, 0)
x1 = cv2.Sobel(res1, cv2.CV_16S, 1, 0)

y0 = cv2.Sobel(res0, cv2.CV_16S, 0, 1)
y1 = cv2.Sobel(res1, cv2.CV_16S, 0, 1)
Scale_absX0 = cv2.convertScaleAbs(x0)  # convert 转换  scale 缩放
Scale_absX1 = cv2.convertScaleAbs(x1)  # convert 转换  scale 缩放
Scale_absY0 = cv2.convertScaleAbs(y0)
Scale_absY1 = cv2.convertScaleAbs(y1)
result0 = cv2.addWeighted(Scale_absX0, 0.5, Scale_absY0, 0.5, 0)
result1 = cv2.addWeighted(Scale_absX1, 0.5, Scale_absY1, 0.5, 0)
result0, binary = cv2.threshold(result0,220, 225, cv2.THRESH_TRUNC)
result1, binary_inv = cv2.threshold(result1, 220, 225, cv2.THRESH_TRUNC)

image2 = cv2.subtract(binary, binary_inv)
image3 = cv2.subtract(binary_inv, binary)
image_s = cv2.addWeighted(image2, 0.5, image3, 0.5, 0)
cv2.imshow('image',image_s)
cv2.waitKey(0)


