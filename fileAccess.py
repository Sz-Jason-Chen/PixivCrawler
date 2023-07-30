class FileAccess:
    def __init__(self, file_name):
        self.file_name = file_name


class TXTRead(FileAccess):
    pass


class TXTSave(FileAccess):
    def __init__(self, file_name):
        super().__init__(file_name=file_name)



