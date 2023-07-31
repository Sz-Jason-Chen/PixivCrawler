import csv
import os


class FileAccess:
    def __init__(self, file_name):
        self.file_name = file_name
        self.output_path = os.getcwd() + "\\output\\"
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)


class TXTRead(FileAccess):
    pass


class FormattedInfoWrite(FileAccess):
    def __init__(self, file_name, info):
        super().__init__(file_name)
        f = open(self.output_path + self.file_name, "w", encoding="UTF-8")
        for attr in info:
            line = attr + ": " + str(info[attr]) + "\n"
            f.write(line)
        f.close()


class PicWrite(FileAccess):
    def __init__(self, file_name, pic):
        super().__init__(file_name)
        f = open(self.output_path + self.file_name, "wb")
        f.write(pic)
        f.close()


class CsvWrite(FileAccess):
    def __init__(self, file_name, rows):
        super().__init__(file_name)
        with open(self.output_path + self.file_name, "w", newline='', encoding="utf-16") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
