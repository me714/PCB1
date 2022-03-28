# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :PCB
# @File     :template
# @Date     :2022/3/28 16:15
# @Author   :Sun
# @Email    :szqqishi@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import glob
import os.path

import cv2
import numpy as np


def root2list(root):
    bmp_list = glob.glob(root + "\\*.bmp")
    return bmp_list


def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))


def make_contour(template, img_gray, w, h, angle, threshold):
    rects = []
    # 模板旋转匹配
    for i in range(0, 360, angle):
        new_rotate = rotate_bound(template, i)
        # 把图片旋转后黑色的部分填充成白色
        new_rotate[new_rotate == 0] = 255
        # 使用matchTemplate对原始灰度图像和图像模板进行匹配
        res = cv2.matchTemplate(img_gray, new_rotate, cv2.TM_CCOEFF_NORMED)
        # 设定阈值
        loc = np.where(res >= threshold)
        # x,y坐标对调打包
        for pt in zip(*loc[::-1]):
            point = np.array([[pt[0], pt[1]], [pt[0] + w, pt[1]],
                              [pt[0], pt[1] + h], [pt[0] + w, pt[1] + h]])
            rects.append(cv2.boundingRect(point))
    # 模板匹配后符合要求的所有图案数量
    length = len(rects)
    # 设定阈值
    threshold = 30
    i = 0
    # 如果两个图案距离在阈值范围内，则等同，然后用集合去重
    while i < length:
        for j in range(length):
            if j != i:
                if np.abs(rects[j][0] - rects[i][0]) <= threshold:
                    if np.abs(rects[j][1] - rects[i][1]) <= threshold:
                        rects[j] = rects[i]
        i = i + 1
    return set(rects)


def draw_contour(img_rgb, contours, color, img_name):
    count = 0
    for contour in contours:
        cv2.rectangle(img_rgb, (contour[0], contour[1]), (contour[0] + contour[2], contour[1] + contour[3]),
                             color, 1)
        cx = contour[0] + (contour[2] // 2)
        cy = contour[1] + (contour[3] // 2)
        count = count + 1
        cv2.putText(img_rgb, str(img_name.split('@')[0]), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, 1)
        with open("data.txt", "a+") as f:
            f.write("contour" + '\t' + str(count) + '\t' + 'cx: ' + str(cx) + '  \t' + 'cy: ' + str(cy) + '  \t' + 'template: ' + img_name.split('@')[0] + '\n')
            # 显示图像
    img_name = os.path.join(r'D:\Projects\PCB\outputs', img_name)
    print(img_name)
    cv2.imwrite(img_name, img_rgb)


def template(img_root, template_root, threshold=0.3, color=(255, 0, 0)):

    """
    :param color:
    :param threshold:
    :param img_root: 待匹配的图片地址
    :param template_root: 模板图片地址
    :return:
    """

    img_list = root2list(img_root)

    template_list = root2list(template_root)
    for i, img_path in enumerate(img_list):
        img_name = img_path.split('\\')[-1]
        img = cv2.imread(img_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for j, template_path in enumerate(template_list):
            if j == 2:
                img_1 = img.copy()
                template_name = template_path.split('\\')[-1].replace('.bmp', '@')
                img_name = template_name + img_name
                template = cv2.imread(template_path, 0)
                w, h = template.shape[::-1]
                contours = make_contour(template, img_gray, w, h, 90, threshold)
                draw_contour(img_1, contours, color, img_name)
                img_name = img_path.split('\\')[-1]


if __name__ == '__main__':
    img_root = r'D:\Projects\PCB\image\imgs'
    template_root = r'D:\Projects\PCB\image\templates'
    template(img_root, template_root)