#for asycio
from threading import Thread
import asyncio
import requests
import json
import re
from time import sleep
import sys
import time
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

new_loop4 = asyncio.new_event_loop()
t4 = Thread(target=start_loop,args=(new_loop4,))
url = 'http://so.gushiwen.org/view_'
data = []
now = lambda : time.time()
def getjson(d):#d is a dictionary
    with open('D:\\poems1.json','a') as f:
        f.write(json.dumps(d,sort_keys=True,indent=4,ensure_ascii=False))
        f.write(',')
def write_web(loops):
    for i in range(70001,73281,1):
        com_url = url+str(i)+'.aspx'
        choose = i%3
        if choose == 0:
            loops[0].call_soon_threadsafe(get_all_web,com_url,i)
        elif choose == 1:
            loops[1].call_soon_threadsafe(get_all_web,com_url,i)
        elif choose == 2:
            loops[2].call_soon_threadsafe(get_all_web,com_url,i)

def get_all_web(url,i):
    tmp = requests.get(url)
    name = re.search('margin-bottom:10px;">([\u4e00-\u9fa5|，。；？、·…（）/《》“”‘’| ｝｛]+)</h1>',tmp.text)
    poem=re.search('id=\"txtare'+str(i)+'\">'+'([\u4e00-\u9fa5|，。；？、]+)',tmp.text)
    specific = re.search('\">([\u4e00-\u9fa5]+)</a><span>：</span><a href=\".+\">([\u4e00-\u9fa5]+).*</a> </p>',tmp.text)#regex for dynasty and poem
    all = {}
    try :
        all['poem'] = poem.group(1)
        all['name'] = name.group(1)
        all['poem'] = poem.group(1)
        all['author'] = specific.group(2)
        all['dynasty'] = specific.group(1)
    except AttributeError:
        return
    new_loop4.call_soon_threadsafe(getjson,all)
    print(str(i),"has already")


def main():
    t4.start()
    new_loop1 = asyncio.new_event_loop()
    new_loop2 = asyncio.new_event_loop()
    new_loop3 = asyncio.new_event_loop()
    all_loops =[new_loop1,new_loop2,new_loop3]
    t1 = Thread(target=start_loop,args=(new_loop1,))
    t2 = Thread(target=start_loop,args=(new_loop2,))
    t3 = Thread(target=start_loop,args=(new_loop3,))
    t1.start()#get url
    t2.start()#get url
    t3.start()#get_url
    write_web(all_loops)

if __name__ == '__main__':
    main()
