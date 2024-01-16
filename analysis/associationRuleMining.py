import csv
import os

from config import OUTPUT_PATH

csv_file_path = os.path.join(OUTPUT_PATH, 'illust_info', 'illust_info_001.csv')
data_dict = {}

with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        key = int(row[0])
        value = eval(row[6])
        data_dict[key] = value

print(data_dict)

# FP-Growth algorithms --------------------------------------------------




