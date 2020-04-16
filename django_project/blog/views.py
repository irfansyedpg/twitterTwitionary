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



# MY SQL 
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="twittter"
)
mycursor = mydb.cursor()



#newshunt
import re
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import re
import tweepy
# json object to go to translation page

import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime


def button_click(request):

    posts=[]
    date=request.GET.get("date")
    posts=get_news(date)


    context = {

        'posts': posts,
        'today':date

    }

    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translation.html', context)


def get_news(newsdate):

    posts = []
    df = pd.read_excel ('dictionary.xlsx')
    mylist = df['words'].tolist()
    r = re.compile('|'.join([r'\b%s\b' % w for w in mylist]), flags=re.I)
    
    url = "https://newshunt.io/getDateNews/"+newsdate


    myResponse = requests.get(url, verify=True)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)

        jData=jData['news']
        for key in jData:

        
            
            listt=r.findall(key['description'])
            if listt:
                header=re.sub('^A-Za-z0-9]+ +', ' ',key['title'])
                prgh=re.sub('^A-Za-z0-9]+ +', ' ',key['description'])
                header=re.sub("\s\s+", " ", header)
                prgh=re.sub("\s\s+", " ", prgh)
                posts.append({
                 
                'href': key['url'],
                'img':  key['media'],
                'header': header,
                'prgh':prgh ,
                'date': newsdate,
                'News':key['source'],
                'words':key['country'],
     
             })
            
    return posts

def translation(request):

    datee=datetime.today().strftime('%Y-%m-%d')
    posts=[]
    posts=get_news(datee)

    context = {

        'posts': posts,
        'today':datee

    }

    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translation.html', context)
    # return render(request, 'blog/translation.html', {'tital': 'translation'})



    
 


def home(request):
    return render(request, 'blog/home.html', {'tital': 'Home'})



# Twiteer scraping

def detial_click(request):

    consumer_key = "iJFZnuM0YHqwvFilNUBSVkzJU"
    consumer_secret = "412n9RVFyUc4lRH3RWBU4kRT1lz5NHWg81d6FEoMPQEvYJPRio"
    access_token = "813456180-jXG4M0Kpc80UjJF4bhwA0z9Bx8aZfAht4veyxSgc"
    access_token_secret = "Cvh3gsUS5Y4HpyfD1UdlMLfpxlqa47iYFo3vxogpP6blR"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    text_query = 'coronavirus'
    language = "en"
    text=""
    userid=""
    username=""
    dated=""
    location=""

    posts = []
    try:
# Pulling individual tweets from query
        for tweet in api.search(q=text_query,lang=language):
# Adding to list that contains all tweets
      #tweets.append((tweet.created_at,tweet.id,tweet.text))
            text=tweet.text
            userid=tweet.id
            dated=tweet.created_at
            username=tweet.user.screen_name
            location=tweet.user.location
            posts.append({
                'text': text,
                'userid': userid,
                'dated': dated,
                'username': username,
                'location': location,
     
                }) 
    except BaseException as e:
        time.sleep(3)

   
    #posts = transcriberDetail(bob_name, main)

    context = {

        'posts': posts
      


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
