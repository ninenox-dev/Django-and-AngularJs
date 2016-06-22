from django.conf.urls import patterns, include, url
from django.contrib import admin
from myapp import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^test/$', views.test, name='test'),
    url(r'^del/$', views.deldata, name='deldata'),
    url(r'^update/$', views.update, name='update'),
    url(r'^page2/$', views.page2, name='page2'),
    url(r'^recievecount/$', views.recievecount, name='recievecount'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signin/$', views.signin_view, name='signin'),
    #url(r'^pdf/$', views.generate_pdf_view, name='myview'),


)
