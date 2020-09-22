
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('home', views.home, name="blog-about"),
    path('news', views.news, name="blog-about"),
    path('actionUrl', views.getNewsButton),
    path('detial_click', views.chart, name='detial_click'),
    path('login', views.login, name='login'),

  

    path('dictionary', views.dictionary_link, name='dictionary_click'),
    path('insertkeywords', views.insertkeywords),

#diciontary datatable 
 
    #url(r'^laptops$', views.display_laptops, name="display_laptops"),

    path(r'^laptops$', views.delete_laptop, name="delete_laptop")
]
