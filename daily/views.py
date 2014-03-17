# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from models import News
import urllib2
import json
from datetime import *

'''
todo list:
更改这垃圾的实现
图片的防盗链机制
'''


def fill_data(request):
    para_date = ''
    if 'date' in request.GET:
        para_date = request.GET['date']

    today = datetime.now().strftime('%Y%m%d')

    if len(para_date) == 8:
        pass
    else:
        dt = datetime.now()
        if dt.hour < 6:
            para_date = get_yesterday(dt).strftime('%Y%m%d')
        else:
            para_date = today  # 若用户传入非法参数，返回当天的日期

    news_list = News.objects.filter(date=para_date).order_by('-seq')

    if len(news_list) < 1:
        has_data = inner_update(para_date)
        if has_data:
            news_list = News.objects.filter(date=para_date).order_by('-seq')
        else:
            news_list = News.objects.filter(date=para_date).order_by('-seq')  # todo 这里要改进

    time1 = datetime.strptime(para_date, '%Y%m%d')
    time_str = time1.strftime('%Y.%m.%d-%A')
    return render(request, 'templay.html', {'now_image_url': news_list[0].image_url,
                                            'img_source': news_list[0].image_source,
                                            'date_text': time_str,
                                            'news': news_list})


def update(request):
    if 'date' in request.GET:
        para_date = request.GET['date']
        inner_update(para_date)
        return HttpResponse("<p>获取指定日期数据</p>")
    else:
        inner_update(None)
        return HttpResponse("<p>获取当前时间的数据 at "+datetime.now().strftime('%Y%m%d %H:%M:%S %Z')+"</p>")


def inner_update(para_date):
    if para_date is None:
        url = 'http://news.at.zhihu.com/api/1.2/news/latest'
    else:
        time1 = datetime.strptime(para_date, '%Y%m%d')
        para_date = get_tomorrow(time1).strftime('%Y%m%d')
        url = 'http://news.at.zhihu.com/api/1.2/news/before/'+para_date
    header = {'User-Agent':
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'}
    req = urllib2.Request(url, headers=header)
    webcode = urllib2.urlopen(req).read()

    data_dict = json.loads(webcode)  # 所有数据的dict
    news_count = len(data_dict['news'])  # 子dick news
    if news_count < 1:
        return False
    the_date = data_dict['date']

    data_dict['news'].reverse()  # 反转List

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
        new_obj.date = the_date

        new_obj.save()
    return True


def get_yesterday(some_day):
    a_day = timedelta(days=1)
    return some_day - a_day


def get_tomorrow(some_day):
    a_day = timedelta(days=1)
    return some_day + a_day