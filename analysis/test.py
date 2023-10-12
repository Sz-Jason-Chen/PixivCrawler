import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
from config import *
from crawler import *

with open(f"{OUTPUT_PATH}illusts_text_storage\\illusts_text_storage_020.txt", "r", encoding="UTF-8") as f:
    start = IllustText(raw=f.readline())
    start_date = start.get_create_date().date()
    print(start_date)

previous_date = start_date

with open(f"{OUTPUT_PATH}illusts_text_storage\\illusts_text_storage_020.txt", "r", encoding="UTF-8") as f:
    for line in f.readlines():
        text = IllustText(raw=line)
        current_date = text.get_create_date().date()

        if current_date == previous_date:
            pass
        elif current_date >= previous_date:
            print(current_date, text.get_id(), text.get_create_date())
            previous_date = current_date
        elif current_date <= previous_date:
            pass
