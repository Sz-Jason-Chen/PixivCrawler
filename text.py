import crawler
import datetime
import json
from exceptions import *


class Text:
    def __init__(self, raw):
        """
        This class receive a text String and transform it into dict format.
        Detailed data can be directly fetched by "get" functions.

        :param raw: Illust's text, in String format
        """
        # print(raw)

        if type(raw) == str:
            string = raw
            if raw[-1] == "\n":
                string = raw[:-1]
        try:
            text = json.loads(string)
        except:
            text = eval(string)

        if "id" in text:
            self.text = text
            print("id")
        if "error" in text:
            if text["error"]:
                raise PageReturnError(text["message"])
            else:
                body = text["body"]
                if len(body) == 0:
                    raise ArtworkUnavailableError()
                else:
                    pid = list(body.keys())[0]
                    self.text = body[pid]


    def get_text(self):
        return self.text

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


if __name__ == "__main__":
    raw = crawler.illusts_text(pid=0)
    text = Text(raw=raw)
    print(text.get_text())
