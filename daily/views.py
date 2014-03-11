# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from models import News
import urllib2
import json
import time, datetime

'''
todo list:
request参数用法
time处理
垃圾的实现
图片的防盗链机制
'''

def fill_data(request):

    #request.
    date = ''
    if(request.GET.has_key('date')): date = request.GET['date']

    today = str(time.strftime('%Y%m%d',time.localtime(time.time())))
    if(len(date) == 8 ):
        pass
    else:
        date = today# 若用户传入非法参数，返回当天的日期

    news_list = News.objects.filter(date = date).order_by('-seq')

    if(len(news_list) < 1):

        hasData = inner_update(date)
        if(hasData):
            news_list = News.objects.filter(date = date).order_by('-seq')
        else:
            news_list = News.objects.filter(date = today).order_by('-seq')

    time1 = time.strptime(date, '%Y%m%d')
    time_str =time.strftime('%Y.%m.%d-%A',time1)
    return render(request, 'templay.html', {'now_image_url':news_list[0].image_url,
                                            'img_source':news_list[0].image_source,
                                            'date_text': time_str,
                                            'news':news_list})


def update(request):
    date = request.GET['date']
    inner_update(date)
    return HttpResponse("<p>获取数据</p>")

def inner_update(date):
    url = ''
    if(date == None):
        url = 'http://news.at.zhihu.com/api/1.2/news/latest'
    else:
        time1 = time.strptime(date, '%Y%m%d')
        datetime1 = datetime.datetime(*time1[:3])
        datetime2 = datetime1 + datetime.timedelta(1)
        date = datetime2.strftime('%Y%m%d')
        url = 'http://news.at.zhihu.com/api/1.2/news/before/'+date
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'}
    req = urllib2.Request(url, headers = header)
    webcode = urllib2.urlopen(req).read()

    data_dict = json.loads(webcode) # 所有数据的dict
    news_count = len(data_dict['news']) #子dick news
    if(news_count < 1): return False;
    date = data_dict['date']

    data_dict['news'].reverse() #反转List

    for i in range(0, news_count):
        new_obj = News()

        a_new = data_dict['news'][i]
        new_obj.id = a_new['id']
        new_obj.title = a_new['title']
        new_obj.share_url = a_new['share_url']
        new_obj.api_url = a_new['url']
        new_obj.image_url = a_new['image']
        new_obj.image_source = a_new['image_source']
        new_obj.seq = i
        new_obj.date = date

        new_obj.save()
    return True