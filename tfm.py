import pandas as pd
import numpy as np
from config import Config as cfg
import pgOperation
import matplotlib.pyplot as plt
import streamlit as st
ori = pd.read_csv('preprocess.csv')
ori['createtime'] = pd.to_datetime(ori['createtime'])
def getPlayerNumResult(df, player_num = 4):
    df = df.loc[df['players'] == player_num].reset_index(drop=True)
    for i in range(1, player_num+1):
        player_idx = 'player'+str(i)
        # print(player_idx)
        player_df = pd.json_normalize(df[player_idx]).reset_index(drop=True)
        if i == 1:
            res = pd.concat([df,player_df.reindex(df.index)],axis=1)
            print((res.loc[pd.isna(res['player']) == False]).shape[0])
        else:
            mid = pd.concat([df,player_df.reindex(df.index)],axis=1)
            res = pd.concat([res, mid],axis=0, ignore_index=True)
            print((mid.loc[pd.isna(mid['player']) == False]).shape[0])
        # df = pd.concat([df, pd.json_normalize(df[player_idx])],axis=1)

    res.drop(['player'+str(i) for i in range(1, 7)], axis=1, inplace=True)
    return res
playerNum = st.radio("select player number", ['2P', '4P'])

if playerNum == '2P':
    player_ori = ori[ori['players'] == 2]
elif playerNum == '4P':
    player_ori = ori[ori['players'] == 4]


delete_list = {'breakthrough': 'breakthrough', 'ares': 'aresExtension', 'eros': 'erosCardsOption', 'double corporations': 'doubleCorp', 'pf': 'pathfindersExpansion'}
game_options = st.multiselect("game options", delete_list.values())
for option in game_options:
    if delete_list.get(option) != None:
        player_ori = player_ori[player_ori[delete_list.get(option)] == True]

player_group = player_ori.groupby([pd.Grouper(key='createtime', freq='2W-SUN')])['generations'] \
    .mean() \
    .sort_index()
    # .reset_index() \

# df8.plot(x="createtime", y="generations")
st.line_chart(player_group)
# st.dataframe(player_group)