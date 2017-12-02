from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/(?P<username>\w+)/$', views.viewUser, name='User Page'),
    url(r'^$', views.main, name='Main Page'),
    url(r'^demo$', views.demo, name='Demo Page'),
    url(r'^data$', views.sbdata, name='Starbucks Data'),
    url(r'^datascatter$', views.plotdata, name='Scatter plot Data')
]
