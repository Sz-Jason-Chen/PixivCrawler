import time

import numpy as np
import pandas as pd
import crawler
import numpy as np
import matplotlib.pyplot as plt
import random
import requests
from config import *
from matplotlib.patches import Ellipse
from multiprocessing.dummy import Pool
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

def userAgent():
    for ua in USER_AGENT_POOL:
        print(ua)
        available = False
        for i in range(10):
            try:
                headers = {
                    "user-agent": ua,
                    "cookie": COOKIE}
                url = "https://www.pixiv.net/ajax/user/51314271/illusts?ids[]=" + "20"
                html = requests.get(url=url, headers=headers)
                text = html.text
                html.close()
                # print(ua)
            except Exception as e:
                print(e)
            else:
                available = True
                break
        print(str(available) )

def repeat(pid):
    t = 0
    f = 0
    while True:
        try:
            headers = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                "cookie": COOKIE}
            url = "https://www.pixiv.net/ajax/user/51314271/illusts?ids[]=" + pid
            html = requests.get(url=url, headers=headers, timeout=10)
            text = html.text
            html.close()
        except:
            f += 1
        else:
            t += 1
        finally:
            print(t, f)
            if t == 100:
                break


def main():
    s = time.time()
    pool = Pool(200)
    empty = []
    for i in range(200):
        empty.append("20")
    pool.map(repeat, empty)
    e = time.time()
    print(e-s)


if __name__=="__main__":
    main()
