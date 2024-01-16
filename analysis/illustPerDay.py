import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, DateFormatter
from matplotlib.ticker import MaxNLocator

import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf

from config import *
from crawler import *


def fetch_data_save_csv():
    """
    DO NOT RUN THIS FUNCTION without original txt files!
    :return:
    """
    # fetch data and saved in pd dataframe --------------------------------------------------
    # fetch the first date
    with open(f"{OUTPUT_PATH}illusts_text_storage\\illusts_text_storage_001.txt", "r", encoding="UTF-8") as f:
        start = IllustText(raw=f.readline())
        start_date = start.get_create_date().date()
        print(start_date)

    # init df and counting value
    daily_df = pd.DataFrame(columns=["date", "new", "total"])
    counting_date = start_date
    counting_new = 0
    counting_total = 0

    # file range
    for file_index in range(1, 101):
        with open(f"{OUTPUT_PATH}illusts_text_storage\\illusts_text_storage_{file_index:0>3}.txt", "r",
                  encoding="UTF-8") as f:
            # check line by line
            for line in f.readlines():
                text = IllustText(raw=line)
                current_date = text.get_create_date().date()

                if current_date == counting_date:
                    counting_new += 1

                elif current_date >= counting_date:
                    counting_total += counting_new
                    daily_df = daily_df._append({"date": counting_date, "new": counting_new, "total": counting_total},
                                                ignore_index=True)

                    counting_new = 1
                    counting_date = current_date

                    print(current_date)
                    # print(text.get_id())
                elif current_date <= counting_date:
                    daily_df.loc[daily_df["date"] == current_date, ["new", "total"]] += 1

    print(daily_df)
    daily_df.to_csv(f"{OUTPUT_PATH}new_and_total_illust_per_day.csv", index=False)


def new_raw_and_rolling_avg():
    daily_df = pd.read_csv(f"{OUTPUT_PATH}new_and_total_illust_per_day.csv")
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    daily_df["rolling_avg"] = daily_df["new"].rolling(window=7, center=True).mean()

    # prepare x labels
    """x_labels = [datetime.datetime(year=2007, month=7, day=1)]
    for year in range(2008, 2023):
        x_labels.append(datetime.datetime(year=year, month=1, day=1))
        x_labels.append(datetime.datetime(year=year, month=7, day=1))
    x_labels.append(datetime.datetime(year=2023, month=1, day=1))"""

    plt.figure(figsize=(40, 30))  # set the figure size (inch)
    plt.plot(daily_df["date"], daily_df["new"], label="raw", linestyle='-')
    plt.plot(daily_df["date"], daily_df["rolling_avg"], label="7-days rolling average", linestyle='-', color="r")
    plt.title("New illust per day", fontsize=100)  # figure title
    plt.xlabel("Date", fontsize=70)  # axis label
    plt.ylabel("Count", fontsize=70)
    plt.xticks(fontsize=40)  # axis ticks font size
    # plt.xticks(x_labels, rotation=90, fontsize=30)  # vertical x-axis label
    plt.yticks(fontsize=40)
    # plt.xlim(left=x_labels[0])
    plt.ylim(bottom=0) # start point of axis
    plt.tick_params(which="both", pad=20)  # label to both axis distance
    plt.grid(linewidth=4)  # show grid and set the grid's width
    plt.legend(fontsize=40, handlelength=4)# present figure legend

    ax = plt.gca()
    ax.xaxis.set_major_locator(YearLocator(base=1))  # 1 year scale
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))  # set x-axis labels' format, only present year
    # ax.xaxis.set_major_locator(MaxNLocator(nbins=40))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=20))  # axis label density
    # set the borderlines' width
    for spine in ax.spines.values():
        spine.set_linewidth(8)

    plt.show()


def new_weekday():
    daily_df = pd.read_csv(f"{OUTPUT_PATH}new_and_total_illust_per_day.csv")
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    daily_df["weekday"] = daily_df["date"].dt.day_name()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    plt.figure(figsize=(40, 30))  # set the figure size (inch)
    for weekday in weekdays:
        weekday_rows = daily_df[daily_df["weekday"] == weekday]
        plt.plot(weekday_rows["date"], weekday_rows["new"], label=weekday, linestyle='-', linewidth=2)
    plt.title("New illust per day classified by weekdays", fontsize=100)  # figure title
    plt.xlabel("Date", fontsize=70)  # axis label
    plt.ylabel("Count", fontsize=70)
    plt.xticks(fontsize=40)  # axis ticks font size
    plt.yticks(fontsize=40)
    plt.ylim(bottom=0)  # start point of axis
    plt.tick_params(which="both", pad=20)  # label to both axis distance
    plt.grid(linewidth=4)  # show grid and set the grid's width
    plt.legend(fontsize=40, handlelength=4) # present figure legend

    ax = plt.gca()
    ax.xaxis.set_major_locator(YearLocator(base=1))  # 1 year scale
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))  # set x-axis labels' format, only present year
    ax.yaxis.set_major_locator(MaxNLocator(nbins=20))  # axis label density
    # set the borderlines' width
    for spine in ax.spines.values():
        spine.set_linewidth(8)

    plt.show()


def total_weekday():
    daily_df = pd.read_csv(f"{OUTPUT_PATH}new_and_total_illust_per_day.csv")
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    daily_df["weekday"] = daily_df["date"].dt.day_name()
    weekday_total = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    for row in range(len(daily_df)):
        weekday_total[daily_df.iloc[row, 3]] += daily_df.iloc[row, 1]

    weekdays = weekday_total.keys()
    totals = weekday_total.values()

    print(weekday_total)

    plt.bar(weekdays, totals)
    plt.title("Weekday total")
    plt.xlabel("weekday")
    plt.ylabel("total")
    plt.show()


def seasonal_decomposition():
    daily_df = pd.read_csv(f"{OUTPUT_PATH}new_and_total_illust_per_day.csv")
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    # daily_df = daily_df[:350]

    result = sm.tsa.seasonal_decompose(daily_df["new"], period=365)  # 这里设置周期为7天，表示一周

    trend = result.trend
    seasonal = result.seasonal
    residual = result.resid

    plt.figure(figsize=(12, 8))

    # 绘制原始数据
    plt.subplot(411)
    plt.plot(daily_df["new"], label='Original Data')
    plt.legend()

    # 绘制趋势
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend()

    # 绘制季节性
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonal')
    plt.legend()

    # 绘制残差
    plt.subplot(414)
    plt.plot(residual, label='Residual')
    plt.legend()

    # 显示图形
    plt.tight_layout()
    plt.show()


def autocorrelation():
    daily_df = pd.read_csv(f"{OUTPUT_PATH}new_and_total_illust_per_day.csv")
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    daily_df = daily_df[2000:3000]
    daily_df.set_index("date", inplace=True)
    print(daily_df)

    # acf = daily_df["new"].autocorr(lag=1)  # lag表示滞后期数
    # print(f'autocorrelation coefficient: {acf}')

    plot_acf(daily_df["new"], lags=100)  # 你可以自定义lags的数量
    plt.show()


if __name__ == "__main__":
    # new_raw_and_rolling_avg()
    # new_weekday()
    # total_weekday()
    # seasonal_decomposition()
    autocorrelation()
    pass

