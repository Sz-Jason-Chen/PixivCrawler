import requests


def web_test():
    """

    :return: Boolean value that represents whether the Pixiv website can be connected
    """
    try:
        requests.get(url="https://www.pixiv.net/")
    except Exception as e:
        print(e)
        return False
    else:
        return True


if __name__ == "__main__":
    isAvailable = web_test()
    print(isAvailable)
