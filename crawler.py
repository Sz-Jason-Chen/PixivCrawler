import random
import requests
from config import *
from retrying import retry


@retry(wait_fixed=1000)
def illusts_text(pid):
    """
    Crawl the original text, including the artwork name, author and tags.

    The url is: https://www.pixiv.net/ajax/user/{uid}/illusts?ids[]={pid}
    The {uid} is the user ID. It seems like any user ID is available.
    The {pid} is the aimed artwork's ID.

    :param pid: Pixiv artwork ID
    :return: Raw text from requests.get().text
    """
    headers = {
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    url = "https://www.pixiv.net/ajax/user/51314271/illusts?ids[]=" + str(pid)
    html = requests.get(url=url, headers=headers, timeout=5)
    text = html.text
    html.close()
    return text


@retry(wait_fixed=1000)
def illust_pages_text(pid):
    """
    Crawl the texts including the artwork's picture source urls.
    The text contains thumbnail and original urls.
    If the artwork have multiple pictures, the text will contain multiple sets of urls.

    The url is: https://www.pixiv.net/ajax/illust/{pid}/pages
    The {pid} is the aimed artwork's ID.

    :param pid: Pixiv artwork ID
    :return: Raw text from requests.get().text
    """
    headers = {
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    url = "https://www.pixiv.net/ajax/illust/" + str(pid) + "/pages"
    html = requests.get(url=url, headers=headers)
    text = html.text
    html.close()
    return text


@retry(wait_fixed=1000)
def img_original_content(url):
    """
    Crawl the picture as original size.

    The url is: https://i.pximg.net/img-original/img/{yyyy}/{mm}/{dd}/{hh}/{mm}/{ss}/{file name}
    The {yyyy}/{mm}/{dd}/{hh}/{mm}/{ss} is the upload time of the picture, for example, 2023/06/11/00/00/26
    The {file name} is: {ID}_{picture index}.{format}
    For example, it can be 108902679_p0.jpg or 108859422_p1.jpg, or it may be gif but have not confirmed yet.
    Consider the url is very complex, it is often extracted from the page texts by the illust_pages_text funtion.

    :param url: Original image's url
    :return: Original image
    """
    headers = {
        "referer": "https://www.pixiv.net",
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    html = requests.get(url=url, headers=headers)
    pic = html.content
    html.close()
    return pic


@retry(wait_fixed=1000)
def ugoira_meta_text(pid):
    headers = {
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    url = "https://www.pixiv.net/ajax/illust/" + str(pid) + "/ugoira_meta"
    html = requests.get(url=url, headers=headers)
    text = html.text
    html.close()
    return text


def ugoira_zip_content(url):
    headers = {
        "referer": "https://www.pixiv.net",
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    html = requests.get(url=url, headers=headers)
    ugo = html.content
    html.close()
    return ugo


@retry(wait_fixed=1000)
def user_profile_text(uid):
    """
    Crawl the user's information, including the illusts' IDs.

    :param uid: User ID
    :return: Raw text from requests.get().text
    """
    headers = {
        "user-agent": random.choice(USER_AGENT_POOL),
        "cookie": COOKIE}
    url = "https://www.pixiv.net/ajax/user/" + str(uid) + "/profile/all"
    html = requests.get(url=url, headers=headers)
    text = html.text
    html.close()
    return text
