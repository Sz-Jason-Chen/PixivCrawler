import csv
import cv2
import os
import zipfile
from exceptions import ImageFilesNotFoundError


class FileManager:
    def __init__(self, file_name, output_path=f"{os.getcwd()}\\output\\"):
        self.file_name = file_name
        self.output_path = output_path
        self.file_path = self.output_path + self.file_name
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)


class TxtManager(FileManager):
    def __init__(self, file_name):
        super().__init__(file_name)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w'):
                pass

    def dict_write(self, info, replace=True):
        lines = []
        for key, value in info.items():
            line = f"{key}: {value}\n"
            lines.append(line)
        if replace:
            with open(self.file_path, "w", encoding="UTF-8") as file:
                file.writelines(lines)
        else:
            with open(self.file_path, "a", encoding="UTF-8") as file:
                file.writelines(lines)




class TXTAppend(FileManager):
    def __init__(self, file_name, line_list):
        super().__init__(file_name)
        with open(self.file_path, "a+", encoding="UTF-8") as file:
            for text in line_list:
                file.write(str(text) + "\n")


class FormattedInfoWrite(FileManager):
    def __init__(self, file_name, info):
        super().__init__(file_name)
        f = open(self.file_path, "w", encoding="UTF-8")
        for attr in info:
            line = attr + ": " + str(info[attr]) + "\n"
            f.write(line)
        f.close()


class PicWrite(FileManager):
    def __init__(self, file_name, pic):
        super().__init__(file_name)
        f = open(self.file_path, "wb")
        f.write(pic)
        f.close()


class CsvManager(FileManager):
    def __init__(self, file_name):
        super().__init__(file_name)

    def row_list_write(self, rows):
        with open(self.output_path + self.file_name, "w", encoding="utf-8-sig", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def dict_list_write(self, dicts):
        header_list = dicts[0].keys()
        with open(self.output_path + self.file_name, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, header_list)
            writer.writeheader()
            writer.writerows(dicts)


class ZipWriter(FileManager):
    def __init__(self, file_name, zip):
        super().__init__(file_name)
        f = open(self.output_path + self.file_name, "wb")
        f.write(zip)
        f.close()


class UnzipWriter(FileManager):
    def __init__(self, file_name, unzip_folder):
        super().__init__(file_name)
        with zipfile.ZipFile(self.output_path + self.file_name, 'r') as zip_ref:
            zip_ref.extractall(unzip_folder)


class Mp4Writer(FileManager):
    def __init__(self, frame_folder, file_name, fps, width, height):
        super().__init__(file_name)

        # get pictures list
        image_files = [f for f in os.listdir(frame_folder) if f.endswith('.jpg') or f.endswith('.png')]
        image_files.sort()
        if not image_files:
            raise ImageFilesNotFoundError(frame_folder)

        # create video encoder
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(self.output_path + self.file_name, fourcc, fps, (width, height))

        # write frame by frame
        for image_file in image_files:
            image_path = os.path.join(frame_folder, image_file)
            image = cv2.imread(image_path)
            video.write(image)

        # release encoder
        video.release()
