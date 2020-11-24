#coding:utf-8
import urllib, urllib2
import traceback
import cookielib,re
#import sys, time
import json

import sys


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


#<iframe src="//player.bilibili.com/player.html?aid=12247594&bvid=BV1gx411B7E8&cid=20183250&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

#<iframe src="//player.bilibili.com/player.html?aid=12247594&bvid=BV1gx411B7E8&cid=20250006&page=40" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

filename = "细讲弟子规(蔡礼旭).txt"
course_prefix = "细讲弟子规"
course_num = 41
link_prefix = '<iframe src="//player.bilibili.com/player.html?aid=12247594&bvid=BV1gx411B7E8&cid=20183250&page='
link_suffix = '" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>'


def myprint(str):
    if str:
        print (str.decode("utf-8"))

try:
   
    output_str = ''

    for number in range(1, course_num+1):

        output_str += course_prefix+ ('%02d' % number)
        output_str += '\n'
        output_str += link_prefix + str(number) + link_suffix
        output_str += '\n'
        output_str += '\n'
     
    #把每个视频的链接保存到文件中
    with open('D:\spider\\'+filename.decode("utf-8"), 'w') as f:
        f.write(output_str)
    myprint ("saving file: " + filename.decode("utf-8") + "\n")

except Exception,e:
    print "Exception: %s" % str(e)
    traceback.print_exc()
#myprint (html)

