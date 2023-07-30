import crawler
import datetime
import json
from exceptions import *


class Text:
    def __init__(self, raw):
        if type(raw) == str:
            string = raw
            if raw[-1] == "\n":
                string = raw[:-1]
        try:
            text = json.loads(string)
        except:
            text = eval(string)
        if "error" in text:
            if text["error"]:
                raise PageReturnError(text["message"])
            else:
                self.body = text["body"]


class IllustText(Text):
    def __init__(self, raw):
        """
        This class receive a text String and transform it into dict format.
        Detailed data can be directly fetched by "get" functions.

        :param raw: Illust's text, in String format
        """
        if '"error"' in raw:
            super().__init__(raw=raw)
            if len(self.body) == 0:
                raise ArtworkUnavailableError()
            else:
                pid = list(self.body.keys())[0]
                self.text = self.body[pid]
        else:
            try:
                self.text = json.loads(raw)
            except:
                self.text = eval(raw)

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

    def get_user_name(self):
        return self.text["userName"]


class IllustPageText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)
        self.thumb_mini = []
        self.small = []
        self.regular = []
        self.original = []
        self.width = []
        self.height = []
        for p in self.body:
            self.thumb_mini.append(p["urls"]["thumb_mini"])
            self.small.append(p["urls"]["small"])
            self.regular.append(p["urls"]["regular"])
            self.original.append(p["urls"]["original"])
            self.width.append(p["width"])
            self.height.append(p["height"])

    def get_thumb_mini(self):
        return self.thumb_mini

    def get_small(self):
        return self.small

    def get_regular(self):
        return self.regular

    def get_original(self):
        return self.original

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class UserProfileText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)

    def get_illusts(self):
        return list(self.body["illusts"].keys())


if __name__ == "__main__":
    raw = crawler.illusts_text(pid=20)
    text = IllustText(raw=raw)
    print(text.get_text())

    raw = crawler.user_profile_text(uid=74555562)
    text = UserProfileText(raw=raw)
    print(text.get_illusts())
