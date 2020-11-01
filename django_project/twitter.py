#!/usr/bin/env python
# coding: utf-8

# In[2]:


import schedule
import time
import requests
import re
import pandas as pd
import tweepy
import os
import mysql.connector


# In[3]:


consumer_key = "iJFZnuM0YHqwvFilNUBSVkzJU"
consumer_secret = "412n9RVFyUc4lRH3RWBU4kRT1lz5NHWg81d6FEoMPQEvYJPRio"
access_token = "813456180-jXG4M0Kpc80UjJF4bhwA0z9Bx8aZfAht4veyxSgc"
access_token_secret = "Cvh3gsUS5Y4HpyfD1UdlMLfpxlqa47iYFo3vxogpP6blR"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


#SQL Connection String strats
mydb = mysql.connector.connect(
    # host="Localhost",
    # # host="localhost",
    # database="twitter",
    # user="tweehunt",
    # passwd="TweeHunt!@#321",
    # host="localhost",
    host="localhost",
    database="twitter",
    user="root",
    passwd="",
  
) 
mycursor = mydb.cursor()
# In[33]:

# langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
#          'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
#          'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
#          'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
#          'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}
def scraptweets(search_words, date_since, numTweets, numRuns):
    
    
    print('function called function')
    db_tweets = pd.DataFrame(columns = [ 'location', 'tweetcreatedts',
                                        'retweetcount', 'text', 'hashtags'])
    program_start = time.time()
    mydb._open_connection() #mysql connection opens 
  
    
    for i in range(0, numRuns):
        

        start_run = time.time()
    
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode='extended').items(numTweets)
          
        
        tweet_list = [tweet for tweet in tweets]
        # print(tweet_list)
        noTweets = 0
        for tweet in tweet_list:
            # username = tweet.user.screen_name
            acctdesc = tweet.user.description

            location = tweet.user.location

            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            usercreatedts = tweet.user.created_at

            tweetcreatedts = tweet.created_at
            retweetcount = tweet.retweet_count

            hashtags = tweet.entities['hashtags']
            tweet_id= tweet.id

            # print(tweetId)
            username = tweet.user.screen_name
            url =  f"https://twitter.com/user/status/{tweet.id}"
            try:
                    text = tweet.retweeted_status.full_text
            except AttributeError:  # Not a Retweet
                    text = tweet.full_text
            query = "INSERT into tbl_twitter(location,tweetcreatedts,retweetcount,text,Username,links,acctdesc,following,followers,totaltweets,usercreatedts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (location, tweetcreatedts, retweetcount, text, username,url,acctdesc,following,followers,totaltweets,usercreatedts)
            mycursor.execute(query,val)
            # print("1 record inserted, ID:", mycursor.lastrowid)
            twitter_col_id=mycursor.lastrowid
            path=[]
            for i in hashtags:
                tagtext= i['text']
                query1 = "INSERT into tbl_hashtags(title,twitter_id) VALUES (%s, %s)"
                val1 = (tagtext,twitter_col_id)
                      
            mycursor.execute(query1,val1)
            noTweets += 1
            mydb.commit()
        # Run ended:
        end_run = time.time()
        
        mydb.close()

     
        duration_run = round((end_run-start_run)/60, 2)
        print('no. of tweets scraped for run {} is {}'.format(i + 1, noTweets))
        print('time take for {} run to complete is {} mins'.format(i+1, duration_run))
        #time.sleep(920) #15 minute sleep time

# Once all runs have completed, save them to a single csv file:
    from datetime import datetime
    
    
    
    program_end = time.time()
    print('Scraping has completed!')
    print('Total time taken to scrap is {} minutes.'.format(round(program_end - program_start)/60, 2))


# In[34]:


def job():
    try:
        # df = pd.read_excel ('dictionarytwets.xlsx')
        # mylist = df['words'].tolist()
        # print(mylist)
        posts = []
        mydb._open_connection()
        # df = pd.read_excel ('dictionarytwets.xlsx')
        # mylist = df['words'].tolist()
        sqlite_select_query = """SELECT Keywords FROM tbl_keywords"""
        mycursor.execute(sqlite_select_query)
        for i in mycursor:
            posts.append(
            i[0]
            )
        mylist=posts
        print(mylist)
        search_words=""
        count=0
        for a in mylist:
            if count==0:
                search_words="#"+a.replace(" ", "")
            else:
                search_words=search_words+" OR #"+a.replace(" ", "")
                
            count=1
        date_since = "2020-09-20"

        numTweets = 1000
        numRuns = 1
        print(search_words)
        scraptweets(search_words, date_since, numTweets, numRuns)
    except Exception as e:
        print(e)
    finally:        
        return


# In[ ]:

job()
#schedule.every().day.at("16:03").do(job)




#while True:
 #   schedule.run_pending()
  #  time.sleep(60) # wait one minute

