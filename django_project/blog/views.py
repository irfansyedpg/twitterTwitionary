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
#used for chart
from .fusioncharts import FusionCharts
from collections import OrderedDict
import mysql.connector

# SQL Connection String strats
mydb = mysql.connector.connect(
    host="localhost",
    database="twitter",
    user="root",
    passwd="",
)
cursor = mydb.cursor()
# countcursor = mydb.cursor(buffered=True)
# SQL Connection String Ends
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
            'country':key['country'],
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
    pie3d = FusionCharts("pie3d", "ex2" , "100%", "400", "chart-1", "json",
        # The data is passed as a string in the `dataSource` as parameter.
    """{
        "chart": {
            "caption": "Recommended Portfolio Split",
            "subCaption" : "For a net-worth of $1M",
            "showValues":"1",
            "showPercentInTooltip" : "0",
            "numberPrefix" : "$",
            "enableMultiSlicing":"1",
            "theme": "fusion"
        },
        "data": [{
            "label": "Equity",
            "value": "300000"
        }, {
            "label": "Debt",
            "value": "230000"
        }, {
            "label": "Bullion",
            "value": "180000"
        }, {
            "label": "Real-estate",
            "value": "270000"
        }, {
            "label": "Insurance",
            "value": "20000"
        }]
    }"""),

    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
#   return  render(request, 'blog/translationdetail.html', {'output' : pie3d.render(), 'chartTitle': 'Pie 3D Chart'})
# def get_AudioName_mysql():

#     sql = "select audioName from ssrDataa"
#     mydb._open_connection()
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     my_list = []
#     for x in myresult:
#         my_list.append(x[0])

#     mydb.close()
#     return my_list


# lstAdName = []
# lstTranslation = []
# lstConfidance = []
# lstDate = []
# lstUrl = []
    try:
        # sqliteConnection = sqlite3.connect('SQLite_Python.db', timeout=20)
        # cursor = sqliteConnection.cursor()
    
        cursor.cursor()
        print("Connected to Mysql")
        sqlite_select_query = """SELECT * FROM twitter ORDER BY id DESC LIMIT 30000"""
        cursor.execute(sqlite_select_query)
        
        for row in cursor:
            print("des",row[7])
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

    print('pie3',pie3d)

    context = {

        'posts': posts,
        'output':pie3d


    }

    # (request,the blog i am requestin,my json object)
    return render(request, 'blog/translationdetail.html', context)

    #used for chart
# from .fusioncharts import FusionCharts
def chart(request):
     
     
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
    mydb._open_connection()
    sqlite_select_query = """SELECT * FROM tbl_twitter ORDER BY id DESC LIMIT 30000"""
    cursor.execute(sqlite_select_query)
        
    for row in cursor:
        print("des",row[7])
        sentiments=sentiment(row[4])
        posts.append({
        'text': row[4],
            'username': row[5],
            'dated': row[2],
            'retweetcount': row[3],
            'location': row[1],
            'urll':row[6],
            'description':row[7],
            'following':row[8],
            'followers':row[9],
            'sentiment': sentiments }) 
    mydb.commit()
    #show data from 2nd table
    tweets_countq_query = """select COUNT(distinct Username) as username,COUNT(Id),COUNT(distinct location) as location from tbl_twitter order by Id"""
    cursor.execute(tweets_countq_query)
    count_row = cursor.fetchone()
    count_username = count_row[0]
    tweets_count = count_row[1]
    tweets_location = count_row[2]
    #end query
    
    #here we can show data from excel sheet total key words
    import openpyxl as xl
    wb = xl.load_workbook("dictionary.xlsx", enumerate)
    sheet = wb.worksheets[0]

    tweets_total_keywords = sheet.max_row
    # column_count = sheet.max_column
    print(tweets_total_keywords)


# start charts from here
    dataSource = OrderedDict()
     # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "TWEETS BY SENTIMENT"
    # chartConfig["subCaption"] = "In MMbbl = One Million barrels"
    # chartConfig["xAxisName"] = "Country"
    # chartConfig["yAxisName"] = "Reserves (MMbbl)"
    # chartConfig["numberSuffix"] = "K"
    chartConfig["theme"] = "fusion"

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # The data for the chart should be in an array wherein each element of the array  is a JSON object having the `label` and `value` as keys.
    # Insert the data into the `dataSource['data']` list.
    dataSource["data"].append({"label": 'Total Tweets', "value": tweets_count})
    dataSource["data"].append({"label": 'Total Users', "value": count_username})
    dataSource["data"].append({"label": 'Total Location', "value": tweets_location})
    dataSource["data"].append({"label": 'Key Words Define', "value": tweets_total_keywords})

    
    # dataSource["data"].append({"label": 'Terrible', "value": '115'})

    pie3d = FusionCharts("pie3d", "ex2" , "100%", "400", "chart-1", "json",
        # The data is passed as a string in the `dataSource` as parameter.
   
    {
        "chart": {
            "caption": "TWEETS BY TYPE",
            # "subCaption" : "For a net-worth of $1M",
            "showValues":"1",
            "showPercentInTooltip" : "0",
            # "numberPrefix" : "$",
            "enableMultiSlicing":"1",
            "theme": "fusion"
        },
        "data": [{
            "label": "Total Tweets",
            "value": tweets_count
            
        }, {
            "label": "Total Users",
            "value":count_username
        }, {
            "label": "Total Location",
            "value": tweets_location
        }, {
            "label": "Key Words Define",
            "value": tweets_total_keywords
        
        }]
    })

    column2D = FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)
  
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
#   return  render(request, 'blog/translationdetail.html', {'output' : pie3d.render(), 'chartTitle': 'Pie 3D Chart'})

   
    #End here we can show data from excel sheet total key words

    return render(request, 'blog/translationdetail.html', {
        'posts': posts,'output':pie3d.render(),'output1':column2D.render(),'tweets_count':tweets_count,'count_username':count_username,'tweets_location':tweets_location,'tweets_total_keywords':tweets_total_keywords
    })


from textblob import TextBlob
def sentiment(text):
    analysis = TextBlob(text)
    # set sentiment 
    if analysis.sentiment.polarity >= 0:
        return 'positive'
    else: 
        return 'negative'


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