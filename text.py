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
                self.info = self.body[pid]
        else:
            try:
                self.info = json.loads(raw)
            except:
                self.info = eval(raw)

    def get_info(self):
        return self.info

    def get_create_date(self):
        return datetime.datetime.fromisoformat(self.info["createDate"])

    def get_height(self):
        return self.info["height"]

    def get_id(self):
        return self.info["id"]

    def get_illust_type(self):
        return self.info["illustType"]

    def get_tags(self):
        return self.info["tags"]

    def get_title(self):
        return self.info["title"]

    def get_user_id(self):
        return self.info["userId"]

    def get_user_name(self):
        return self.info["userName"]

    def get_width(self):
        return self.info["width"]


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


class UgoiraMetaText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)

    def get_original_src(self):
        return self.body["originalSrc"]

    def get_delay(self):
        return self.body["frames"][0]["delay"]


class UserProfileText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)

    def get_illusts(self):
        return list(self.body["illusts"].keys())
