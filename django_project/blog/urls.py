
from django.urls import path
from django.conf.urls import url
from . import views
# from blog.views import PostTemplateView, post_json

urlpatterns = [
    path('', views.index, name="blog-home"),
    path('home', views.home, name="blog-about"),
    path('news', views.news, name="blog-about"),
    path('actionUrl', views.getNewsButton),
    path('detial_click', views.chart, name='detial_click'),
    path('login', views.login, name='login'),
    path('dictionary', views.dictionary_link, name='dictionary_click'),
    path('insertkeywords', views.insertkeywords),
    # path('delete_laptop', views.delete_laptop),
    path('search', views.search_keywords,name='search_page'),
    path('twitter_details', views.twitter_details,name='twitter_details'),
    path('twitter_search', views.twitter_search,name='twitter_search'),
    path('twitter_list', views.twitter_list,name='twitter_list'),
    path('index', views.index,name='index'),
    path('mapper', views.mapper,name='mapper'),
    path('addkeywords', views.add_keywords,name='addkeywords'),
    path('delete_keywords', views.delete_keywords,name='delete_keywords'),
    path('updatekeywords', views.updatekeywords,name='updatekeywords'),
    path('keywords', views.post_json,name='keywords'),
    path('reports', views.reports,name='reports'),

]
#helo