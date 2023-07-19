import crawler
import time
import random
import json
from config import *


def get_artwork_information(pid):
    """
    Using pixiv artwork ID, search for corresponding artwork information.
    The information is stored in a list and returned and saved as a txt file.
    If there's no artwork under the ID, it will return an empty list and will not create a file.

    :param pid: Pixiv artwork ID
    :return: A list containing detailed information of the artwork.

    """

    raw_info = crawler.illusts_text(pid=pid)
    parsed_info = json.loads(raw_info)
    if len(parsed_info["body"]) != 0:
        info = parsed_info["body"][pid]
        print(info["title"])
    else:
        info = []
    print(info)
    if len(info) != 0:
        file_name = PATH + pid + ".txt"
        file = open(file_name, "w", encoding="UTF-8")
        for attr in info:
            line = attr + ": " + str(info[attr]) + "\n"
            file.write(line)
        file.close()

    return info


def get_artwork_picture(pid):
    """
    Using pixiv artwork ID, search for corresponding artwork and save it in a png file.

    :param pid: Pixiv artwork ID
    :return:
    """
    raw_info = crawler.illust_pages_text(pid=pid)
    parsed_info = json.loads(raw_info)
    urls = []
    for page in parsed_info["body"]:
        urls.append(page["urls"]["original"])

    p = 0
    for url in urls:
        print(url)
        pic = crawler.img_original_content(url)
        file_name = PATH + pid + "_p" + str(p) + ".png"
        file = open(file_name, "wb")
        file.write(pic)
        file.close()

        p = p + 1


if __name__ == "__main__":
    for pid in range(38, 39):
        pid = str(pid)
        print(pid)
        info = get_artwork_information(pid=pid)
        if len(info) != 0:
            get_artwork_picture(pid=pid)
        time.sleep(random.uniform(0, 1))
