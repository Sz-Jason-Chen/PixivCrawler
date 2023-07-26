import numpy as np
import pandas as pd
import crawler
import numpy as np
import matplotlib.pyplot as plt
from config import *
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris


def main():
    string = crawler.illusts_text(20)
    print(type(string))
    print(eval(string))

if __name__=="__main__":
    main()