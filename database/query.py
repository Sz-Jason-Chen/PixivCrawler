import datetime
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='chen0402', db='pixiv')
cursor = conn.cursor()

'''
# effect_row1 = cursor.execute("select * from illust where id>80000000 and tags like '%VTuber%' limit 1000;")
# effect_row1 = cursor.execute("select * from illust where id>80000000 and tags like '%VTuber%';")
effect_row1 = cursor.execute("select * from illust where tags like '%VTuber%' limit 1000")
row1 = cursor.fetchone()
row2 = cursor.fetchmany(5)

print(effect_row1)
print(row1)
print(row2)
'''

date1 = datetime.datetime(2020, 6, 1, 0, 0, 0)
date2 = datetime.datetime(2020, 6, 2, 0, 0, 0)
for i in range(100):
    dailynew = cursor.execute(f"select count(*) from illust WHERE (createDate >= timestamp '{date1}') AND (createDate < timestamp '{date2}');")
    row1 = cursor.fetchone()
    print(date1)
    print(row1[0])

    date1 = date1 + datetime.timedelta(days=1)
    date2 = date2 + datetime.timedelta(days=1)



