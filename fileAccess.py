import os


class FileAccess:
    def __init__(self, file_name):
        self.file_name = file_name
        self.output_path = os.getcwd() + "\\output\\"
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)


class TXTRead(FileAccess):
    pass


class FormattedInfoSave(FileAccess):
    def __init__(self, file_name, info):
        super().__init__(file_name)
        file = open(self.output_path + self.file_name, "w", encoding="UTF-8")
        for attr in info:
            line = attr + ": " + str(info[attr]) + "\n"
            file.write(line)
        file.close()


class PicSave(FileAccess):
    def __init__(self, file_name, pic):
        super().__init__(file_name)
        file = open(self.output_path + self.file_name, "wb")
        file.write(pic)
        file.close()
