from os import environ
from django.db import models

import time           # time date libarary
import json           # Json paring

from django.shortcuts import render

import io        # seting eniromental variable
import os        # setting enivromental varible
import xlwt
from django.http import HttpResponse
import sys

# my scraping code start here

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import sqlite3
import sys
from firebase import firebase
firebase = firebase.FirebaseApplication('https://twitionary.firebaseio.com/', None) 
#from datetime import timedelta
import datetime







#newshunt
import re
import pandas as pd

import time
import re
import tweepy
# json object to go to news page

import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime

#getNews When Get News Button Clicked
def getNewsButton(request):

    posts=[]
    date1=request.GET.get("date1")
    date2=request.GET.get("date2")
    country=request.GET.get("contry")
    #lang=request.GET.get("lang")
  #  if lang=='Urdu':
       # posts=getNewsUrdu(date,country)
    #else:
    posts=getNewsEnglish(date1,date2,country)
    countries=getCountryNames()


    context = {

        'posts': posts,
      
        'country':countries,
         'date1':date1,
         'date2':date2

    }

    
    return render(request, 'blog/news.html', context)


def getNewsEnglish(newsdate1,newsdate2,country):


    if newsdate1==newsdate2:
        datee=datetime.today().strftime('%Y-%m-%d')
        datee2=datetime.today() + timedelta(days=1)
        datee2=datee2.strftime('%Y-%m-%d')
        newsdate1=datee
        newsdate2=datee2

    posts = []
    df = pd.read_excel ('dictionary.xlsx')
    mylist = df['words'].tolist()
    
    r = re.compile('|'.join([r'\b%s\b' % w for w in mylist]), flags=re.I)

    url = "https://newshunt.io/getBetweenDates/"+newsdate1+'/'+newsdate2
    if country!='World':
        url="https://newshunt.io/getBetweenDates/"+newsdate1+'/'+newsdate2+'/'+country
    
   

    print(url)

  
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
                sentiments=sentiment(prgh)
                posts.append({
                 
            'href': key['url'],
            'img':  key['media'],
            'header': header,
            'prgh':prgh ,
            'date': key['pub_date'],
            'News':key['source'],
            'words':key['country'],
            'sentiment':sentiments,
            'keyWord':listt,
     
             })
            
                 
            
    return posts



def getNewsUrdu(newsdate,country):



    posts = []
    df = pd.read_excel ('dictionary.xlsx')
    mylist = df['words'].tolist()
    r = re.compile('|'.join([r'\b%s\b' % w for w in mylist]), flags=re.I)
    
    url = "https://newshunt.io/getDateNews/"+newsdate

    count=[]
    myResponse = requests.get(url, verify=True)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)

        jData=jData['news']
        for key in jData:
            if key['country'] not in count:
                count.append(key['country'])
            listt=r.findall(key['description'])
            if country==key['country'] and key['lang']=='urdu':
                #if listt:
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
                'sentiment':"NA",
     
             })
            elif country=="World" and key['lang']=='urdu':
                 #if listt:
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
                'sentiment':"NA",
     
             })
                 
            
    return posts

from datetime import datetime, timedelta
countries=[]
def news(request):

    

    datee=datetime.today().strftime('%Y-%m-%d')
 

 
    

    posts=[]
    posts=getNewsEnglish(datee,datee,'pakistan')
    
    countries=getCountryNames()

    context = {

        'posts': posts,
        'date1':datee,
        'date2':datee,
        'country':countries

    }

    

    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/news.html', context)
    # return render(request, 'blog/news.html', {'tital': 'news'})

def getCountryNames():
    url = "https://newshunt.io/getCountriesIrfan"

    country=[]
    myResponse = requests.get(url, verify=True)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
        jData=jData['country']

        for key in jData:
            country.append(key["name"])

    return country        


def login(request):

   

    context = {

      

    }

    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/login.html', context)
    
 


def home(request):
    return render(request, 'blog/home.html', {'tital': 'Home'})



# Twiteer scraping

def detial_click(request):

    #df = pd.read_csv ('tweets.csv')
    posts=[]
    #for index, row in df.iterrows():
     #   posts.append({
      #          'text': row['text'],
       #         'username': row['Username'],
        #        'dated': row['tweetcreatedts'],
         #       'retweetcount': row['retweetcount'],
          #      'location': row['location'],
     
           #     }) 

    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db', timeout=20)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * FROM twitter ORDER BY id DESC LIMIT 30000"""
        cursor.execute(sqlite_select_query)
        
        for row in cursor:
            sentiments=sentiment(row[4])
            posts.append({
               'text': row[4],
                'username': row[5],
                'dated': row[2],
                'retweetcount': row[3],
                'location': row[1],
                'urll':row[6],
                'sentiment': sentiments }) 
       
        cursor.close()
        

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The Sqlite connection is closed")          

    #df = pd.read_csv ('tweets.csv')
    #df = firebase.get('twitter', '')  
    #posts=[]
    #for  row in df:
     #   posts.append({
      #          'text': df[row]['text'],
       #         'username': df[row]['username'],
        #        'dated': df[row]['tweetcreatedts'],
         #       'retweetcount': df[row]['retweetcount'],
          #      'location': df[row]['location'],
     
           #     }) 

    context = {

        'posts': posts
      


    }
    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translationdetail.html', context)

    

from textblob import TextBlob
def sentiment(text):
    analysis = TextBlob(text)
    # set sentiment 
    if analysis.sentiment.polarity >= 0:
        return 'positive'
    else: 
        return 'negative'
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
    columns = ['AudioName Name', 'news', 'Confidance', 'InterviewTime', 'Audio URL', ]

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


#dicinoaty data table

def dictionary_link(request):
    df = pd.read_excel ('dictionary.xlsx')
    #items = Laptops.objects.all()
    posts=[]
    for  index, row in df.iterrows():
        posts.append({
           'words': row['words'],
           'pk': row['pk'],
       
     
              }) 


    #items=df
    context = {
        'items': posts,
        'header': 'Laptops',
    }
    return render(request, 'blog/dictionary.html', context)


def delete_laptop(request):


    pk=request.GET.get("pk")
    df = pd.read_excel ('dictionary.xlsx')
  
    
    df = df.query("pk != "+pk)
    df.to_excel('dictionary.xlsx')
    df = pd.read_excel ('dictionary.xlsx')
    posts=[]

 
    for  index, row in df.iterrows():
      posts.append({
           'words': row['words'],
           'pk': row['pk'],
     
              }) 


    #items=df
    context = {
        'items': posts,
        'header': 'Laptops',
    }
  
    return render(request, 'blog/dictionary.html', context)

def insertkeywords(request):

    keywords=request.GET.get("words")
    df = pd.read_excel ('dictionary.xlsx')
    lstvalue=df['pk'].tail(1).index.item()
    df= df.append({'pk' : lstvalue+5 , 'words' : keywords} , ignore_index=True)
    if  keywords:
        df.to_excel('dictionary.xlsx')
    df = pd.read_excel ('dictionary.xlsx')
    posts=[]

 
    for  index, row in df.iterrows():
      posts.append({
           'words': row['words'],
           'pk': row['pk'],
     
              }) 


    #items=df
    context = {
        'items': posts,
        'header': 'Laptops',
    }
  
    return render(request, 'blog/dictionary.html', context)