# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 18:40:06 2018

@author: venka
"""

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv




#Twitter API credentials
consumer_key = "VN4OYU8QnNF9tNBq1CMMYKHTT"
consumer_secret = "kcdQ7MVLyTkB8vtEzqqx83p27AdYkB0wdfiyHV9zPvXdHhQ1nP"
access_key = "838270436077023232-Gpshjx7uO1AHoVgef4Td8cGFgM6l20q"
access_secret = "XWjtFWWMCjQsefcwdMerxSpsntgn2HtmHw3H7Un5dHQgw"


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print( "getting tweets before %s" % (oldest))

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv
    with open('K%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    #tweets from 28/12/2018
    get_all_tweets("realDonaldTrump")
    get_all_tweets("BarackObama")
    #nltk.download('vader_lexicon')
    #nltk.download('punkt')