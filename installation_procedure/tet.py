#-*- coding: utf-8 -*-
#ネットワーク演習 カラム取得用
#ディレクトリは自分でダウンロードしたものに変更してください
####
import sqlite3
from contextlib import closing
####
import sys
####
import gensim import corpora


#データ取得準備
#samplecount =680
dpath = '/home/iniad/cs2018_PL1/Youtube-Watch-History-Scraper/youtube_history.db'
connection = sqlite3.connect(dpath)
c = connection.cursor()

#文字化け回避

#query = '''
#        pragma encoding = 'unicode';
#        '''
#connection.execute(query)

#データ取得２
query = '''
        SELECT title FROM videoshistory
        '''

test = []
i=0
for row in c.execute(query):
    test.append(row[0].encode('utf-8'))
    i+=1

#for x in test:
#    print(x)
#stop_words = set('for a of the and to in'.split())

t = Tokenizer()
#for token in t.tokenize(test[1]):
#    print(token)

#connection.commit()
c.close()
connection.close()

#学習


#リコメンデーション作成


