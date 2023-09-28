import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='chen0402', db='pixiv')
cursor = conn.cursor()

# effect_row1 = cursor.execute("select * from illust where id>80000000 and tags like '%VTuber%' limit 1000;")
# effect_row1 = cursor.execute("select * from illust where id>80000000 and tags like '%VTuber%';")
effect_row1 = cursor.execute("select * from illust where tags like '%VTuber%';")
row1 = cursor.fetchone()
row2 = cursor.fetchmany(5)

print(effect_row1)
print(row1)
print(row2)
