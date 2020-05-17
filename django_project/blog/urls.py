
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('home', views.home, name="blog-about"),
    path('translation', views.translation, name="blog-about"),
    path('actionUrl', views.button_click),
    path('detial_click', views.detial_click, name='detial_click'),
    path('downloadexcel', views.download_excel_data),
    path('dtranslation', views.download_excel_transcription),
    path('ddictionary', views.download_excel_data),
    path('dictionary', views.dictionary_link, name='dictionary_click'),

#diciontary datatable 
 
    #url(r'^laptops$', views.display_laptops, name="display_laptops"),

    path(r'^laptops$', views.delete_laptop, name="delete_laptop")
]
