import mysql.connector
from config import *

def read_data():
    tuple_list = []

    with open(OUTPUT_PATH + 'illusts_text_storage_001.txt', 'r', encoding="UTF-8") as f:
        pass


    return tuple_list


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


def main():
    pass


if __name__ == "__main__":
    main()
