from fileAccess import *
from text import *

"""
No multithreading, might be very slow.
"""


def get_artwork_information(pid):
    """
    Using pixiv artwork ID, search for corresponding artwork information.
    The information is stored in a list and returned and saved as a txt file.

    :param pid: Pixiv artwork ID
    :return: Detailed information of the artwork, if ArtworkUnavailableError return None

    """
    pid = str(pid)
    text = IllustText(raw=crawler.illusts_text(pid=pid))
    print(text.get_title())
    info = text.get_text()
    file_name = pid + ".txt"
    FormattedInfoSave(file_name=file_name, info=info)
    return info


def get_artwork_picture(pid):
    """
    Using pixiv artwork ID, search for corresponding artwork and save it in a png file.

    :param pid: Pixiv artwork ID
    :return:
    """
    urls = IllustPageText(raw=crawler.illust_pages_text(pid=pid)).get_original()
    p = 0
    for url in urls:
        print(url)
        pic = crawler.img_original_content(url)
        file_name = pid + "_p" + str(p) + ".png"
        PicSave(file_name=file_name, pic=pic)
        p = p + 1


def main():
    """lower = int(input("Input pid lower bound:"))
        upper = int(input("Input pid upper bound:"))
        for pid in range(lower, upper + 1):
            pid = str(pid)
            print(pid)
            info = get_artwork_information(pid=pid)
            if len(info) != 0:
                get_artwork_picture(pid=pid)
            time.sleep(random.uniform(0, 1))"""

    pid = input("PID: ")
    if get_artwork_information(pid=pid):
        get_artwork_picture(pid=pid)


if __name__ == "__main__":
    main()

