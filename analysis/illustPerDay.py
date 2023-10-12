import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
from config import *
from crawler import *


def main():
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
    for file_index in range(1, 21):
        with open(f"{OUTPUT_PATH}illusts_text_storage\\illusts_text_storage_{file_index:0>3}.txt", "r", encoding="UTF-8") as f:
            # check line by line
            for line in f.readlines():
                text = IllustText(raw=line)
                current_date = text.get_create_date().date()

                if current_date == counting_date:
                    counting_new += 1

                elif current_date >= counting_date:
                    counting_total += counting_new
                    daily_df = daily_df._append({"date": counting_date, "new": counting_new, "total": counting_total}, ignore_index=True)

                    counting_new = 1
                    counting_date = current_date

                    print(current_date)
                    # print(text.get_id())
                elif current_date <= counting_date:
                    daily_df.loc[daily_df["date"] == current_date, ["new", "total"]] += 1


    print(daily_df)

    daily_df.to_csv(f"{OUTPUT_PATH}illustPerDay.csv", index=False)

    plt.figure(figsize=(32, 18))
    plt.plot(daily_df["date"], daily_df["new"], linestyle='-')
    plt.title("New illust per day", fontsize=60)
    plt.xlabel("Date", fontsize=40)
    plt.ylabel("Count", fontsize=40)
    plt.xticks(rotation=90, fontsize=30)  # vertical x axis label
    plt.yticks(fontsize=30)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
