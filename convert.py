#coding:utf-8
import urllib, urllib2
import traceback
import cookielib,re
#import sys, time
from bs4 import BeautifulSoup
import json
import os
import sys


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



#抓取的每本书的数据存储格式(json)
# {
#     "bookname": "xx",
#     "chapters": [
#         {
#             "chaptername": "xx",
#             "chaptercontent": [
#                 {"title": "xx", "text": "xx"},
#                 ......
#             ]
#         },
#         ......
#     ]
# }

def myprint(str):
    if str:
        print (str.decode("utf-8"))

try:

    for root, dirs, files in os.walk(".\input"):
        # 遍历文件
        for f in files:
            filename = os.path.join(root, f)

            with open(filename,'r') as load_f:
                load_dict = json.load(load_f)
                output_s = ""
                for chapter in load_dict["chapters"]:
                    if chapter["chaptername"]:
                        output_s += "<h1>"+chapter["chaptername"]+"</h1>"
                    for content in chapter["chaptercontent"]:
                        output_s += "<h2>"+content["title"]+"</h2>"
                        output_s += content["text"]

                with open('D:\spider\output\\'+f, 'w') as fw:
                    fw.write(output_s)


except Exception,e:
    print "Exception: %s" % str(e)
    traceback.print_exc()
#myprint (html)

