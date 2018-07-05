# -*- coding:utf-8 -*- ＃
# author：Ethan

import pandas as pd
import json

with open('output/team.txt','r') as f:
    i = 0
    for line in f.readlines():
        line = line.replace('\n','')
        if i==0:
            line = line.strip('()').replace("'",'').replace(' ','').split(',')
            df = pd.DataFrame(columns=line)
            # print(len(df.columns))
        else:
            line = line.strip('[]').replace("'",'').split(',')
            df.loc[i-1] = line
        i+=1
    print("line num is {}".format(i))
    df.to_csv("team.csv",index=False)


