from os import environ
from django.db import models
# from django.core.files.storage import default_storage
# from google.cloud import pubsub_v1  # Google cloud publication subscribion library
import time           # time date libarary
import json           # Json paring

from django.shortcuts import render
# from django.http import HttpResponse
# import argparse  # for Parsing
import io        # seting eniromental variable
import os        # setting enivromental varible
import xlwt
from django.http import HttpResponse

# my scraping code start here

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

import re
import pandas as pd

# json object to go to translation page
def button_click(request):
    
    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translation.html', context)


def translation(request):

    posts = []
    df = pd.read_excel ('dictionary.xlsx')
    mylist = df['words'].tolist()
    r = re.compile('|'.join([r'\b%s\b' % w for w in mylist]), flags=re.I)

    #DAWN News
    
    url = 'https://www.dawn.com/latest-news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for article in soup.findAll("article"):
        try:
            href=article.find('a')
            href=href['href']
            img=article.find('img')
            img=img['src']
            header=article.find('h2')
            header=header.text
            prgh=article.find_all("div")[1]
            prgh=prgh.text
            date=article.find_all("span")[2]
            date=date.text
            articaltext=article.getText()
            #data mining
            listt=r.findall(articaltext)
            if listt:
                posts.append({
                'href': href,
                'img': img,
                'header': header,
                'prgh': prgh,
                'date': date,
                'News':'DAWN'
     
                })
        except :
            print("error")


            #THENEWS News
    url = 'https://www.thenews.com.pk/latest-stories'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for article in soup.findAll("div",{"class": "writter-list-item-story"}):
        try:
            href=article.find('a')
            href=href['href']
            img=article.find('a')
            img=img.find('img')
            img=img['src']
       
            header=article.find('h2')
            header=header.text
       
            prgh=article.find("p")
            prgh=prgh.text
            date=article.find("span")
            date=date.text
            #data mining
            articaltext=article.getText()
            listt=r.findall(articaltext)
            if listt:
                posts.append({
                'href': href,
                'img': img,
                'header': header,
                'prgh': prgh,
                'date': date,
                'News':'THENEWS'
     
             })
        except :
            print("error")


    
    
    #posts = get_buckets('1')

    context = {

        'posts': posts

    }
    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translation.html', context)
    # return render(request, 'blog/translation.html', {'tital': 'translation'})


def home(request):
    return render(request, 'blog/home.html', {'tital': 'Home'})



# here this is click when the user wants to go to next page for detail summary of text with word level confidacen
def detial_click(request):

    bob_name = request.GET.get("name")
    datee = request.GET.get("datee")
    audi_url = request.GET.get("publicurl")
    datee = request.GET.get("datee")

    posts = []
    main = []
    #posts = transcriberDetail(bob_name, main)

    context = {

        'posts': posts,
        'main': main,
        'text': bob_name,
        'datee': datee,
        'audi_url': audi_url,


    }
    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translationdetail.html', context)



def download_excel_data(request):
        # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename="SSRWordDictinary.xls"'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Transcription Name', 'Word', 'Confidance', 'Start Time', 'End  Time', ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row[0], font_style)
        ws.write(row_num, 1, my_row[1], font_style)
        ws.write(row_num, 2, my_row[2], font_style)
        ws.write(row_num, 3, my_row[3], font_style)
        ws.write(row_num, 4, my_row[4], font_style)

    wb.save(response)
    return response



def download_excel_transcription(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename="SSRTranslation.xls"'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0
    row_index = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['AudioName Name', 'Translation', 'Confidance', 'InterviewTime', 'Audio URL', ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # get your data, from database or from a text file...

    for my_row in lstAdName:
        row_num = row_num+1
        ws.write(row_num, 0, lstAdName[row_index], font_style)
        ws.write(row_num, 1, lstTranslation[row_index], font_style)
        ws.write(row_num, 2, lstConfidance[row_index], font_style)
        ws.write(row_num, 3, lstDate[row_index], font_style)
        ws.write(row_num, 4, lstUrl[row_index], font_style)
        row_index=row_index+1

    wb.save(response)
    return response
