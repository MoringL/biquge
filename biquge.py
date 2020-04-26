import os
from urllib import parse
import requests
from docx import Document
from lxml import etree
import re
import random
from multiprocessing import Pool

import time


class biqugeCrawl():

    m_url = "http://www.biquge.tv/"

    # 爬取文章内容函数
    def parse(self, url_name):
        url = url_name[0]
        name = url_name[1]

        try:
            response = requests.get(url=url, headers=self.__random_ua())
            html = response.content.decode('gbk')

            root = etree.HTML(response.content)
            book_name = root.xpath('//div[@class="con_top"]/a[2]/text()')[0]

            content = "".join(re.findall('<div id="content">(.*?)</div>', html, re.S))

            content = re.sub("<.*?>", "", re.sub("&nbsp;&nbsp;", " ", content))

            # 创建document对象
            document = Document()

            # 将文本写入文档
            document.add_paragraph(content)

            document.save("《{}》/《{}》.docx".format(book_name, name))

            print('《' + name + '》已下载完成')

        except Exception as e:
            with open("./log.txt", "a+", encoding="utf-8") as file:
                file.write("*"*30+"\n"+str(e))
            print("出现异常，下载中断，请查看log文件！")
            pass

    # 随机UA
    def __random_ua(self):
        UA = ["Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0",
              "Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot;Gecko/20100101 Firefox/38.0",
              "Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0",
              "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
              "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
              "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0",
              "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
              "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
              "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
              "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0",
              "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
              "Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/20.6.14",
              "Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
              "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
              "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
              "Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; Gecko/20100101 Firefox/38.0",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
              ]

        headers = {
            "User-Agent": {}
        }

        headers["User-Agent"] = random.choice(UA)

        return headers

    # 查询书籍函数
    def search_book(self):
        serach_url = "http://www.biquge.tv/modules/article/search.php?searchkey={}"

        name = input("请输入书名：")

        name = parse.quote(name.encode('gbk'))

        url = serach_url.format(name)

        response = requests.get(url=url, headers=self.__random_ua())

        root = etree.HTML(response.content)

        try:
            book_name = root.xpath('//*[@id="nr"]/td[1]/a/text()')[0]

            book_author = root.xpath('//*[@id="nr"]/td[3]/text()')[0]

            book_url = root.xpath('//*[@id="nr"]/td[1]/a/@href')[0]

            return [book_name, book_author, book_url]

        except:
            return None

    # 下载函数
    def download(self, book_name, url):
        url = url.strip()
        response = requests.get(url=url, headers=self.__random_ua())
        root = etree.HTML(response.content)

        content_urls = list(map(lambda x: "http://www.biquge.tv/" + x, root.xpath('//*[@id="list"]/dl/dd/a/@href')[9:]))
        content_names = root.xpath('//*[@id="list"]/dl/dd/a/text()')[9:]

        # 创建以书名命名的文件夹
        path = '《' + book_name + '》'
        if not os.path.exists(path):
            os.mkdir(path)

        utls_names = [i for i in zip(content_urls, content_names)]

        pool = Pool(processes=5)
        pool.map(self.parse, utls_names)

        print("《{}》下载完毕!".format(book_name))


if __name__ == '__main__':
    biquge = biqugeCrawl()
    print("----笔趣阁(http://www.biquge.tv/)小说爬虫----")
    print("1-------------搜索小说")
    print("2-------------通过小说链接下载")
    print("3----------------退出")

    flag = input("请输入指令选择相应功能：")

    while 1:
        error_str = ""

        if flag == "1":
            book = biquge.search_book()

            if book is not None:
                flag = input("搜索到的书名为《{}》，作者名为{},请确认是否下载【Y/N】".format(book[0], book[1]))
                while 1:
                    if flag == 'Y' or flag == 'y':
                        biquge.download(book[0], book[2])
                        break
                    elif flag == 'N' or flag == 'n':
                        break
                    else:
                        flag = input("请正确输入【Y/N】！")
            else:
                print("查无此书")
        elif flag == '2':
            book_url = input("请输入小说链接：")
            book_name = input("请输入小说名（可自定义）")
            biquge.download(book_name, book_url)
        elif flag == "3":
            exit(1)

        else:
            error_str = "指令错误，"

        flag = input("{}请重新输入指令选择相应功能【1.搜索；2.链接下载；3.退出】：".format(error_str))


