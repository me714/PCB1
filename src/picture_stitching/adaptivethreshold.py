import cv2

img = cv2.imread('D:\PCB\code\image.bmp')

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

gauss = cv2.GaussianBlur(gray, (3, 3), 1)

maxvalue = 255

def onaptivethreshold(x):
    value = cv2.getTrackbarPos("value", "Threshold")
    if(value < 3):
        value = 3
    if(value % 2 == 0):
        value = value + 1
    args = cv2.adaptiveThreshold(gauss, maxvalue, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, value, 1)
    gaus = cv2.adaptiveThreshold(gauss, maxvalue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, value, 1)
    cv2.imshow("Args", args)
    cv2.imshow("Gaus", gaus)

cv2.namedWindow("Threshold")

cv2.createTrackbar("value", "Threshold", 0, 10, onaptivethreshold)

cv2.imshow("Threshold", img)

cv2.waitKey(0)