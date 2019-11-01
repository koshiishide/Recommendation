from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import sqlite3
from janome.tokenizer import Tokenizer
import collections
import random
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from googleapiclient.discovery import build
from .youtube_data_model import YouTubeData

'''
URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = 'AIzaSyBe5M4o9ERpdcwkR8hJv6B7e2iBovcWsb0'

PL_URL = 'https://www.googleapis.com/youtube/v3/playlists'
'''


def youtube(request):
    #データ取得準備
    #samplecount =680
    dpath = '/home/cch4n/django/network-practice-team/python_testcode/youtube_history.db'
    connection = sqlite3.connect(dpath)
    c = connection.cursor()


    #データ取得２
    query = '''
            SELECT title FROM videoshistory
            '''

    test = []
    i=0
    for row in c.execute(query):
        test.append(row[0])
        i+=1


    t = Tokenizer()
    word_dic={}

    for i in test:
        malist = t.tokenize(i)
        for w in malist:
            word = w.surface
            ps   = w.part_of_speech
        if ps.find('名詞')< 0: continue

        if not word in word_dic:
            word_dic[word] = 0
        word_dic[word] +=1

    keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)


    newlist=[]
    count = 0
    for i in keys:
        if len(i[0]) != 1 and ord((i[0])[0])>= 65 :
            newlist.append(i[0])
        count +=1

    t = random.choice(newlist)
    DEVELOPER_KEY = "AIzaSyDhljyqnmT_h_QNzuCUNbs6-s5bJMGaloQ"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    u1=""
    u2=""
    u3=""
    u4=""
    u5=""
     
    ytdata = YouTubeData(q=t, max_results=5)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    
    search_response = youtube.search().list(
        q=ytdata.q,
        part="id,snippet",
        maxResults=ytdata.max_results
    ).execute()

   
    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s " % (search_result["id"]["videoId"]))
    
    u1="http://www.youtube.com/embed/"+videos[0]
    u2="http://www.youtube.com/embed/"+videos[1]
    u3="http://www.youtube.com/embed/"+videos[2]
    u4="http://www.youtube.com/embed/"+videos[3]
    c.close()
    connection.close()

    testview = {'url1':u1,'url2':u2,'url3':u3,'url4':u4}
    return render(request, 'youtube/youtube.html',testview)

@login_required
def login(request):
    return render(request, 'youtube/login/login.html', {})
