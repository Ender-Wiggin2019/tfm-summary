import streamlit as st
import numpy as np
import hashlib
# import hydralit_components as hc
import datetime
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import altair as alt
import base64
st.set_page_config(page_title= '殖民火星数据',page_icon='🔥', initial_sidebar_state='auto',)

f = open('./count.txt')
count = f.read()
f.close()
f = open('./count.txt', 'w')
add = str(int(count)+1)
f.write(add)
f.close()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

@st.cache
def get_corp_trans():
    return pd.read_csv('./corp_list.csv')
corp_trans = get_corp_trans()
# @st.cache(allow_output_mutation=True)
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file)
#     page_bg_img = '''
#     <style>
#     body {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
    
#     st.markdown(page_bg_img, unsafe_allow_html=True)
#     return

# set_png_as_page_bg('./assets/background.png')
# page_bg_img = '''
# <style>
# body {
# background-image: url("https://images.app.goo.gl/vzFv1SKxTNdW83gm8");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

# # specify the menu definition we'll stick in the sidebar
# side_menu_data = [
#     {'icon': "far fa-copy", 'label':"Left End",'ttip':"I'm the Left End tooltip!"}, #can specify an icon from the bootstrap icon library
#     {'icon': "far fa-copy", 'label':"Copy"},
#     {'label':"Chart"}, # the minimum we can specify for a menu item
#     {'id':'special return value here','icon': "far fa-address-book", 'label':"Book"}, #can provide a special id to return when clicked
#     {'icon': "far fa-calendar-alt", 'label':"Calendar"}, #or can let the label be the return value when clicked
#     {'icon':"🐙",'label':"Component",'ttip':"I'm the Component tooltip!"}, # can als use an emoji as the icon
#     {'icon': "fas fa-tachometer-alt", 'label':"Dashboard"},
#     {'label':"Da55shboard"}, # or no icon
#     {'icon':'🤵','label':"Right End"},
# ]

# # specify the primary menu definition
# menu_data = [
#     {'icon': "far fa-copy", 'label':"Left End"},
#     {'id':'Copy','icon':"🐙",'label':"Copy"},
#     {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
#     {'icon': "far fa-address-book", 'label':"Book"},
#     {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
#     {'icon': "far fa-clone", 'label':"Component"},
#     {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
#     {'icon': "far fa-copy", 'label':"Right End"},
# ]

# # we can override any part of the primary colors of the menu
# #over_theme = {'txc_inactive': '#FFFFFF','menu_background':'red','txc_active':'yellow','option_active':'blue'}
# over_theme = {'txc_inactive': '#FFFFFF'}
# menu_id = hc.nav_bar(menu_definition=menu_data,home_name='Home',override_theme=over_theme)

# with st.sidebar:
#     side_menu_id = hc.nav_bar(menu_definition=side_menu_data,key='sidetbar',login_name='Login',override_theme=over_theme,first_select=6)

# #get the id of the menu item clicked
# st.info(f"{menu_id=}")
# st.info(f"{side_menu_id=}")

# def _max_width_(prcnt_width:int = 75):
#     max_width_str = f"max-width: {prcnt_width}%;"
#     st.markdown(f""" 
#                 <style> 
#                 .reportview-container .main .block-container{{{max_width_str}}}
#                 </style>    
#                 """, 
#                 unsafe_allow_html=True,
#     )
# _max_width_()
ori = pd.read_csv('preprocess.csv')
ori['createtime'] = pd.to_datetime(ori['createtime'])

page = st.sidebar.selectbox("选择类别", ['公司数据', '用户数据', '卡牌数据', '成就榜', '网站介绍'], index=1)
playerNum = st.sidebar.selectbox("选择玩家人数", ['2P', '4P'], index=1)

if playerNum == '2P':
    playerNum = 2
    player_ori = ori[ori['players'] == 2]
elif playerNum == '4P':
    playerNum = 4
    player_ori = ori[ori['players'] == 4]

delete_list = {'界限突破': 'breakthrough', '阿瑞斯扩': 'aresExtension', '群友扩': 'erosCardsOption', '双公司': 'doubleCorp', '探路者扩': 'pathfindersExpansion', '月球扩': 'moonExpansion'}
with st.sidebar.expander("选择游戏设置"):
    for i in delete_list.values():
        exec("%s = st.radio('%s', ('全选', '开启', '禁用'))"%(i,list(delete_list.keys())[list(delete_list.values()).index(i)]))

for option in delete_list.values():
    if vars()[option] == '全选':
        continue
    elif vars()[option] == '开启':
        player_ori = player_ori[player_ori[option] == True]
    elif vars()[option] == '禁用':
        player_ori = player_ori[(player_ori[option] == False) | (pd.isna(player_ori[option]) == True)]


# df8.plot(x="createtime", y="generations")
# st.dataframe(player_group)
@st.cache
def getPlayerNumCorpResult(df, player_num = 4):
    def expandDoubleCorp(df):
        pd.options.mode.chained_assignment = None
        df1 = df[df['doubleCorp'] == True]
        df2 = df[df['doubleCorp'] == True]
        df2['corporation'] = df2['corporation2']
        res = pd.concat([df1, df2],axis=0, ignore_index=True)
        res['count'] = 0.5
        return res
    df = df.loc[df['players'] == player_num].reset_index(drop=True)
    for i in range(1, player_num+1):
        player_idx = 'player'+str(i)
        player_df_pre = df[player_idx].apply(lambda x:eval(x))
        # print(player_idx)
        player_df = pd.json_normalize(player_df_pre).reset_index(drop=True)
        if i == 1:
            res = pd.concat([df,player_df.reindex(df.index)],axis=1)
            print((res.loc[pd.isna(res['player']) == False]).shape[0])
        else:
            mid = pd.concat([df,player_df.reindex(df.index)],axis=1)
            res = pd.concat([res, mid],axis=0, ignore_index=True)
            # print((mid.loc[pd.isna(mid['player']) == False]).shape[0])
        # df = pd.concat([df, pd.json_normalize(df[player_idx])],axis=1)
    res.drop(['player'+str(i) for i in range(1, 7)], axis=1, inplace=True)
    res['count'] = 1
    res_single = res[~(res['doubleCorp'] == True)]
    res_double = expandDoubleCorp(res)
    res_final = pd.concat([res_single, res_double],axis=0, ignore_index=True)
    res_final = res_final.merge(corp_trans, how='left', on='corporation', suffixes=['','_drop'])
    return res_final
corp_df = getPlayerNumCorpResult(player_ori, playerNum)
corp_df_group = corp_df.groupby(['cn', 'corporation']).agg(
    position = ('position', 'mean'),
    playerScore = ('playerScore', 'mean'),
    generations = ('generations', 'mean'),
    total = ('count', 'sum')
).dropna().sort_values('position').reset_index()

if page == '公司数据':

    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    icon("search")
    corp_key = st.text_input("")
    button_clicked = st.button("OK")
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;vertical-align: baseline;} </style>', unsafe_allow_html=True)
    # st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    player_group = player_ori.groupby([pd.Grouper(key='createtime', freq='2W-SUN')])['generations'] \
        .mean() \
        .sort_index()
        # .reset_index() \
    player_gen_avg = round(player_ori['generations'].mean(),1)
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
    # game_options = st.multiselect("game options", delete_list.values())

    corp = (corp_trans['corporation']).to_list()
    if corp_key == '': corp_df_group = corp_df_group
    else: corp_df_group = corp_df_group[(corp_df_group['corporation'].str.contains('(?i)'+corp_key)) | (corp_df_group['cn'].str.contains('(?i)'+corp_key))]
    corp_df_group.columns = ['公司中文', '公司英文', '位次', '得分', '时代', '打出次数']
    corp_df_group = corp_df_group.set_index('公司中文')
    img_mode = st.checkbox('开启图片模式(手机上请不要选择)', value = False)
    if img_mode == False:
        st.dataframe(corp_df_group.style.format({'位次': '{:.1f}', '得分': '{:.1f}', '时代': '{:.1f}', '打出次数': '{:.0f}'}))
    else:
        # select_corp = st.selectbox('choose corporation', corp)
        last_label = 0
        if playerNum == 2: tier_setter = [1.2, 1.4, 1.6, 1.8]
        else: tier_setter = [1.5, 2, 2.5, 3] 
        for i, v in corp_df_group.iterrows():
            if last_label == 0 and v.位次 <= tier_setter[0]:
                st.markdown('**第0梯队**')
            elif last_label <= tier_setter[0] and v.位次 > tier_setter[0]:
                st.markdown('**第1梯队**')
            elif last_label <= tier_setter[1] and v.位次 > tier_setter[1]:
                st.markdown('**第2梯队**')
            elif last_label <= tier_setter[2] and v.位次 > tier_setter[3]:
                st.markdown('**第3梯队**')
            elif last_label <= tier_setter[3] and v.位次 > tier_setter[3]:
                st.markdown('**第4梯队**')

            last_label = v.位次
            c1,c2,c3,c4,c5 = st.columns([1,5,1,1,2])
            corporation = v['公司英文']
            try: image = Image.open('./test/' + corporation + '.png')
            except:
                img = Image.open('./assets/' + 'nofound' + '.png')
                image = img.resize((50,62))
            c1.image(image)
            # c2.markdown('**%s**'%(corporation))
            # c2.markdown('**%s**'%(corporation))
            c2.info('%s'%(corporation))
            if v.位次 <= 2:
                c3.success('**%.2f**'%(round(v.位次,2)))
            elif v.位次 <= 3:
                c3.warning('**%.2f**'%(round(v.位次,2)))
            if v.位次 > 3:
                c3.error('**%.2f**'%(round(v.位次,2)))
            #     with c3:
            #         hc.info_card(title=str(v.位次), content='', sentiment='good',bar_value=v.位次/4)
            # c4.markdown('**%.1f**'%(v.total))
            c4.info('%.d'%(v.打出次数))
            breakdown_df = corp_df[corp_df['corporation']==corporation]
            breakdown_df_group = breakdown_df.groupby('position').agg(
                total = ('count', 'sum')
            ).sort_values('position').reset_index()
            # c4.bar_chart(breakdown_df_group)
            # fig = breakdown_df_group.plot(kind='bar', figsize=(4, 3), dpi=50)
            # fig, ax = plt.subplots(figsize=(2, 2))
            # ax.plot(breakdown_df_group['position'], breakdown_df_group['total'])
            fig = plt.figure(figsize = (2, 0.9))
            plt.bar(breakdown_df_group['position'], breakdown_df_group['total'], width=0.5, color='salmon')
            # plt.yticks(np.arange(1, 4, 1))
            c5.pyplot(fig)

elif page == '用户数据':
    name = st.text_input('请输入用户名')
    pwd = st.text_input('请输入密码')
    user_data = pd.read_csv('./用户数据.csv')
    user_pwd = pd.read_csv('./users_db.csv')
    verify = user_data[(user_data['is_id']==1) & (user_data['user_name'].str.lower()==name.lower())]
    if 'permission' not in st.session_state:
        st.session_state.permission = False
    if 'admin' not in st.session_state:
        st.session_state.admin = False
    if name != '' and verify.shape[0] != 1:
        st.error('用户名无法匹配')
        st.session_state.permission = False
    elif name == 'admin' and pwd == 'ender':  st.session_state.admin = True
    elif name != '' and verify.shape[0] == 1:
        md5_pwd = hashlib.md5(pwd.encode())
        if user_pwd.loc[user_pwd['name'].str.lower() == name.lower(),'password'].values == md5_pwd.hexdigest():
            st.success('登陆成功！')
            st.session_state.permission = True
        elif pwd != '':
            st.error('密码错误')
            st.session_state.permission = False
    st.text('小提示：手机玩家在网页左上角可以展开选项设置')
    if st.session_state.admin == True: st.session_state.permission = True
    if st.session_state.permission == True:
        name_df = user_data[user_data['user_name'].str.lower()==name.lower()]['name'].to_list()
        names = st.multiselect('常用游戏名称：', name_df, default=name_df)

        # @st.cache
        def getPlayersCard(name_list):
            df = pd.read_csv('./playersCardRank.csv')
            res = df.loc[df['player'].isin(name_list)]
            res_group = res \
            .groupby(['cn', 'name']) \
            .agg(
                position = ('sum_position', 'sum'),
                playerScore = ('sum_playerScore', 'sum'),
                generations = ('sum_generations', 'sum'),
                total = ('total', 'sum')
            ) \
            .dropna()
            res_group['position'] = res_group['position'] / res_group['total']
            res_group['playerScore'] = res_group['playerScore'] / res_group['total']
            res_group['generations'] = res_group['generations'] / res_group['total']
            res_group = res_group.sort_values(['total', 'position'], ascending=[False, True]).reset_index()
            res_group.columns = ['卡牌中文', '卡牌英文', '位次', '得分', '时代', '打出次数']

            return res_group.drop('卡牌英文', axis=1).head(20).round(2)
        # @st.cache
        def getPlayerNumPlayerResult(df, name_list, player_num = 4):
            """
            主键: game_id, player
            """
            # df = df.loc[(df['players'] == player_num) & (df['player'].isin(name_list))].reset_index(drop=True)
            df = df.loc[(df['players'] == player_num)].reset_index(drop=True)
            for i in range(1, player_num+1):
                player_idx = 'player'+str(i)
                # print(df[player_idx].head())
                # player_df_pre = df[player_idx].apply(lambda x:eval(x))
                # print(player_idx)
                # player_df = pd.json_normalize(player_df_pre).reset_index(drop=True)
                player_df = pd.json_normalize(df[player_idx].apply(lambda x:eval(x))).reset_index(drop=True)
                if i == 1:
                    res = pd.concat([df,player_df.reindex(df.index)],axis=1)
                else:
                    mid = pd.concat([df,player_df.reindex(df.index)],axis=1)
                    res = pd.concat([res, mid],axis=0, ignore_index=True)
                    # print((mid.loc[pd.isna(mid['player']) == False]).shape[0])
                # df = pd.concat([df, pd.json_normalize(df[player_idx])],axis=1)
            res.drop(['player'+str(i) for i in range(1, 7)], axis=1, inplace=True)
            res['count'] = 1
            res = res[res['player'].isin(name_list)].reset_index(drop=True)
            
            print(res.columns)
            return res

        player_df = getPlayerNumPlayerResult(player_ori, names, playerNum)
        player_df_group = player_df.groupby('count').agg(
            平均顺位 = ('position', 'mean'),
            平均分数 = ('playerScore', 'mean'),
            平均时代 = ('generations', 'mean'),
            总数 = ('count', 'sum')
        ).dropna().sort_values('平均顺位').reset_index(drop=True)

        # TODO 时间序列，全局和按天数聚合的结果
        player_df['小时'] = (pd.to_datetime(player_df['createtime'])).dt.hour
        player_time = player_df.groupby(player_df.小时).agg(
        局数 = ('count', 'sum')
        ).dropna().sort_index()
        st.markdown('### 对局统计')

        st.table((player_df_group.assign(用户名=name) \
                .set_index('用户名')) \
                .style.format({'平均顺位': '{:.2f}', '平均分数': '{:.3f}', '平均时代': '{:.3f}'}))

        playersCardRank = getPlayersCard(names)
        with st.expander('你最喜欢的卡牌'):
            
            st.table(playersCardRank.style.format({'位次': '{:.2f}', '得分': '{:.2f}', '时代': '{:.2f}'}))

        # 根据玩家的game_id join, 取位次高于该玩家的用户，按名称聚合
        @st.cache
        def getPlayersPlayWith(df, name_list, player_num = 4):
            """
            主键: game_id, player
            """
            # df = df.loc[(df['players'] == player_num) & (df['player'].isin(name_list))].reset_index(drop=True)
            df = df.loc[(df['players'] == player_num)].reset_index(drop=True)
            for i in range(1, player_num+1):
                player_idx = 'player'+str(i)
                # print(df[player_idx].head())
                # player_df_pre = df[player_idx].apply(lambda x:eval(x))
                # print(player_idx)
                # player_df = pd.json_normalize(player_df_pre).reset_index(drop=True)
                player_df = pd.json_normalize(df[player_idx].apply(lambda x:eval(x))).reset_index(drop=True)
                if i == 1:
                    res = pd.concat([df,player_df.reindex(df.index)],axis=1)
                else:
                    mid = pd.concat([df,player_df.reindex(df.index)],axis=1)
                    res = pd.concat([res, mid],axis=0, ignore_index=True)
                    # print((mid.loc[pd.isna(mid['player']) == False]).shape[0])
                # df = pd.concat([df, pd.json_normalize(df[player_idx])],axis=1)
            res.drop(['player'+str(i) for i in range(1, 7)], axis=1, inplace=True)
            res['count'] = 1
            
            res_player = res[res['player'].isin(name_list)].reset_index(drop=True)
            res_other = res[~(res['player'].isin(name_list))].reset_index(drop=True)
            res_final = res_other.merge(res_player, on='game_id', how='inner', suffixes=['', '_drop'], indicator=True).query('position.notna()', engine="python")
            res_final.loc[res_final['position'] > res_final['position_drop'],'win'] = 1
            res_final.loc[res_final['position'] <= res_final['position_drop'],'win'] = 0
            res_final_group = res_final.groupby('player').agg(
            总共遇到次数 = ('win', 'count'),
            被你击败 = ('win', 'sum')
            ).dropna().sort_values('总共遇到次数', ascending=False)
            res_final_group['被你击败'] = res_final_group['被你击败'].astype(int)
            return res_final_group

        with st.expander('你最喜欢的公司'):
            try:
                fav_corps = corp_df.loc[corp_df['player'].isin(names)]
                fav_corps_group = fav_corps.groupby(['cn']).agg(
                    平均顺位 = ('position', 'mean'),
                    平均分数 = ('playerScore', 'mean'),
                    平均时代 = ('generations', 'mean'),
                    总数 = ('count', 'count')
                ).dropna().sort_values('总数', ascending=False).head(15)
                st.table(fav_corps_group.style.format({'平均顺位': '{:.1f}', '平均分数': '{:.2f}', '平均时代': '{:.1f}', '总数': '{:.0f}'}))
            except: st.warning('该选项组合没有数据')
        with st.expander('和你游戏的玩家'):
            try:
                player_with_you = getPlayersPlayWith(player_ori, names, playerNum)
                st.table(player_with_you.head(15))
            except: st.warning('该选项组合没有数据')
        with st.expander('活跃时间'):
            st.bar_chart(player_time)

        challenge = pd.read_csv('./成就.csv')
        all_challenge = (pd.unique(challenge['title'])).shape[0]
        challenge = challenge.loc[challenge['player'].isin(names)].sort_values('index')
        challenge.drop_duplicates(subset=['title'], keep='first', inplace=True)
        challenge = challenge.loc[:,['title', 'reason', 'createtime']].set_index('title')
        challenge.columns = ['成就', '达成时间']
        your_challenge = challenge.shape[0]
        with st.expander('火星成就 (%d/%d)'%(your_challenge, all_challenge)):
            if challenge.shape[0] == 0:
                challenge = challenge.append({'成就': '达成成就数量 (%d/%d)'%(your_challenge, all_challenge), '达成时间': '直到此刻'}, ignore_index=True)
                challenge.rename(index={0:'火星打工人'},inplace=True)
            st.table(challenge)
            
elif page == '卡牌数据':
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    icon("search")
    card_key = st.text_input("")
    card_clicked = st.button("OK")
    allCardsRank = pd.read_csv('./allCardsRank.csv')
    if playerNum == 2:
        allCardsRank = allCardsRank.loc[allCardsRank['players'] == 2].drop('players', axis=1)
    elif playerNum == 4:
        allCardsRank = allCardsRank.loc[allCardsRank['players'] == 4].drop('players', axis=1)
    allCardsRank.columns = ['卡牌中文', '卡牌英文', '位次', '得分', '时代', '打出次数']
    if card_key == '': allCardsRank = allCardsRank
    else: allCardsRank = allCardsRank[(allCardsRank['卡牌英文'].str.contains('(?i)'+card_key)) | (allCardsRank['卡牌中文'].str.contains('(?i)'+card_key))]
    st.dataframe(allCardsRank.style.format({'位次': '{:.2f}', '得分': '{:.1f}', '时代': '{:.1f}', '打出次数': '{:.0f}'}))
    
    st.markdown('注：卡牌的数据统计根据打出该卡牌的玩家最终位次和得分计算')
    st.markdown('目前卡牌数据只支持选择2p/4p，不支持游戏扩展筛选。')

elif page == '网站介绍':
    st.markdown("""
    ## 数据来源
    本网站数据来自[殖民火星国服](http://jaing.me/)的后台数据库，有超过14000局游戏的记录，本数据站主要针对2P和4P进行统计。
    
    ## FAQ
    
    * **Q: 登陆账号是哪个账号?**
    
        A: 火星游戏网站的注册账号。
    
    * **Q: 我的常用游戏名和登陆账号不符怎么办?**
    
        A: 联系*QQ: 209926937*, 将个人常用id发给我即可。
    
    * **Q: 我想看更多的数据, 或者有优化界面的建议, 如何提出呢?**
    
        A: 联系上方的QQ号就行了捏。
        
    ## 当前点击量
    目前已被访问%s次。
    """%(add)
    )
elif page == '成就榜':
    all_challenge = pd.read_csv('./成就.csv').query('index == 0')
    total_num = pd.read_csv('./成就.csv').groupby('title').agg(max).reset_index()
    all_players = pd.read_csv('./用户数据.csv').shape[0]
    all_challenge.drop_duplicates('title', keep='first', inplace=True)
    all_challenge = all_challenge.merge(total_num, on='title', how='left', suffixes=['', '_drop'])
    all_challenge['rate'] = all_challenge['index_drop'] / all_players
    all_challenge = all_challenge.loc[:,['title', 'reason', 'rate', 'player']].set_index('title').sort_values('rate')
    all_challenge.columns = ['成就', '稀有度', '最佳获得者']
    st.table(all_challenge.style.format({'稀有度': '{:,.2%}'}))
    
    pass