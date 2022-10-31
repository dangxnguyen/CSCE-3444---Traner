#from django.conf.urls import url, include
from . import views
from django.urls import include, re_path

app_name = 'home'

urlpatterns = [
    re_path(r'^$', views.home, name="home"),
    re_path(r'home/homepage.html', views.home, name="home"),
    re_path(r'^login.html/$', views.login_view, name="login"),
    re_path(r'^options/$', views.options_view, name="options"),
    re_path(r'^compose/$', views.compose_view, name="compose"),
    re_path(r'options/compose.html', views.compose_view, name="compose"),
  # re_path(r'^inbox/$', views.inbox_view, name="inbox"),
  # re_path(r'^sent/$', views.sent_view, name="sent"),
  # re_path(r'^trash/$', views.trash_view, name="trash"),
   
]