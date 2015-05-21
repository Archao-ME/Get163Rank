#coding = utf-8
import urllib2
import urllib
import HTMLParser
import json
from models import SongList
import datetime 

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
            songList[x["song"]["id"]] = {"name":x["song"]["name"],"score":x["score"]}
            #songList[x["song"]["id"]]["name"]   = x["song"]["name"]
        songList = sorted(songList.items(),key =lambda x:x[1]["score"],reverse=True)
        songJson = json.dumps(songList,encoding="UTF-8",ensure_ascii=False)
        self.songJson = songJson
        #print songJson
        return songJson
    def SaveWeek(self):
        jsonx =json.loads(self.songJson)
        #jsonx = json.dumps(jsonx,encoding="UTF-8",ensure_ascii=False)
        ISOFORMAT='%Y%m%d'
        today = datetime.date.today().strftime(ISOFORMAT)
        queryList=[]
        for x in jsonx :
            song_Name = json.dumps(x[1]["name"],encoding="UTF-8",ensure_ascii=False)[1:-1]
            song_ID = x[0]
            SongList.objects.filter(user_ID=self.id,date=today,song_ID=song_ID).delete()
            SongModel = SongList(song_ID = song_ID,song_Name = song_Name ,score = x[1]["score"],user_ID = self.id,date=today)
            queryList.append(SongModel)
            #state = SongModel.save()
            print x[0]
        SongList.objects.bulk_create(queryList)
        return '200'
    def __init__(self,id):
        self.id = id   
        self.songJson = {}



