import pandas as pd
# from config import Config as cfg
# import pgOperation
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
playerNum = st.radio("选择玩家人数", ['2P', '4P'])

if playerNum == '2P':
    player_ori = ori[ori['players'] == 2]
elif playerNum == '4P':
    player_ori = ori[ori['players'] == 4]


# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;vertical-align: baseline;} </style>', unsafe_allow_html=True)
# st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
delete_list = {'界限突破': 'breakthrough', '阿瑞斯扩': 'aresExtension', '群友扩': 'erosCardsOption', '双公司': 'doubleCorp', '探路者扩': 'pathfindersExpansion'}
# game_options = st.multiselect("game options", delete_list.values())
for i in delete_list.values():
    exec("%s = st.radio('%s', ('全选', '开启', '禁用'))"%(i,list(delete_list.keys())[list(delete_list.values()).index(i)]))

for option in delete_list.values():
    if vars()[option] == '全选':
        continue
    elif vars()[option] == '开启':
        player_ori = player_ori[player_ori[option] == True]
    elif vars()[option] == '禁用':
        player_ori = player_ori[(player_ori[option] == False) | (pd.isna(player_ori[option]) == True)]
player_group = player_ori.groupby([pd.Grouper(key='createtime', freq='2W-SUN')])['generations'] \
    .mean() \
    .sort_index()
    # .reset_index() \
player_gen_avg = round(player_ori['generations'].mean(),1)

# df8.plot(x="createtime", y="generations")
row1_1, row1_2 = st.columns((5,1))
row1_1.line_chart(player_group)
if 'last_gen_num' not in st.session_state:
    row1_2.metric(label="统计数量", value=player_ori.shape[0])
    st.session_state.last_gen_num = player_ori.shape[0]
else:
    row1_2.metric(label="统计数量", value=player_ori.shape[0], delta=str(round((100*(player_ori.shape[0]-st.session_state.last_gen_num)/st.session_state.last_gen_num),2))+'%')
    st.session_state.last_gen_num = player_ori.shape[0]

if 'last_gen_avg' not in st.session_state:
    row1_2.metric(label="平均时代", value=player_gen_avg)
    st.session_state.last_gen_avg = player_gen_avg
else:
    row1_2.metric(label="平均时代", value=player_gen_avg, delta=str(round((100*(player_gen_avg-st.session_state.last_gen_avg)/st.session_state.last_gen_avg),2))+'%')
    st.session_state.last_gen_avg = player_gen_avg
# st.dataframe(player_group)