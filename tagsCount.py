import datetime
import os
import pandas as pd
import time
from collections import Counter
from config import *


class Text:
    def __init__(self, string):
        """
        This class receive a text String and transform it into dict format.
        Detailed data can be directly fetched by "get" functions.

        :param string: Illust's text, in String format
        """
        if string[-1] == "\n":
            self.text = eval(string[:-1])
        else:
            self.text = eval(string)

    def get_create_date(self):
        return datetime.datetime.fromisoformat(self.text["createDate"])

    def get_id(self):
        return self.text["id"]

    def get_tags(self):
        return self.text["tags"]

    def get_title(self):
        return self.text["title"]

    def get_user_id(self):
        return self.text["userId"]


def total():
    """
    Count all tags in given range of files.
    :return:
    """
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
                line_object = Text(string=line)
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
        if not os.path.exists(PATH + file_name):
            continue

        # count line by line
        with open(PATH + file_name, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                count += 1
                text = Text(string=line)
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
