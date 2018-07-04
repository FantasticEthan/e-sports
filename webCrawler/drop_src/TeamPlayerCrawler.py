# -*- coding:utf-8 -*- ＃
import sys
import requests
import re
import json
from requests.exceptions import RequestException

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'gameType=2; wanplus_token=99741ab201410ab6ecdb281a7b5dd663; wanplus_storage=lf4m67eka3o; wanplus_sid=582f6a3bb9f54d26823669a8ea21764e; wanplus_csrf=_csrf_tk_812504310; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1494295646; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1494296667',
    'Host':'www.wanplus.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

f = open('season_Dictonary.txt', 'r')
season_dict=json.loads(f.read())
url_team = 'http://www.wanplus.com/lol/event/'
url_player = 'http://www.wanplus.com/lol/event/'
def get_one_page(url):
    try:
        response = requests.get(url,headers =  headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_team(html):
    pattern = re.compile(
        '<tr>.*?<td>(.*?)</td>.*?text-hid">(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>'
        +'.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>'
         +'.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?</tr>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield  {
            '名次':item[0],
            '战队 ':item[1],
            'KDA':item[2],
            '场均击杀':item[3],
            '场均死亡':item[4],
            '每分钟伤害':item[5],
            '一血率': item[6],
            '场均时长': item[7],
            '场均经济': item[8],
            '每分钟经济': item[9],
            '每分钟补刀': item[10],
            '场均小龙': item[11],
            '小龙控制率': item[12],
            '场均大龙': item[13],
            '大龙控制率': item[14],
            '每分钟插眼': item[15],
            '每分钟排眼': item[16],
            '排眼效率': item[17],
            '场均推塔数': item[18],
            '场均被推塔数': item[19],
        }

def parse_player(html):
    pattern = re.compile(
        '<tr>.*?<td>(.*?)</td>.*?text-hid">(.*?)</td>.*?text-hid">(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>'
        +'.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?;">(.*?)</td>'
         +'.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?;">(.*?)</td>.*?</tr>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield  {
            '名次':item[0],
            '选手 ':item[1],
            '战队':item[2],
            '位置':item[3],
            '出场次数':item[4],
            'KDA':item[5],
            '参团率': item[6],
            '场均击杀': item[7],
            '单场最高击杀': item[8],
            '场均死亡': item[9],
            '单场最高死亡': item[10],
            '场均助攻': item[11],
            '单场最高助攻': item[12],
            'GPM': item[13],
            'CSPM': item[14],
            '每分钟输出': item[15],
            '输出占比': item[16],
            '每分钟承受伤害': item[17],
            '承受伤害占比': item[18],
            '每分钟插眼数': item[19],
            '每分钟排眼数': item[20],
        }

def write_to_file1(season_name,content):
    with open('output/'+season_name+'team.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def write_to_file2(season_name,content):
    with open('output/'+season_name+'player.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def main():
    for season_name,id in season_dict.items():
        print('season name is {}'.format(season_name))
        url_team_full = url_team+id+'/team'
        player_team_full = url_player+id+'/player'
        team = get_one_page(url_team_full)
        if team:
            print('采集战队页成功...')
        for i in parse_team(team):
            # print(i)
            write_to_file1(season_name,i)
        player = get_one_page(player_team_full)
        if player:
            print('采集选手页成功...')
        for j in parse_player(player):
            # print(j)
            write_to_file2(season_name,j)

if __name__ ==  '__main__':
    main()