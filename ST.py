# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import sqlite3
import codecs #
from _MM.basic import WhatCode, WhatLang2, TimeLine
import re #
import sys
import os
import io
import winsound
import stardict
#d=stardict.open_dict('_MM/dict/stardict.db')
import _MM.mydict
from _MM.word import Word_formatting_txt, Word_KWord, Word_KWord2
from opencc import OpenCC
import yichen0831
import pkuseg #北京這個可以開多線程 # pip install pkuseg #NLP系列（一）, nthread=20開多線程 - 简书 - https://parg.co/E2s
#字幕進資料庫，把原來的檔名 當作一個欄位加進去，再加上一欄關鍵字，前後包引號多關鍵字用逗號分隔
import msvcrt

count_files = count_files_new = int()
exline = ''
#%%#設定路徑
WDir = os.path.dirname(__file__) + "/Eric_data_3/" # S:/ENV + 
#WDir = os.path.dirname(__file__) + "/sandbox/" # S:/ENV + 

#判斷一個字元（不是一行句子）
def is_alphabet(uchar): # python 利用utf-8编码判断中文英文字符 - CSDN博客 - https://parg.co/rG6
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False
    
#處理一個字幕檔
def EachST(EachSrt): 
    part = []
    GetNextTwo = int(0)
    content = io.open(WDir + EachSrt, "r", encoding = 'utf-8-sig').read()
    for eachline in content.split('\n'):
        if eachline == '' or len(eachline) >= 100: #避開垃圾
            continue
        
        #攔胡，平常不作用，除非GetNextTwo = 2
        if GetNextTwo != 0: #不為0。可能是GetNextTwo2中文或GetNextTwo1英文。
            #print('' + str(eachline) + ',' + str(WhatLang2(eachline)) + ',' + str(GetNextTwo))

            if GetNextTwo == 2 and WhatLang2(eachline) != 'Zh': # 排除英文在第一行，中文在第二行的字幕
                #print('這應是中文' + str(eachline) + ',' + str(WhatLang2(eachline)) + ',' + str(GetNextTwo))                
                part = [] #資料清空
                GetNextTwo = int() #計數歸零
                continue
            
            if GetNextTwo == 1 and WhatLang2(eachline) != 'En': # 排除第二行也是中文的（兩行中文兩行英文那種字幕）
                part = [] #資料清空
                GetNextTwo = int() #計數歸零
                continue
            
            part.append(eachline) #第一次附加中文行 #-1後第二次來附加英文行
            GetNextTwo = GetNextTwo - 1
            
            #如果GetNextTwo是1，就繼續去抓下一行
            if GetNextTwo != 0:                
                continue
            
            #GetNextTwo 是 0。來自於if GetNextTwo != int(0)，而現在是0，表示一組已經完成
            else: # 完成一組，這時GetNextTwo == 0
                
#                #print('這應是英文' + str(eachline) + ',' + str(WhatLang2(eachline)) + ',' + str(GetNextTwo))
#                if WhatLang2(eachline) == 'Zh': #避開兩行中文的
#                    #print('這應是英文' + str(eachline) + ',' + str(WhatLang2(eachline)) + ',' + str(GetNextTwo))   
#                    part = [] #資料清空
#                    GetNextTwo = int() #計數歸零
#                    continue
#                else:
#%%#--- # 寫入數據 ---
#
#

                #插入数据:一次性插入很多行，你應該使用：executemany
                cur.execute("INSERT INTO t_zh(ZhLine,EnLine,Episode,TLine,OriPKey) VALUES(?,?,?,?,?)", (part[2], part[3], EachSrt, part[1], part[0])) #简单的插入一行数据,不过需要提醒的是,只有提交了之后,才能生效.我们使用数据库连接对象con来进行提交commit和回滚rollback操作.    
                con.commit()
                #print('\n'.join(part) + '\n') #檢查用，不要刪
                part = [] #資料清空

            
        if TimeLine(eachline) is False: 
            #False /*BUG*/
            # 美剧字幕下载 请登陆 www.YYeTs.net,False
            #BBC Life 02 Reptiles and Amphibians
            #9 feet long. A top predator.,
            #print(eachline + ',' + str(TimeLine(eachline)))
            
            exline = eachline #累積，但是在時間軸找到的時候，這行即是單檔的PKey
            continue
                  
        #if TimeLine(eachline) is True: #是時間軸，中
        else:
            #print('' + str(eachline) + ',' + str(WhatLang2(eachline)) + ',' + str(TimeLine(eachline)))
            #01:00:35,560 --> 01:00:39,390,Num,True
            #因為第一個字是數字所以WhatLang2會是Num
            part.append(exline)
            part.append(eachline) # 本行時間軸，共累積2行
            #print('# ' + str(part)) # 這裡完美
            
            GetNextTwo = int(2)
            exline = ''
            continue
            


        #if '-->' in eachline:
            
        
#        if eachline.encode( 'UTF-8' ).isdigit():
#            exline = eachline
#            continue
            

#    '''
#    #PKey 主鍵欄 row[0]
#    #ZhLine 讀取中文欄 row[1]
#        #檢查格式
#    #EnLine 讀取英文欄 row[2]
#        #檢查格式
#        
#    #From 檔名欄 row[3]
#
#    #TLine 讀取時間軸欄 row[4] # Lyrics_1.txt沒有時間軸
#        #檢查格式
#        
#    #OriPKey 原各字幕的primary key row[5]
#
#    '''

    #print('# ' + str(EachSrt) + '\n')
#with open('S:/ENV/test.csv','r',encoding = 'utf-8-sig') as fin: 
#    # `with` statement available in 2.5+
#    # csv.DictReader uses first line in file for column headings by default
#    dr = csv.DictReader(fin) # comma is default delimiter
#    to_db = [(i['filename'], i['word'], i['tag'], i['phonetic'], i['translation'], i['definition']) for i in dr]
    
    #寫入SQLite3一列 #cur.executemany("INSERT INTO t (Word,ZhLine,EnLine,From,TLine,OriPKey,PKey) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
    return

#%%#開撸
#連接資料庫
con = sqlite3.connect("S:/ENV/_MM/dict/zhdict.db") # First, establish a connection to the the SQLite database by creating a Connection object.
cur = con.cursor() #Next, create a Cursor object using the cursor method of the Connection object.
FNList = None
#沒有第一欄就建立第一欄
#con.execute("create table if not exists t(id integer primary key autoincrement, KWord varchar(128), ZhLine varchar(128),EnLine,From,TLine,OriPKey,PKey)")

#讀取所有字幕檔名

AllSrts = []
AllSrts = os.listdir(WDir)

#讀取SQLite中所有檔名欄（去除重複）
#cur = self.__con.cursor()
FNList = cur.execute("SELECT Episode from t_zh") #type__<class 'sqlite3.Cursor'>
#該行轉成能閱讀的形式
#record = ''.join(str(cur.fetchone())) # fetchone type__<class 'str'>
FNList = cur.fetchall() # fetchall type__<class 'list'> #取得list

if str(FNList) != '[]': #避免Episode沒有任何資料的時候噴錯
    FNList =list(map(list,(zip(*FNList)))).pop(0)

#FNList = re.sub(r'\(|\)|\[|\]', '', ''.join(str(FNList)))
#FNList = [str(x) for x in FNList.split(',')] # 轉回list
#print('__' + str(FNList)) # [('Fringe.S02E06.HDTV.XviD-P0W4.简体&英文.srt',), ('Fringe.S02E07.HDTV.XviD-P0W4.简体&英文.srt',)]
#sys.exit("#FNList的type__" + str(type(FNList)))


#從所有字幕中，取出一個檔案
for EachSrt in AllSrts:
    count_files += 1 
    #如果檔名跟資料庫中的檔名欄重複    
    #print('# ' + str(EachSrt))   #[BBC：生命].BBC.Life.10.Primates.2009.BluRay.720p.x264.DD51.AAC.TriAudio-MySiLU.简体&英文.srt
    #print('# ' + str(FNList[0])) #('[BBC：生命].BBC.Life.01.Challenges.Of.Life.2009.BluRay.720p.x264.DD51.AAC.TriAudio-MySiLU.简体&英文.srt',)
    if EachSrt in FNList:        
        #print(EachSrt + '已存在')
        continue    

    EachST(EachSrt)
    count_files_new += 1 
    
    if (count_files_new/10).is_integer() is True:
        print('新完成檔案/全部檔案__' + str(count_files_new) + '/' + str(count_files))  
        #break

#    #print("Press 'D' to exit...") # 這樣如果想中斷的話，會在一個檔案整個完成後，才從這裡斷出，不但失敗，還無窮迴圈 /*BUG*/
#    while True:
#        if ord(msvcrt.getch()) in [68, 100]:
#            break

con.close()
print("#---------------\n# 新完成檔案/全部檔案：" + str(count_files_new) + '/' + str(count_files) + ' 個\n#---------------\n')        
winsound.Beep(1750, 100) # 37-12000 - 簡書 - https://goo.gl/a7e1Hs
time.sleep(0.5)
winsound.Beep(1750, 100)
time.sleep(0.5)