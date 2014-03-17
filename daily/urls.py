from django.conf.urls import patterns, include, url
from zhihu_daily.settings import TEMPLATE_DIRS

urlpatterns = patterns('',
    url(r'^$', 'daily.views.fill_data'),
    url(r'^css/(?P<path>.*)$','django.views.static.serve',
                         {'document_root':TEMPLATE_DIRS[0]+'/css'}),
    url(r'^images/(?P<path>.*)$','django.views.static.serve',
                         {'document_root':TEMPLATE_DIRS[0]+'/images'}),
    url(r'^update', 'daily.views.update'),
)