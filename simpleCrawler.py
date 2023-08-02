from connector import Connector
from fileManager import *
from text import *


def main():
    pid = str(input("PID: "))

    text = IllustText(raw=Connector.illusts_text(pid=pid))
    print("Title: " + text.get_title())

    info = text.get_info()
    file_name = pid + ".txt"
    TxtManager(file_name=file_name).dict_write(info=info)
    print("Text saved")

    urls = IllustPageText(raw=Connector.illust_pages_text(pid=pid)).get_original()
    p = 0
    for url in urls:
        pic = Connector.img_original_content(url)
        file_name = pid + "_p" + str(p) + ".png"
        PicWrite(file_name=file_name, pic=pic)
        p = p + 1
    print("Picture saved")

    if text.get_illust_type() == 2:
        ugo_meta_text = UgoiraMetaText(raw=Connector.ugoira_meta_text(pid=pid))
        ugo_src = ugo_meta_text.get_original_src()
        ugo_fps = ugo_meta_text.get_delay()
        ugo_zip = Connector.ugoira_zip_content(ugo_src)

        ZipWriter(file_name=pid + ".zip", zip=ugo_zip)

        unzip_folder = os.getcwd() + "\\output\\" + "unzip_folder"
        UnzipWriter(file_name=pid + ".zip", unzip_folder=unzip_folder)

        Mp4Writer(frame_folder=unzip_folder,
                  file_name=pid + ".mp4",
                  fps=ugo_fps,
                  width=text.get_width(),
                  height=text.get_height())
        print("Video saved")


if __name__ == "__main__":
    main()
