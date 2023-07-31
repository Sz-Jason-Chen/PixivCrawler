import cv2
import numpy as np
import os
import pandas as pd
import time
import crawler
import numpy as np
import matplotlib.pyplot as plt
import random
import requests
import zipfile
from config import *
from fileAccess import *
from matplotlib.patches import Ellipse
from multiprocessing.dummy import Pool
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris



def main():
    url = "https://i.pximg.net/img-zip-ugoira/img/2022/11/18/03/26/34/102879473_ugoira1920x1080.zip"
    headers = {
        "referer": "https://www.pixiv.net",
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    html = requests.get(url=url, headers=headers)
    ugo = html.content
    html.close()

    f = open(os.getcwd() + "\\output\\" + "ugo.zip", "wb")
    f.write(ugo)
    f.close()

    with zipfile.ZipFile(os.getcwd() + "\\output\\" + "ugo.zip", 'r') as zip_ref:
        zip_ref.extractall(os.getcwd() + "\\output\\" + 'unzip_folder')

    zip_folder = os.getcwd() + "\\output\\" + "unzip_folder"



    def images_to_video(zip_folder, output_video_path, fps=30):
        # 获取图片文件夹中所有图片的列表
        image_files = [f for f in os.listdir(zip_folder) if f.endswith('.jpg') or f.endswith('.png')]
        image_files.sort()

        if not image_files:
            print(f"No image files found in {zip_folder}.")
            return

        # 获取第一张图片的尺寸，假设所有图片尺寸相同
        first_image_path = os.path.join(zip_folder, image_files[0])
        first_image = cv2.imread(first_image_path)
        height, width, _ = first_image.shape

        # 创建视频编码器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        # 将图片逐帧写入视频
        for image_file in image_files:
            image_path = os.path.join(zip_folder, image_file)
            image = cv2.imread(image_path)
            video.write(image)

        # 释放视频编码器资源
        video.release()

        print(f"Video saved as {output_video_path}.")

    # 示例用法
    output_video_path = "output.mp4"
    images_to_video(zip_folder, output_video_path, fps=24)


if __name__=="__main__":
    main()


