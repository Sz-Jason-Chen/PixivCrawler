import connector
import json
import os
import threading
import time
from config import *
from connector import Connector
from multiprocessing.dummy import Pool
from text import IllustText
from fileManager import TXTAppend



class InfoStore:
    def __init__(self, file_name):
        """
        An auto crawling and saving procedure for text.

        :param file_name: File to store text line by line.
        """
        self.text_dict_list = []
        self.file_name = file_name
        self.last = 0

        # check file existence
        # if yes then read last line to get last pid
        if os.path.exists(OUTPUT_PATH + self.file_name):
            with open(OUTPUT_PATH + self.file_name, 'r', encoding="UTF-8") as file:
                last_line = None
                current_line = None
                for line in file:
                    current_line = line.rstrip('\n')
                    if last_line is not None:
                        last_line = current_line
                last_line = current_line
            if last_line:
                self.last = int(eval(last_line)["id"])
        # if not then create
        else:
            with open(OUTPUT_PATH + self.file_name, 'w') as f:
                pass

    """def crawl(self, pid):
        print(pid)
        raw_text = crawler.illusts_text(pid=pid)
        # print(raw_text)
        parsed_text = json.loads(raw_text)
        if len(parsed_text["body"]) != 0:
            text_dict = parsed_text["body"][str(pid)]
            self.text_dict_list.append(text_dict)
            print(text_dict)"""

    def crawl(self, pid):
        print(pid)
        try:
            text = IllustText(raw=Connector.illusts_text(pid=pid))
        except:
            pass
        else:
            text_dict = text.get_info()
            self.text_dict_list.append(text_dict)
            # print(text_dict)

    def save(self):
        sorted_list = sorted(self.text_dict_list, key=lambda x: int(x['id']))
        TXTAppend(file_name=self.file_name, line_list=sorted_list)

    def main(self, maximum, minimum=1, pools=100, step=50000):
        print(self.last)
        times = []
        if minimum <= self.last:
            minimum = self.last + 1
        # pool = Pool(pools)
        p_pid = [pid for pid in range(minimum, maximum + 1)]
        print(p_pid)

        p_pid_list = [p_pid[i:i + step] for i in range(0, len(p_pid), step)]

        for p_pid in p_pid_list:
            print(p_pid)
            start = time.time()
            """
            pool.map(self.crawl, p_pid)
            """

            """threads = []
            for pid in p_pid:
                threads.append(threading.Thread(target=self.crawl, args=(pid,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()"""

            if len(p_pid) < pools:
                pools = len(p_pid)
            threads = [None] * pools
            processing = [False] * len(p_pid)

            def single_thread(index):
                processing[index] = True
                self.crawl(pid=p_pid[index])
                next_index = 0
                for i in range(len(p_pid)):
                    if not processing[i]:
                        next_index = i
                        single_thread(index=next_index)

            for i in range(pools):
                threads[i] = threading.Thread(target=single_thread, args=(i,))
                threads[i].start()
            for i in range(pools):
                threads[i].join()

            self.save()
            self.text_dict_list = []
            end = time.time()
            print(times)
            TXTAppend(file_name="time.txt", line_list=["%s, %s, %s" % (str(pools), str(step), str(end - start))])



if __name__ == "__main__":
    """infoStore = InfoStore(file_name="illusts_text_storage_001.txt")
    infoStore.main(maximum=1000000, minimum=0, pools=50, step=10000)"""

    for i in range(28, 112):
        maximum = i * 1000000
        minimum = (i - 1) * 1000000 + 1
        file_name = ("illusts_text_storage_%s.txt" % f'{i:0>3}')
        print(file_name)
        infoStore = InfoStore(file_name=file_name)
        infoStore.main(maximum=maximum, minimum=minimum, pools=1000, step=100000)
