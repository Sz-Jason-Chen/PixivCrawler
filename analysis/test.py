import datetime
import os
from config import *
from crawler import *

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf

from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense

# 创建一个标量（标量可以是任何数字，这里以整数1为例）
scalar = 1

# 创建一个一维张量
tensor_1d = tf.constant([2, 3, 4])



# 打印堆叠后的张量
print(tensor_1d)








