from config import *
from connector import Connector
from fileManager import *
from text import *

def main():
    # 导入 csv 库
    import csv

    data_list = []
    for i in range(31, 41):
        file_name = ("illusts_text_storage_%s.txt" % f'{i:0>3}')

        with open(OUTPUT_PATH + file_name, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                line_text = IllustText(raw=line)
                info = line_text.get_info()
                ignored_keys = ["url", "description", "isBookmarkable", "bookmarkData", "alt",
                                "titleCaptionTranslation", "isUnlisted", "isMasked", "profileImageUrl"]
                for key in ignored_keys:
                    del info[key]
                data_list.append(info)
                print(line_text.get_id())

    CsvManager(file_name="illusts_text_04.csv").dict_list_write(dicts=data_list)


if __name__=="__main__":
    main()