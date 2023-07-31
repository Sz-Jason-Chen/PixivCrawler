from fileAccess import *
from text import *


def main():
    pid = str(input("PID: "))

    text = IllustText(raw=crawler.illusts_text(pid=pid))
    print(text.get_title())
    info = text.get_info()
    file_name = pid + ".txt"
    FormattedInfoWrite(file_name=file_name, info=info)

    urls = IllustPageText(raw=crawler.illust_pages_text(pid=pid)).get_original()
    p = 0
    for url in urls:
        print(url)
        pic = crawler.img_original_content(url)
        file_name = pid + "_p" + str(p) + ".png"
        PicWrite(file_name=file_name, pic=pic)
        p = p + 1

    if text.get_illust_type() == 2:
        ugo_meta_text = UgoiraMetaText(raw=crawler.ugoira_meta_text(pid=pid))
        ugo_src = ugo_meta_text.get_original_src()
        ugo_fps = ugo_meta_text.get_delay()
        ugo_zip = crawler.ugoira_zip_content(ugo_src)

        ZipWriter(file_name=pid + ".zip", zip=ugo_zip)

        unzip_folder = os.getcwd() + "\\output\\" + "unzip_folder"
        UnzipWriter(file_name=pid + ".zip", unzip_folder=unzip_folder)

        Mp4Writer(frame_folder=unzip_folder, file_name=pid + ".mp4", fps=ugo_fps)


if __name__ == "__main__":
    main()
