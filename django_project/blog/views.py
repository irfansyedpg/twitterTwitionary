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
def button_click(request):
    
    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translation.html', context)


def translation(request):

    posts = []
    df = pd.read_excel ('dictionary.xlsx')
    mylist = df['words'].tolist()
    r = re.compile('|'.join([r'\b%s\b' % w for w in mylist]), flags=re.I)

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
                'News':'DAWN',
                'words':listt
     
                })
        except :
            print("error")

#DailyTimePakistan 
    url = 'https://dailytimes.com.pk/pakistan/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for article in soup.findAll("article"):
        try:
            href=article.find('a')
            href=href['href']
            img=article.find('img')
            img=img['src']
            header=article.find('header')
            header=header.find('h2')
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
                'News':'DailyTimePakistan',
                'words':listt
     
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
                'News':'THENEWS',
                'words':listt
     
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
'''

#News Hunt News
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver", chrome_options=options)
    
    driver.get("https://newshunt.io/#/en/")
    more_buttons = driver.find_element_by_link_text("Latest News")
    driver.execute_script("arguments[0].click();", more_buttons)
#try:
    
    old_page = driver.page_source
    while True:
    
        for i in range(2):
            driver.execute_script("window.scrollBy(0,"+str(2000)+")")
            time.sleep(2)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break
#except :
 #   print("error")
    page_source = driver.page_source   
    soup = BeautifulSoup(page_source, 'lxml')

    reviews_selector = soup.find_all('div', class_='flex')
    for article in reviews_selector:
        img=article.find('img')
        img=img['src']
        href1=article.find('a')
        href=href1['href']
        header=href1.text
        prgh=article.find("p")
        prgh=prgh.text
        date=article.find("span",class_='news-time')
        date=date.text
        source=article.find("span",class_='news-source')
        source=source.text
        articaltext=article.getText()
        r = re.compile('|'.join([r'\b%s\b' % w for w in mylist]), flags=re.I)
        listt=r.findall(articaltext)
        if listt:
            posts.append({
            'href': href,
            'img': img,
              
            'header': re.sub(' +', ' ', header),
            'prgh': re.sub(' +', ' ', prgh),
            'date': date,
            'News':source,
            'words':listt

                    }) 

                    '''
  #DAWN News
   


    
 


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
