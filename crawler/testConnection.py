import os
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

    from pathlib import Path
    FILE = Path(__file__).resolve()
    project_root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(project_root_dir)
