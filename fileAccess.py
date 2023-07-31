import csv
import cv2
import os
import zipfile


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

class ZipWriter(FileAccess):
    def __init__(self, file_name, zip):
        super().__init__(file_name)
        f = open(self.output_path + self.file_name, "wb")
        f.write(zip)
        f.close()


class UnzipWriter(FileAccess):
    def __init__(self, file_name, unzip_folder):
        super().__init__(file_name)
        with zipfile.ZipFile(self.output_path + self.file_name, 'r') as zip_ref:
            zip_ref.extractall(unzip_folder)

class Mp4Writer(FileAccess):
    def __init__(self, frame_folder, file_name, fps=30):
        super().__init__(file_name)
        # 获取图片文件夹中所有图片的列表
        image_files = [f for f in os.listdir(frame_folder) if f.endswith('.jpg') or f.endswith('.png')]
        image_files.sort()

        if not image_files:
            print(f"No image files found in {frame_folder}.")
            return

        # 获取第一张图片的尺寸，假设所有图片尺寸相同
        first_image_path = os.path.join(frame_folder, image_files[0])
        first_image = cv2.imread(first_image_path)
        height, width, _ = first_image.shape

        # 创建视频编码器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(self.output_path + self.file_name, fourcc, fps, (width, height))

        # 将图片逐帧写入视频
        for image_file in image_files:
            image_path = os.path.join(frame_folder, image_file)
            image = cv2.imread(image_path)
            video.write(image)

        # 释放视频编码器资源
        video.release()

        print(f"Video saved.")
