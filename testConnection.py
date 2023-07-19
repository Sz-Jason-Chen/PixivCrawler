import requests


def web_test():
    try:
        requests.get(url="https://www.pixiv.net/")
    except Exception:
        return False
    else:
        return True


if __name__ == "__main__":
    isAvailable = web_test()
    print(isAvailable)
