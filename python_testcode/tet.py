#-*- coding: utf-8 -*-
#ネットワーク演習 カラム取得用
#ディレクトリは自分でダウンロードしたものに変更してください
####
import sqlite3
#from contextlib import closing
####
#import sys
####
from janome.tokenizer import Tokenizer
import collections
####
import random
###
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from googleapiclient.discovery import build


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


DEVELOPER_KEY = "AIzaSyDhljyqnmT_h_QNzuCUNbs6-s5bJMGaloQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

u1=""
u2=""
u3=""
u4=""
u5=""


def youtube_search(options):
      
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s " % (search_result["id"]["videoId"]))
 
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
  u1=videos[0]
  u2=videos[1]
  u3=videos[2]
  u4=videos[3]
  u5=videos[4]

if __name__ == "__main__":
  # 検索ワード
  argparser.add_argument("--q", help="Search term", default=random.choice(newlist))
  # 検索上限
  argparser.add_argument("--max-results", help="Max results", default=5)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

c.close()
connection.close()

