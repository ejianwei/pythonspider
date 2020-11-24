#coding:utf-8
import urllib, urllib2
import traceback
import cookielib,re
#import sys, time
from bs4 import BeautifulSoup
import json

import sys


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#search_list = ["左传", "吕氏春秋", "列子", "孙子兵法", "墨子", "淮南子", "庄子", "韩非子", "老子", "史通", "战国策", "史记", "山海经", "大学", "中庸", "孟子", "论语", "孝经", "礼记", "周礼", "诗经", "周易", "金刚经", "心经", "维摩诘经", "六祖坛经", "楞严经", "法华经", "华严经", "了凡四训"]
search_list = ["大学", "中庸", "孟子", "论语", "孝经", "礼记", "周礼", "诗经", "周易", "金刚经", "心经", "维摩诘经", "六祖坛经", "楞严经", "法华经", "华严经", "了凡四训"]



base_url = "https://so.gushiwen.org"


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
    # #前半部分的链接(注意是http，不是https)
    # url = 'https://so.gushiwen.org/search.aspx?value=%E9%87%91%E5%88%9A%E7%BB%8F'
 
    # #获得一个cookieJar实例
    # cj = cookielib.CookieJar()
    # #cookieJar作为参数，获得一个opener的实例
    # opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
    # opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
    # #访问登陆页面，访问之后cookieJar会自定保存cookie
    

    for book in search_list:

        #第一步，搜书
        search_url = base_url + "/search.aspx?value=" + book

        search_response = urllib2.urlopen(search_url)
        search_html = search_response.read()
        search_soup = BeautifulSoup(search_html, 'html.parser')

        book_json = {}
        book_json["bookname"] = book
        book_json["chapters"] = []

        #得到书的链接
        book_url = ""
        for data in search_soup.select('.divimg'):
            book_url = data.a.get('href')
            break

        if not book_url:
            myprint ("搜索失败：" + book)
            with open('D:\spider\\failed.log', 'w+') as f:
                f.write(book+'\n')
            continue

        book_url = base_url + book_url

        myprint ("搜索成功: " + book)
        myprint ("链接: " + book_url)
        #打开书的链接
        book_response = urllib2.urlopen(book_url)
        book_html = book_response.read()
        book_soup = BeautifulSoup(book_html, 'html.parser')


        #每本书分两级结构，大章节和小章节
        #大章节
        for data in book_soup.select('.bookcont'):
            
            chapter_json = {}
            chapter_json["chaptername"] = ""
            chapter_json["chaptercontent"] = []

            for chapter in data.select('.bookMl'):
                #myprint (chapter.string)
                #chapters_json.append(chapter.string)
                chapter_json["chaptername"] = chapter.string
                break

            myprint("抓取章节："+ chapter_json["chaptername"])

            for span in data.select('span'):
                #在一个chapter下，遍历每个小节的内容

                #print (span.attrs)
                #print type(span.attrs)
                title = span.string
                myprint (title)
                link = span.a.get('href')
                myprint (link)
                
                #如果该章节没有链接（古籍中该章缺失），则跳过后续处理。
                if not link:
                    #title_list = [title, ""]
                    #chapter_json["chaptercontent"].append([title, ""])
                    chapter_json["chaptercontent"].append({"title": title, "text":""})
                    continue
                
                text_response = urllib2.urlopen(link)
                text_html = text_response.read()
                text_soup = BeautifulSoup(text_html, 'html.parser')

                #myprint (text_html)
                for text in text_soup.select('.contson'):
                    #myprint (text.get_text())
                    #title_list = [title, text.get_text()]
                    #chapter_json["chaptercontent"].append([title, text.get_text()])
                    #print (text.attrs)
                    #print type(text.attrs)
                    #myprint(text)
                    #print text
                    paragraphs = ""
                    for p in text:
                        if p.string:
                            paragraphs = paragraphs + "<p>" + p.string + "</p>"

                    chapter_json["chaptercontent"].append({"title": title, "text":paragraphs})
                    break
                #测试目的
                #break

            #上面遍历抓取了一个chapter的内容，把它存入到book json中，下一次循环继续抓取下一个chapter
            book_json["chapters"].append(chapter_json)
            #测试目的
            #break

        jsondata = json.dumps(book_json, ensure_ascii=False, indent=4)


        filename = book+'.txt'
        #抓完了一本书的内容，保存到文件中
        with open('D:\spider\\'+filename.decode("utf-8"), 'w') as f:
            f.write(jsondata)
        myprint ("saving file: " + filename.decode("utf-8") + "\n")

        #测试目的
        #break

except Exception,e:
    print "Exception: %s" % str(e)
    traceback.print_exc()
#myprint (html)

