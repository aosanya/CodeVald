from django.conf.urls import patterns, url
from codevaldapp import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView, name='index'),
    url(r'^MySQLToXML/', views.ConvertMySQLToXML, name='MySQLToXML'),
    url(r'^XMLToCode/', views.XMLToCode, name='XMLToCode'),
    url(r'^Team/', views.Team, name='Team'),
)