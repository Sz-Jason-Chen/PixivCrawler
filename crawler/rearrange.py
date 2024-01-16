from config import *
from connector import Connector
from fileManager import *
from text import *

def decisave():
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


def removerepli():
    for i in range(81, 101):
        print(i)
        # 打开输入文件和输出文件
        with open(f'E:\program\git project\PixivCrawler\output\illusts_text_storage_{i:0>3}.txt', 'r', encoding="UTF-8") as infile, open(f'E:\program\git project\PixivCrawler\output\illusts_text_storage\illusts_text_storage_{i:0>3}.txt', 'w', encoding="UTF-8") as outfile:
            # 读取第一行
            previous_line = infile.readline()
            # 将第一行写入输出文件
            outfile.write(previous_line)

            # 逐行读取并处理文件内容
            for current_line in infile:
                # 如果当前行与前一行不同，就将当前行写入输出文件
                if current_line != previous_line:
                    outfile.write(current_line)
                    previous_line = current_line

        # 关闭文件
        infile.close()
        outfile.close()


def main():
    for i in range(1, 101):
        data_list = []
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
        CsvManager(file_name=f"illust_info_{i:0>3}.csv",
                   output_path=f"{os.getcwd()}\\output\\illust_info\\").dict_list_write(dicts=data_list)


if __name__=="__main__":
    removerepli()