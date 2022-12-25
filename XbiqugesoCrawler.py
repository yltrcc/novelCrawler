# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests,re
import threading
import os
import logging
import time
"""
类说明:下载
Parameters:
    无
Returns:
    无
Modify:
    2019-02-28
"""
class downloader(object):
    def __init__(self):
        self.server = 'https://www.xbiquge.so/book/6684/'
        self.target = 'https://www.xbiquge.so/book/6684/'
        self.baseDir = 'D:\\smallTools\\17版2\\录制资料库\\'
        self.novelName = '斗破苍穹'
        self.names = []            #存放章节名
        self.urls = []            #存放章节链接
        self.nums = 0            #章节数
    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2019-02-28
    """
    def get_download_url(self):
        req = requests.get(url=self.target, verify=False)
        req.encoding = "gbk"
        html = req.text
        div_bf = BeautifulSoup(html, "html5lib")
        div = div_bf.find_all('div', id = 'list')
        a_bf = BeautifulSoup(str(div[0]), "html5lib")
        a = a_bf.find_all('a')
        self.nums = len(a)                                #剔除不必要的章节，并统计章节数
        for each in a:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))
    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2019-02-28
    """
    def get_contents(self,target):
        #停止1s 然后请求
        time.sleep(1)
        req = requests.get( url = target, verify=False)
        req.encoding = req.apparent_encoding  # 因为网站头部没有指定编码，因此需要requests自己去判断
        html = req.text
        bf = BeautifulSoup(html,"html5lib")
        texts = bf.find_all('div', id='content')
        texts = str(texts[0])
        texts =texts.replace('<br/><br/>     ', '\n') # 去掉<br/>
        texts =texts.replace('<div id="content" name="content">', '') # 去掉<br/>
        texts =texts.replace('<br/><br/>    ', '\n') # 去掉<br/>
        texts =texts.replace('</div>', '\n') # 去掉<br/>
        return texts
    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2019-02-28
    """
    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write("## " + name + '\n')
            # \n 替换 \n\n
            text = text.replace("\n", "\n\n")
            f.writelines(text)
            f.write('\n\n')

"""
    函数说明:使用多线程
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2019-02-28
    """
exitFlag = 0
class myThread(threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        global quotient
        print("开始线程：" + self.name)
        print_time(self.name, self.threadID)
        print("退出线程：" + self.name)

def print_time(threadName, threadID):
    start = threadID * quotient
    end = (threadID + 1) * quotient
    global remainder
    if exitFlag == 1:
        end = threadID * quotient + remainder
        for i in range(start, end):
            dl.writer(dl.names[i], dl.baseDir + dl.novelName + '\\' + dl.novelName + '第' + str(threadID + 1) + '部分.md',
                      dl.get_contents(dl.urls[i]))
            print('\n', '线程' + threadName + '已下载：  %.3f%%' % float((i-start) / (end - start) * 100), end='', flush=True)
    else:
        for i in range(start, end):
            if i >= dl.nums:
                break
            dl.writer(dl.names[i], dl.baseDir + dl.novelName + '\\' + dl.novelName + '第' + str(threadID + 1) + '部分.md',
                      dl.get_contents(dl.urls[i]))
            print('\n', '线程' + threadName + '已下载：  %.3f%%' % float((i-start) / (end - start) * 100), end='', flush=True)


if __name__ == "__main__":
    logging.captureWarnings(True)
    dl = downloader()
    dl.get_download_url()
    print(dl.novelName + ' 开始下载：')
    # 判断目录是否存在
    if not os.path.exists(dl.baseDir + dl.novelName):
        os.makedirs(dl.baseDir+ dl.novelName)
    quotient = 30
    remainder = dl.nums % 30
    threads = []
    num = 0
    cnt = 0
    # 每次执行 只开 10 个线程 执行完才执行下一批
    batch = 0
    while dl.nums > (num+1) * 30:
        thread = myThread(num, "Thread-" + str(num), 1)
        # 每个批次 开 5 个线程
        if (cnt < 5):
            threads.append(thread) # 先讲这个线程放到线程threads
            cnt += 1
        else:
            for t in threads:
                # 让线程池中的所有数组开始
                t.start()
            for t in threads:
                t.join()
            batch += 1
            print("第" + str(batch) + "批次")
            cnt = 0
            threads.clear()
            threads.append(thread) # 先讲这个线程放到线程threads
        num = num + 1
    exitFlag = 1
    thread1 = myThread(num, "Thread-" + str(num), 1)
    thread1.start()
    print('\r', '已下载：  100%', end='', flush=True)
    print('\n下载完成!')
