from crawler import *
from collections import Counter
from multiprocessing.dummy import Pool



"""
Fetch a user's all illusts' tags, count each tag's occurrence, save in a csv file.
"""


def get_user_illusts(uid):
    text = UserProfileText(raw=Connector.user_profile_text(uid=uid))
    return text.get_illusts()


def get_user_name(uid):
    pid = get_user_illusts(uid=uid)[0]
    text = IllustText(raw=Connector.illusts_text(pid=pid))
    return text.get_user_name()


def illusts_tags_count(pids):
    counter = Counter()

    def crawl(pid):
        tags = IllustText(raw=Connector.illusts_text(pid=pid)).get_tags()
        counter.update(tags)
        print(pid)

    pool = Pool(50)
    pool.map(crawl, pids)
    return dict(counter)


def csv_output(tags_count):
    col_names = ["tag", "count"]
    row_list = [col_names]
    for item in tags_count.items():
        row_list.append(list(item))
    print(row_list)
    CsvManager("tags_count.csv").row_list_write(rows=row_list)


def main():
    uid = input("uid: ")
    user_illusts = get_user_illusts(uid=uid)
    tags_count = illusts_tags_count(pids=user_illusts)
    csv_output(tags_count)
    print(get_user_name(uid=uid))


if __name__ == "__main__":
    main()
