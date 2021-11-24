# -*- coding:utf-8 -*-
import numpy as np
import cv2 as cv
# from matplotlib import pyplot as plt
import time

'''
抽取关键点
kp  是一个list<关键点>。 关键点：特殊结构体，属性当中有坐标，方向、角度等等
des 是关键点的特征向量，为128维的向量
'''


def function_sift(image):
    sift = cv.SIFT_create()
    kp, des = sift.detectAndCompute(image, None)
    # 可以对关键点进行一些自定义的筛选。
    return kp, des


'''
匹配比较合适的关键点
使用K近邻（KNN）算法。
K近邻算法求取在空间中距离最近的K个数据点，并将这些数据点归为一类。
在进行特征点匹配时，一般使用KNN算法找到最近邻的两个数据点，
    如果最接近和次接近的比值大于一个既定的值，那么我们保留这个最接近的值，
    认为它和其匹配的点为good match（由Lowe在SIFT论文中提出）。
'''


def function_good_match(des1, des2, delta=0.5):
    bfm = cv.BFMatcher()
    matches = bfm.knnMatch(des1, des2, k=2)
    good_match = []
    for m1, m2 in matches:
        if m1.distance < delta * m2.distance:
            good_match.append(m1)
    return good_match


'''
根据img1将img2进行校准后重新输出，使得img2与img1能够得到较好的像素匹配
完全根据原始图像的大小来的，所以适合不太大的图像。
@imgOut 根据img1将img2进行配准后的图片
@H      单应矩阵
@status 使用状态。（基本无用）
'''


def function_Alignment(img1, img2):
    kp1, des1 = function_sift(img1)
    kp2, des2 = function_sift(img2)
    goodMatch = function_good_match(des1, des2)
    if len(goodMatch) > 4:
        ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ransacReprojThreshold = 4
        H, status = cv.findHomography(ptsA, ptsB, cv.RANSAC, ransacReprojThreshold)
        imgOut = cv.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]),
                                    flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP)
    return imgOut, H, status


'''
根据img1将img2进行校准后重新输出，使得img2与img1能够得到较好的像素匹配
适合比较大的图像，先将两幅图缩小到tSize大小，然后计算配准矩阵
'''


def function_Alignment2(img10, img20, tSize=(512, 512)):
    img1 = cv.resize(img10, tSize)
    img2 = cv.resize(img20, tSize)
    h, w = img10.shape[0], img10.shape[1]
    delta_h = h / tSize[0]
    delta_w = w / tSize[1]
    kp1, des1 = function_sift(img1)
    kp2, des2 = function_sift(img2)
    goodMatch = function_good_match(des1, des2)
    if len(goodMatch) > 4:
        ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ransacReprojThreshold = 4
        H, status = cv.findHomography(ptsA, ptsB, cv.RANSAC, ransacReprojThreshold)
        H[0, 2] *= delta_w
        H[1, 2] *= delta_h
        imgOut = cv.warpPerspective(img20, H, (img10.shape[1], img10.shape[0]),
                                    flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP)
    return imgOut, H, status