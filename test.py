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
    url = "https://i.pximg.net/img-zip-ugoira/img/2022/11/18/03/26/34/102879473_ugoira600x600.zip"
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


if __name__=="__main__":
    main()


