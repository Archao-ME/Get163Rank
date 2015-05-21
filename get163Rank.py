#coding = utf-8
import urllib2
import urllib
import thread
import re
import HTMLParser
import json

class Get163Rank:

    def GetHtml(self):
        
        url  = 'http://music.163.com/api/play/record?uid='+self.id+'&type=1'
        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        cookies = {
            'appver':'2.0.2'
        }
        headers = { 'User-Agent' : userAgent,'Referer':'http://music.163.com'}

        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie','appver = 2.0.2'))
        opener.addheaders.append(('Referer','Http://music.163.com'))
        opener.addheaders.append(('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'))

        try :
            self.json1 = opener.open(url).read()

        except urllib2.URLError,e:
            return e.code   

        return self.json1
    def WeekDic(self):
        json1 = self.json1
        jsonx = json.loads(json1)
        songList = {}
        for x in  jsonx["weekData"] :
            songList[x["song"]["name"]] = x["score"]
        songList = sorted(songList.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)
        songJson = json.dumps(songList,encoding="UTF-8",ensure_ascii=False)
        self.songJson = songJson
        return songJson
    
    def __init__(self,id):
        self.id = id   
        self.songJson = {}


