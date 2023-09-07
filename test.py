import cv2
import numpy as np
import os
import pandas as pd
import time
import connector
import numpy as np
import matplotlib.pyplot as plt
import random
import requests
import zipfile
from config import *
from connector import Connector
from fileManager import *
from matplotlib.patches import Ellipse
from multiprocessing.dummy import Pool
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from text import *


def url():
    pic = Connector.img_original_content(url="https://i.pximg.net/user-profile/img/2023/05/12/23/27/09/24413190_1f5f1ac750918e023b0269c2b235ff51_50.jpg")

    PicWrite(file_name="11", pic=pic)

def main():
    # 打开输入文件和输出文件
    with open('E:\program\git project\PixivCrawler\output\illusts_text_storage_003.txt', 'r', encoding="UTF-8") as infile, open('E:\program\git project\PixivCrawler\output\illusts_text_storage_0003.txt', 'w', encoding="UTF-8") as outfile:
        # 读取第一行
        previous_line = infile.readline()
        # 将第一行写入输出文件
        outfile.write(previous_line)

        # 逐行读取并处理文件内容
        for current_line in infile:
            # 如果当前行与前一行不同，就将当前行写入输出文件
            if current_line != previous_line:
                outfile.write(current_line)
                previous_line = current_line

    # 关闭文件
    infile.close()
    outfile.close()


if __name__=="__main__":
    main()
    # url()


