# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import praw, datetime, json, math, os, time, string
from django.conf import settings
from random import randrange

#Retrieve file of most common words
file_path = os.path.join(settings.STATIC_ROOT, 'words.txt')
with open(file_path) as f:
    lines = [line.rstrip('\n') for line in open(file_path)]

#Insert Reddit API credentials
r = praw.Reddit(client_id='kcOeD0bMwMLHjA', client_secret="boWy-jafjjMu8nrCdvSkjilbsaM",
                     password='AnthonyGioDevPW', user_agent='testscript',
                     username='AnthonyGioDev')

#List of printable ASCII characters
printable = set(string.printable)

# Create your views here.
def viewUser(request, username):
    class subreddit:
        postCount = 0
        positive = 0
        negative = 0
        neutral = 0
        name = ''

        def __init__(self,name):
            self.name=name
        def increment(self, score):
            if score > 1:
                self.positive +=1
            elif score < 0:
                self.negative+=1
            else:
                self.neutral+=1
            self.postCount+=1

    def JSONEncoder(subreddit):
        return {
            'Subreddit': str(subreddit.name),
            'Positive': str(subreddit.positive),
            'Neutral': str(subreddit.neutral),
            'Negative': str(subreddit.negative)
        }
    user = r.redditor(username)
    days = 30 #Number of previous days post times to record
    #Current time
    today = datetime.datetime.now()
    #Last microsecond of today
    endOfDay = datetime.datetime(
        year=today.year,
        month=today.month,
        day=today.day,
    ) + datetime.timedelta(days=1,microseconds=-1)
    posts=[]
    subreddits=[]
    wordcount={}
    wordcountLabels=[]
    wordcountVals=[]
    postsPerHour=[0]*((days+1)*24) #Preinitialized to number of hours in the recorded number of days
    for comment in user.comments.new(limit=None):
        #Date from UNIX timestamp
        comment.created_utc=datetime.datetime.utcfromtimestamp(comment.created_utc)
        #Collect number of posts in each sub and scores
        newSub = True
        for i in subreddits or []:
             if i.name==comment.subreddit:
                i.increment(comment.score)
                newSub = False
        if newSub:
            s = subreddit(comment.subreddit)
            subreddits.append(s)
            subreddits[-1].increment(comment.score)
        #Collect post time data in terms of hours from the end of today
        if comment.created_utc > datetime.datetime.now()+datetime.timedelta(-days):
            temp = endOfDay - comment.created_utc
            hoursAgo = temp.total_seconds()/3600.0
            hoursAgo = math.ceil(hoursAgo)
            postsPerHour[int(hoursAgo)]+=1
        #Word counter
        for word in comment.body.lower().split():
            if word not in lines:
                if word.find('\'')==-1:
                    if word not in wordcount:
                        word = filter(lambda x: x in printable, word) #Filtering non-ASCII characters
                        word = word.replace("\"","")
                        wordcount[word]=1
                    else:
                        word = filter(lambda x: x in printable, word) #Filtering non-ASCII characters
                        word = word.replace("\"","")
                        wordcount[word]+=1
    #Sort by total posts descending
    subreddits = sorted(subreddits,key=lambda x: x.postCount, reverse=True)

    #Use only top 10
    subreddits = subreddits[0:10]

    #Encode to JSON
    subData = json.dumps([JSONEncoder(subreddit) for subreddit in subreddits])

    #Word counter (makeshift JSON encoder)
    for key, value in sorted(wordcount.iteritems(), key=lambda (k, v): (v, k)):
        wordcountLabels.append(key)
        wordcountVals.append(value)
    wordcountLabels=wordcountLabels[-101:-1]
    wordcountVals=wordcountVals[-101:-1]
    WCout=""
    for i in range(0,wordcountVals.__len__()):
        if i < wordcountVals.__len__()-1:
            WCout = WCout + "{\"word\":\""+str(wordcountLabels[i])+"\",\"count\":"+str(wordcountVals[i])+"},"
        else:
            WCout = WCout + "{\"word\":\""+str(wordcountLabels[i])+"\",\"count\":"+str(wordcountVals[i])+"}"


    #Finally, return request with all relevent data
    return render(request, 'RedditStats/viewuser.html', {'posts':posts, 'username': username, 'subData':subData, 'postsPerHour':postsPerHour, 'wordcount':WCout})

def main(request):
    today = datetime.datetime.now()
    endOfToday = datetime.datetime(
        year=today.year,
        month=today.month,
        day=today.day,
    ) + datetime.timedelta(days=1,microseconds=-1)
    endTimestamp = time.mktime(endOfToday.timetuple())
    beginOfToday = datetime.datetime(
        year=today.year,
        month=today.month,
        day=today.day
    )
    beginTimestamp = time.mktime(beginOfToday.timetuple())

    #Get random username
    authors=[]
    for submission in r.subreddit('all').hot(limit=250):
        authors.append(submission.author)
    index = randrange(0,len(authors))
    random = authors[index]
    return render(request, 'RedditStats/main.html',{'username':random})

def demo(request):
    return render(request, 'RedditStats/demo.html',{})

def sbdata(request):
    return render(request, 'RedditStats/data2.tsv', {})

def plotdata(request):
    return render(request, 'RedditStats/plotdata.csv', {})