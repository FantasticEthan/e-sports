#!/usr/bin/env python
#created by Baird

import requests
from bs4 import BeautifulSoup
import re
import json


season_file = open('season_Dictonary.txt', 'r')
season_dict=json.loads(season_file.read())

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
data = [('名次','战队','KDA','场均击杀','场均死亡','每分钟伤害','一血率','场均时长','场均经济',
         '每分钟经济','每分钟补刀','场均小龙','小龙控制率','场均大龙','大龙控制率','每分钟插眼',
         '每分钟排眼','排眼效率','场均推塔数','场均被推塔数','year','Season')]

for target in url_list:
    year = re.search(r'(\d{4})',target).group(0)
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
            url = 'https://www.wanplus.com/lol' + temp + '/team'
            target_urls.append((year,url))

for i in range(len(target_urls)):
    # data.append(titles_id[i])
    target_url = target_urls[i]
# for target_url in target_urls:
#     print(target_url)
    count = 0
    temp = []
    res = requests.get(url=target_url[1])
    soup = BeautifulSoup(res.text, 'lxml')
    tds = soup.select('td')

    for td in tds:
        if count == 20:
            temp.append(target_url[0])
            temp.append(season_dict[titles_id[i]])
            data.append(temp)
            count = 0
            temp = []
        temp.append(td.text)
        count += 1

with open('output/team.txt','w',encoding='utf-8') as f:
    for item in data:
        f.write(str(item)+'\n')

