#bilibili crawler sakura
import requests
import json
import re
from time import sleep
import xlwt
import io
import sys
postfix="?page=1&page_size=20&version=0&is_finish=0&start_year=2017&tag_id=&index_type=1&index_sort=0&quarter=0"
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
class crawler:
    total = 0;
    __slots__=("name","original_url","data")
    def __init__(self,name,original_url):
        self.name = name
        self.original_url = original_url
        self.data = []
    def get_bilibili_page(self,i):
        tmp_postfix = postfix[:6]+str(i)+postfix[7:]
        final = self.original_url + tmp_postfix
        tmp = requests.post(final)
        for anime in tmp.json()['result']['list']:
            self.data.append(anime)
            print(str(i),' has appended!')
    def get_more_about_anime(self):#I will use re to check the num of bilibili, the amount of play ,fans
        for anime in self.data:
            deep = anime['url']
            deeper = requests.get(deep)
            sl = re.findall('<em>(\d+[\.]*\d*)[万]?</em>',deeper.text)
            print(anime['url'],'has gotten more specific data!')
            print(sl)
            if(len(sl)==3):
                if(float(sl[2]) >1000):
                    sll = float(sl[2])/10000
                else:
                    sll = float(sl[2])
            else:sll = 0
            anime['bilibili'] = str(sll)
            if(len(sl)==1):
                anime['fans'] ='0'
            elif(len(sl)>=2): anime['fans'] = sl[1]
            anime['amount_play'] = sl[0]
            #sleep(1)
    def play(self):
        r = requests.post(self.original_url+postfix)
        total = r.json()['result']['count']
        m = int(int(total)/20) + 1
        for i in range(1,m+1):
            self.get_bilibili_page(i)
            sleep(1)
        self.get_more_about_anime()

    def WriteExcel(self):
        file = xlwt.Workbook()
        table = file.add_sheet('database',cell_overwrite_ok = True)
        table.write(0,1,'番剧名称')
        table.write(0,3,'追番人数（万）')
        table.write(0,2,'总播放量（万）')
        table.write(0,4,'弹幕数量（万）')
        i = 1
        for a in self.data:
            table.write(i,1,a['title'])
            table.write(i,3,a['fans'])
            table.write(i,2,a['amount_play'])
            table.write(i,4,a['bilibili'])
            i +=1
            print(' has been writen!')
        file.save("D:\\2017anime_data.xls")

def main():
    Kugimiya = crawler('Holo','https://bangumi.bilibili.com/web_api/season/index_global')
    Kugimiya.play()
    Kugimiya.WriteExcel()

if __name__ == '__main__':
    main()
