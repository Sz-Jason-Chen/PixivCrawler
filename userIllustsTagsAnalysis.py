import crawler
import csv
import json
from config import OUTPUT_PATH
from text import *

"""
Fetch a user's all illusts' tags, count each tag's occurrence, save in a csv file.
"""


def get_user_illusts(uid):
    text = UserProfileText(raw=crawler.user_profile_text(uid=uid))
    return text.get_illusts()


def get_user_name(uid):
    pid = get_user_illusts(uid=uid)[0]
    raw_text = crawler.illusts_text(pid=pid)
    parsed_text = json.loads(raw_text)
    return parsed_text["body"][pid]["userName"]


def illusts_tags_count(pids, limit=0):
    tags_count = {}
    illusts_count = 0
    for pid in pids:
        raw_text = crawler.illusts_text(pid=pid)
        parsed_text = json.loads(raw_text)
        tags = parsed_text["body"][pid]["tags"]
        for tag in tags:
            if tag in tags_count:
                tags_count[tag] += 1
            else:
                tags_count[tag] = 1

        illusts_count += 1
        print(illusts_count)
        if illusts_count == limit:
            break
    return tags_count


def csv_output(tags_count):
    col_names = ["tag", "count"]
    row_list = [col_names]
    for item in tags_count.items():
        row_list.append(list(item))
    print(row_list)

    with open(OUTPUT_PATH + "tags_count.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


def main(uid):
    user_illusts = get_user_illusts(uid=uid)
    tags_count = illusts_tags_count(pids=user_illusts, limit=0)
    csv_output(tags_count)


if __name__ == "__main__":
    uid = input("uid: ")
    main(uid=uid)
    print(get_user_name(uid=uid))
