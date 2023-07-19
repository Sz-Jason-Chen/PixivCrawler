import numpy as np
import pandas as pd
import crawler
import numpy
import matplotlib.pyplot as plt
from config import *

from matplotlib.patches import Ellipse


def plot_point_cov(points, nstd=3, ax=None, **kwargs):
    # 求所有点的均值作为置信圆的圆心
    pos = points.mean(axis=0)
    # 求协方差
    cov = np.cov(points, rowvar=False)

    return plot_cov_ellipse(cov, pos, nstd, ax, **kwargs)


def plot_cov_ellipse(cov, pos, nstd=3, ax=None, **kwargs):
    def eigsorted(cov):
        cov = np.array(cov)
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        return vals[order], vecs[:, order]

    if ax is None:
        ax = plt.gca()
    vals, vecs = eigsorted(cov)

    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * nstd * np.sqrt(vals)
    ellip = Ellipse(xy=pos, width=width, height=height, angle=theta, **kwargs)
    ax.add_artist(ellip)
    return ellip


'''画置信圆'''


def show_ellipse(X_pca, y, pca, flag=1):
    # 定义颜色

    colors = ['tab:blue', 'tab:orange', 'seagreen']
    regions = ['Ethiopia', 'Somalia', 'Kenya']

    # 定义分辨率
    plt.figure(dpi=300, figsize=(8, 6))
    # 三分类则为3
    for i in range(0, 3):
        pts = X_pca[y == int(i), :]
        new_x, new_y = X_pca[y == i, 0], X_pca[y == i, 1]

        plt.plot(new_x, new_y, '.', color=colors[i], label=regions[i], markersize=14)

        plot_point_cov(pts, nstd=3, alpha=0.25, color=colors[i])

    # 添加坐标轴
    plt.xlim(-3.5, 4.5)
    plt.ylim(-1.5, 1.7)
    plt.xticks(size=16, family='Times New Roman')
    plt.yticks(size=16, family='Times New Roman')
    font = {'family': 'Times New Roman', 'size': 16}
    plt.xlabel('PC1 ({} %)'.format(round(pca.explained_variance_ratio_[0] * 100, 2)), font)
    plt.ylabel('PC2 ({} %)'.format(round(pca.explained_variance_ratio_[1] * 100, 2)), font)

    plt.legend(prop={"family": "Times New Roman", "size": 9}, loc='upper right')
    plt.show()


import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

def main():
    labels = ['setosa', 'versicolor', 'virginica']
    iris = load_iris()
    X = iris.data
    y = iris.target_names[iris.target]

    print("y length--------", len(y))
    y_category = pd.Categorical(y, ordered=True, categories=['setosa', 'versicolor', 'virginica'])

    y = y_category.codes
    print(y)
    print(y.shape)
    print(type(y[0]))
    n_components = 2
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    show_ellipse(X_pca, y, pca)


if __name__=="__main__":
    main()