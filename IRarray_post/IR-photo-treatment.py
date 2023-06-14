# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2

datalist = os.listdir("IRdata/")


'''
for file_name in datalist:
    data = np.loadtxt("IRdata/"+file_name).reshape(24,32)
    plt.title("Pcolormesh", fontsize=20)
    plt.pcolormesh(data, cmap='viridis_r', shading='gouraud')
    #plt.pcolormesh(data, cmap='plasma', shading='gouraud')
    #plt.show()
    filename_save="IRpic/"+file_name[0:-3]+"png"
    plt.savefig(filename_save)
    #time.sleep(0.05)
'''

 
# 图片文件夹路径
piclist = os.listdir("IRpic/")
# 视频文件保存路径和名称
video_name = "IRpic/test_video.mp4"

# 读取第一张图片，获取图片尺寸
img = cv2.imread("IRpic/"+piclist[0])
height, width, channels = img.shape
 
# 创建视频编写器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 定义视频编码器
video = cv2.VideoWriter(video_name, fourcc, 3, (width, height))  # 定义视频文件，帧率为3
 
# 逐个将图片写入视频文件
for img_path in piclist:
    img = cv2.imread("IRpic/"+img_path)
    video.write(img)
 
# 释放资源
video.release()
