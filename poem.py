import requests
import json
import re
from time import sleep
import sys
url = 'http://so.gushiwen.org/view_'
class crawler:
    __slots__=("original_url",'data','all')
    def __init__(self,original_url):
        self.original_url = original_url
        self.data = []
    def get_all_web(self):
        for i in range(30001,35001,1):
            tmp = requests.get(self.original_url+str(i)+'.aspx')
            poem=re.search('id=\"txtare'+str(i)+'\">'+'([\u4e00-\u9fa5|，。；？]+)',tmp.text)
            specific = re.search('\">([\u4e00-\u9fa5]+)</a><span>：</span><a href=\".+\">([\u4e00-\u9fa5]+).*</a> </p>',tmp.text)#regex for dynasty and poem
            all = {}
            try :
                all['poem'] = poem.group(1)
            except AttributeError:
                continue
            all['poem'] = poem.group(1)
            all['author'] = specific.group(2)
            all['dynasty'] = specific.group(1)
            self.data.append(all)
            print(str(i),"has already")
    def getjson(self):
        with open('D:\\poemdata1.json','a') as f:
            f.write(json.dumps(self.data,sort_keys=True,indent=4,ensure_ascii=False))

def main():
    sakura = crawler(url)
    sakura.get_all_web();
    sakura.getjson();

if __name__ == '__main__':
    main()
