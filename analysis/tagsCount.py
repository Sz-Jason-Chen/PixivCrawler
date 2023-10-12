import datetime
import pandas as pd
import time
import os
from collections import Counter
from config import *
from crawler import IllustText, CsvManager


def total():
    """
    Count all tags in given range of files.
    :return:
    """
    counter = Counter()
    count = 0
    for i in range(1, 101):
        # check file exist
        file_name = f"illusts_text_storage_{i:0>3}.txt"
        if not os.path.exists(OUTPUT_PATH + "illusts_text_storage\\" + file_name):
            continue

        # count line by line
        with open(OUTPUT_PATH + "illusts_text_storage\\" + file_name, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                count += 1
                line_object = IllustText(raw=line)
                print(count, end=" / ")
                print(line_object.get_id())
                tags = line_object.get_tags()
                counter.update(tags)

    sorted_counter = [[item, count] for item, count in counter.items()]
    sorted_counter.sort(key=lambda item: item[1], reverse=True)
    CsvManager(file_name="tags_count.csv").row_list_write(rows=sorted_counter)

    # save counting result
    """with open(OUTPUT_PATH + "tags_count.txt", "w", encoding="UTF-8") as f:
        top_10 = counter.most_common(10)
        for item in top_10:
            print(item[0], ":", item[1])
        f.write(str(counter))"""


def daily(minimum=1, maximum=10):
    """
    Count daily tags sum in given range.

    :param minimum: min file No.
    :param maximum: max file No.
    :return:
    """
    counter = Counter()
    count = 0
    last_date = datetime.datetime(2007, 9, 9)
    df = pd.DataFrame()

    for i in range(minimum, maximum):
        # check file exist
        file_name = ("illusts_text_storage_%s.txt" % f'{i:0>3}')
        if not os.path.exists(OUTPUT_PATH + "illusts_text_storage\\" + file_name):
            continue

        # count line by line
        with open(OUTPUT_PATH + "illusts_text_storage\\" + file_name, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                count += 1
                text = IllustText(raw=line)
                current_date = text.get_create_date()

                # If previous day counting finished
                if current_date.day != last_date.day:
                    print(last_date)
                    print(counter.most_common(20))

                    # formatting
                    col_names = [last_date.date()]
                    row_names = []
                    data = []
                    for tag, count in counter.most_common(20):
                        row_names.append(tag)
                        data.append(count)

                    # append to global counter dataframe
                    df = df.add(pd.DataFrame(data, index=row_names, columns=col_names), fill_value=0)
                    print(df)

                    # update current date
                    last_date = current_date

                tags = text.get_tags()
                counter.update(tags)

    df.fillna(0)
    df.to_csv(OUTPUT_PATH + "tags_count_top_10.csv")


def main():

    start = time.time()
    daily(minimum=1, maximum=100)
    # total()
    end = time.time()
    time_consume = end - start
    print(time_consume)


if __name__ == "__main__":
    main()
