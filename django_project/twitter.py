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

import sqlite3


# In[3]:


consumer_key = "iJFZnuM0YHqwvFilNUBSVkzJU"
consumer_secret = "412n9RVFyUc4lRH3RWBU4kRT1lz5NHWg81d6FEoMPQEvYJPRio"
access_token = "813456180-jXG4M0Kpc80UjJF4bhwA0z9Bx8aZfAht4veyxSgc"
access_token_secret = "Cvh3gsUS5Y4HpyfD1UdlMLfpxlqa47iYFo3vxogpP6blR"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# In[33]:


def scraptweets(search_words, date_since, numTweets, numRuns):
    
    
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    print('function called')

    db_tweets = pd.DataFrame(columns = [ 'location', 'tweetcreatedts',
                                        'retweetcount', 'text', 'hashtags'])
    program_start = time.time()
  
    
    for i in range(0, numRuns):
        

        start_run = time.time()
    
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode='extended').items(numTweets)

        tweet_list = [tweet for tweet in tweets]

        noTweets = 0
        for tweet in tweet_list:

            #username = tweet.user.screen_name
            #acctdesc = tweet.user.description
            location = tweet.user.location
            #following = tweet.user.friends_count
            #followers = tweet.user.followers_count
            #totaltweets = tweet.user.statuses_count
            #usercreatedts = tweet.user.created_at
            tweetcreatedts = tweet.created_at
            retweetcount = tweet.retweet_count
            #hashtags = tweet.entities['hashtags']
            username = tweet.user.screen_name
            url =  f"https://twitter.com/user/status/{tweet.id}"
            try:
                    text = tweet.retweeted_status.full_text
            except AttributeError:  # Not a Retweet
                    text = tweet.full_text
        
            
            
            query = """INSERT into twitter(location,tweetcreatedts,retweetcount,text,Username,links)
                          VALUES (?,?,?,?,?,?)"""
            param = (location, tweetcreatedts, retweetcount, text, username,url)
            cursor.execute(query,param)
            #db_tweets.loc[len(db_tweets)] = ith_tweet
            noTweets += 1
        # Run ended:
        end_run = time.time()
        sqliteConnection.commit()
        cursor.close()

        if (sqliteConnection):
            sqliteConnection.close()
        duration_run = round((end_run-start_run)/60, 2)
        print('no. of tweets scraped for run {} is {}'.format(i + 1, noTweets))
        print('time take for {} run to complete is {} mins'.format(i+1, duration_run))
        time.sleep(920) #15 minute sleep time

# Once all runs have completed, save them to a single csv file:
    from datetime import datetime
    
    
    
    program_end = time.time()
    print('Scraping has completed!')
    print('Total time taken to scrap is {} minutes.'.format(round(program_end - program_start)/60, 2))


# In[34]:


def job():
    df = pd.read_excel ('dictionarytwets.xlsx')
    mylist = df['words'].tolist()
    search_words=""
    count=0
    for a in mylist:
        if count==0:
            search_words="#"+a.replace(" ", "")
        else:
            search_words=search_words+" OR #"+a.replace(" ", "")
        count=1
    #search_words=search_words+" OR #tariqjamil"
    #search_words = "#tariqjamil OR #COVID-19 OR #pakistan"
    date_since = "2020-04-23"
    #numTweets = 2500
    numTweets = 2500
    numRuns = 6
    # Call the function scraptweet1
    scraptweets(search_words, date_since, numTweets, numRuns)
    return


# In[ ]:

#job()
schedule.every().day.at("16:03").do(job)
schedule.every().day.at("16:03").do(job)



while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

