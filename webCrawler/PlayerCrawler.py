#!/usr/bin/env python
#created by Baird

import requests
from bs4 import BeautifulSoup

url_list = [
    'https://www.wanplus.com/lol/event?t=3&year=2014&page=1',
    'https://www.wanplus.com/lol/event?t=3&year=2014&page=2',
    'https://www.wanplus.com/lol/event?t=3&year=2014&page=3',
    'https://www.wanplus.com/lol/event?t=3&year=2015&page=1',
    'https://www.wanplus.com/lol/event?t=3&year=2015&page=2',
    'https://www.wanplus.com/lol/event?t=3&year=2015&page=3',
    'https://www.wanplus.com/lol/event?t=3&year=2016&page=1',
    'https://www.wanplus.com/lol/event?t=3&year=2016&page=2',
    'https://www.wanplus.com/lol/event?t=3&year=2017&page=1',
    'https://www.wanplus.com/lol/event?t=3&year=2017&page=2',
    'https://www.wanplus.com/lol/event?t=3&year=2017&page=3',
    'https://www.wanplus.com/lol/event?t=3&year=2017&page=4',
    'https://www.wanplus.com/lol/event?t=3&year=2018'
]


target_urls = []                        #赛事url
titles_id = []                          #赛事名对应ID
data = [('名次','选手','战队','位置','出场次数','KDA','参团率','场均击杀','单场最高击杀','场均死亡','单场最高死亡','场均助攻','单场最高助攻',
         'GPM','CSPM','每分钟输出','输出占比','每分钟承受伤害','承受伤害占比','每分钟插眼数','每分钟排眼数')]

for target in url_list:
    res = requests.get(url=target)
    soup = BeautifulSoup(res.text,'lxml')
    div = soup.select('.event-list')[0]
    tags_a = div.select('a')
    for tag_a in tags_a:
        href = tag_a.attrs['href']
        if 'html' in href:
            temp = href.split('.')[0]
            titile_id = temp.rsplit('/')[2]
            # print(titile_id)
            titles_id.append(titile_id)
            url = 'https://www.wanplus.com/lol' + temp + '/player'
            target_urls.append(url)

for i in range(len(target_urls)):
    data.append(titles_id[i])
    target_url = target_urls[i]
# for target_url in target_urls:
#     print(target_url)
    count = 0
    temp = []
    res = requests.get(url=target_url)
    soup = BeautifulSoup(res.text, 'lxml')
    tds = soup.select('td')

    for td in tds:
        if count == 21:
            data.append(temp)
            count = 0
            temp = []
        temp.append(td.text)
        count += 1

with open('output/player.txt','w',encoding='utf-8') as f:
    for item in data:
        f.write(str(item)+'\n')

