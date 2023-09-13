use pixiv;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/illust_info_001.csv'
INTO TABLE illust
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

TRUNCATE TABLE illust;
delete from illust where id > 91000000;

select * from illust order by id desc limit 100;
select * from illust where id=600000;
select * from illust where rst!=0;