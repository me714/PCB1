import cv2
import glob
from Stitcher import Stitcher

bmp_path = r'F:\Web Downloads\PCB\bad'
bmp_list = glob.glob(bmp_path + "\\*.bmp")
print(bmp_list)
stitch = Stitcher()
image0 = cv2.imread(bmp_list[0])
for i in range(4):
    if i > 0:
        image1 = cv2.imread(bmp_list[i])
        image0 = stitch.stitch([image0, image1], showMatches=False)

cv2.imwrite('image2.bmp', image0)
# cv_show('image', image0)
