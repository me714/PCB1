import cv2
from code.picture_stitching.position_correction import function_Alignment

image0 = cv2.imread(r'D:\Projects\calming_lipstick\image\1\b.bmp')
image1 = cv2.imread(r'D:\Projects\calming_lipstick\image\1\n_a.bmp')

# scale = 0.2
# print(image0.shape)
# dsize = (int(image0.shape[0]*scale), int(image0.shape[1]*scale))
# print(dsize)
# image0 = cv2.resize(image0, dsize, interpolation=cv2.INTER_AREA)
# image1 = cv2.resize(image1, dsize, interpolation=cv2.INTER_AREA)
# cv2.imshow('image0',image0)
# cv2.imshow('image1',image1)
# cv2.waitKey(0)
correction, _, _ = function_Alignment(image0, image1)
cv2.imwrite('image_c.bmp', correction)
cv2.imshow('result', correction)
cv2.waitKey(0)
# b, g, r = cv2.split(image0)
# res = cv2.pyrDown(g)
# cv_show('image', res)
# # canny_edg = cv2.Canny(res,50, 150)
# # cv_show('can', canny_edg)
# # Sobel边缘检测算子
# x = cv2.Sobel(res, cv2.CV_16S, 1, 0)
# y = cv2.Sobel(res, cv2.CV_16S, 0, 1)
# # cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
# # 可选参数alpha是伸缩系数，beta是加到结果上的一个值，结果返回uint类型的图像
# Scale_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
# Scale_absY = cv2.convertScaleAbs(y)
# result = cv2.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
# cv_show('res', result)
#
# result = otsu(result)
# cv2.imwrite('image_0.bmp', result)
# cv_show('res', result)
