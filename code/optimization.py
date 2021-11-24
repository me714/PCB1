import cv2
from code.position_correction import function_Alignment
from code.cv_show import cv_show
from code.Ostu import otsu

image0 = cv2.imread('D:\PCB\code\image.bmp')
image1 = cv2.imread('D:\PCB\code\image1.bmp')



# correction, _, _ = function_Alignment(image0,image1)
# cv2.imwrite('image_c.bmp',correction)
b, g ,r = cv2.split(image0)
res = cv2.pyrDown(g)
cv_show('image', res)
# canny_edg = cv2.Canny(res,50, 150)
# cv_show('can', canny_edg)
# Sobel边缘检测算子
x = cv2.Sobel(res, cv2.CV_16S, 1, 0)
y = cv2.Sobel(res, cv2.CV_16S, 0, 1)
# cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
# 可选参数alpha是伸缩系数，beta是加到结果上的一个值，结果返回uint类型的图像
Scale_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
Scale_absY = cv2.convertScaleAbs(y)
result = cv2.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
cv_show('res', result)

result = otsu(result)
cv2.imwrite('image_0.bmp',result)
cv_show('res', result)
