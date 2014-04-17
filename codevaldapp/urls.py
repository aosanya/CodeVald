from django.conf.urls import patterns, url
from codevaldapp import views

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),
    url(r'^MySQLToXML/', views.ConvertMySQLToXML, name='MySQLToXML'),
    url(r'^GenerateCode/', views.GenerateCode, name='GenerateCode'),
    url(r'^Team/', views.Team, name='Team'),
)