import datetime
import os
import pandas as pd
import time
from collections import Counter
from config import *


class Line:
    def __init__(self, line):
        self.line = line

    def get_create_date(self):
        return datetime.datetime.fromisoformat(eval(self.line[:-1])["createDate"])

    def get_id(self):
        return eval(self.line[:-1])["id"]

    def get_tags(self):
        return eval(self.line[:-1])["tags"]

    def get_title(self):
        return eval(self.line[:-1])["title"]

    def get_user_id(self):
        return eval(self.line[:-1])["userId"]


def total():
    counter = Counter()
    count = 0
    for i in range(1, 2):
        # check file exist
        file_name = ("illusts_text_storage_%s.txt" % f'{i:0>3}')
        if not os.path.exists(PATH + file_name):
            continue

        # count line by line
        with open(PATH + file_name, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                count += 1
                line_object = Line(line=line)
                print(count, end=" / ")
                print(line_object.get_id())
                tags = line_object.get_tags()
                counter.update(tags)

    # save counting result
    with open(PATH + "tags_count.txt", "w", encoding="UTF-8") as f:
        """top_10 = counter.most_common(10)
        for item in top_10:
            print(item[0], ":", item[1])"""

        f.write(str(counter))
        print(counter)


def daily(minimum=1, maximum=10):
    counter = Counter()
    count = 0
    last_date = datetime.datetime(2007, 9, 9)
    df = pd.DataFrame()

    for i in range(minimum, maximum):
        # check file exist
        file_name = ("illusts_text_storage_%s.txt" % f'{i:0>3}')
        if not os.path.exists(PATH + file_name):
            continue

        # count line by line
        with open(PATH + file_name, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                count += 1
                line_object = Line(line=line)
                current_date = line_object.get_create_date()

                if current_date.day != last_date.day:
                    print(last_date)
                    print(counter.most_common(20))
                    col_names = [last_date.date()]
                    row_names = []
                    data = []
                    for tag, count in counter.most_common(20):
                        row_names.append(tag)
                        data.append(count)
                    df = df.add(pd.DataFrame(data, index=row_names, columns=col_names), fill_value=0)
                    print(df)

                    last_date = current_date

                tags = line_object.get_tags()
                counter.update(tags)

    df.fillna(0)
    df.to_csv(PATH + "tags_count_top_10.csv")


def main():
    # total()
    start = time.time()
    daily(minimum=100, maximum=110)
    end = time.time()
    time_consume = end - start
    print(time_consume)


if __name__ == "__main__":
    main()
