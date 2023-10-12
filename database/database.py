import json
import mysql.connector
from config import *
from crawler import IllustText

def read_data(file_name):
    tuple_list = []

    with open(file_name, 'r', encoding="UTF-8") as f:
        for line in f.readlines():

            line_text = IllustText(raw=line)
            info = line_text.get_info()
            print(line_text.get_id())

            ignored_keys = ["url", "description", "isBookmarkable", "bookmarkData", "alt",
                            "titleCaptionTranslation", "isUnlisted", "isMasked", "profileImageUrl"]
            for key in ignored_keys:
                del info[key]

            info['tags'] = ', '.join(info['tags'])

            tuple_list.append(tuple(info.values()))
            if len(tuple_list) == 100000:
                insert_ordered_list(tuple_list)
                tuple_list = []

    if len(tuple_list) != 0:
        insert_ordered_list(tuple_list)


def insert_ordered_list(data):
    # 创建MySQL数据库连接
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='chen0402',
        database='pixiv'
    )

    # 创建游标对象
    cursor = connection.cursor()

    # 要插入的数据列表
    """data_to_insert = [
        ('306988', '女子高生', '0', '0', '0', '2',
         "['女の子', 'オリジナルキャラ', '和', 'ロングヘア', '制服', 'ミニスカート', 'クリーチャー', '彼岸花']",
         '28316', '/', '555', '780', '1', '2008-01-05T19:50:15+09:00', '2008-01-05T19:50:15+09:00', '0')
        # 添加更多数据行
    ]"""
    data_to_insert = data


    # SQL插入语句模板
    insert_query = "INSERT INTO illust VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # 批量插入数据
    cursor.executemany(insert_query, data_to_insert)

    # 提交事务
    connection.commit()

    # 关闭游标和连接
    cursor.close()
    connection.close()


def test():
    line = {'id': '91291541', 'title': '"error"', 'illustType': 0, 'xRestrict': 1, 'restrict': 0, 'sl': 6, 'url': 'https://i.pximg.net/c/250x250_80_a2/img-master/img/2021/07/17/01/19/06/91291541_p0_square1200.jpg', 'description': '', 'tags': ['R-18', '中出し', 'オリジナル', '女子', '事後'], 'userId': '51029790', 'userName': 'KimKkaMan', 'width': 1452, 'height': 2048, 'pageCount': 1, 'isBookmarkable': True, 'bookmarkData': None, 'alt': '#中出し "error" - KimKkaMan的插画', 'titleCaptionTranslation': {'workTitle': None, 'workCaption': None}, 'createDate': '2021-07-17T01:19:06+09:00', 'updateDate': '2021-07-17T01:19:06+09:00', 'isUnlisted': False, 'isMasked': False, 'aiType': 0, 'profileImageUrl': 'https://i.pximg.net/user-profile/img/2022/10/25/05/08/23/23510632_2891d378a9784161516ea42a2af676aa_50.jpg'}
    line = str(line)
    line_text = IllustText(raw=line)

    print(line)
    eval(line)

def main():
    for i in range(92, 101):
        file_name = OUTPUT_PATH + 'illusts_text_storage\\' + f'illusts_text_storage_{i:0>3}.txt'
        read_data(file_name=file_name)


if __name__ == "__main__":
    main()
    # test()
