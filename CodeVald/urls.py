from django.conf.urls import patterns, include, url
from django.contrib import admin
from CodeVald import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CodeVald.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', lambda r: HttpResponseRedirect('codevaldapp/')),
    # url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^$', views.index, name='index'),
    url(r'^codevaldapp/', include('codevaldapp.urls', namespace="codevaldapp")),
    url(r'^admin/', include(admin.site.urls)),
)
