import streamlit as st
import pandas as pd

import plotly.graph_objs as go
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import sqlite3
import os
from PIL import Image

st.set_page_config(page_title= '殖民火星数据',page_icon='🔥', initial_sidebar_state='auto', layout="wide")

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

@st.experimental_singleton
def get_db_sessionmaker():
    ana = sqlite3.connect('./game_analysis.db', check_same_thread=False)
    return ana

con = get_db_sessionmaker()

# con = get_db_sessionmaker()
if 'permission' not in st.session_state or st.session_state.permission == False:
    st.warning('Please log in first!')
else:
    user = st.session_state.user
    user = st.text_input('user name:')
    sql = """
    select
        players,
        avg(rank)          as rank,
        avg(playerScore)   as score,
        avg(generations)   as generations,
        count(corporation) as total_games
    from ods_game_results
    where lower(player) in (select distinct lower(name)
                    from ods_user_alias
                    where lower(user_name) = '{}')
    group by players
    order by players, total_games desc
    ;
    """.format(user)
    df = pd.read_sql(sql, con=con).round(2)
    df.columns = ['人数', '排名', '分数', '时代', '总数']
    st.table(df.style.format({'排名': '{:.1f}', '时代': '{:.1f}', '分数': '{:.1f}'}))
    
    
    
    player_num = st.slider('选择玩家人数', 2, 5, value=4)
    sql2 = """
        select
        corporation,
        corporation2,
        playerScore,
        players,
        generations,
        position,
        rank,
        date(createtime) as date
    from ods_game_results
    where lower(player) in (select distinct lower(name)
                    from ods_user_alias
                    where lower(user_name) = '{}'
                    and players = {})

    ;
    """.format(user, player_num)
    
    df2 = pd.read_sql(sql2, con=con)
    df2['CORP_PATH'] = str(os.getcwd()) + '/assets/' + df2['corporation'] + '.png'
    # df2['CORP_PATH'] = str(os.getcwd()) + '/assets/' + 'Chaos' + '.png'
    
    image_nation = JsCode("""function (params) {
        var element = document.createElement("span");
        var imageElement = document.createElement("img");
    
        if (params.data.CORP_PATH) {
            imageElement.src = params.data.CORP_PATH;
            imageElement.width="20";
        } else {
            imageElement.src = "";
        }
        element.appendChild(imageElement);
        element.appendChild(document.createTextNode(params.value));
        return element;
        }""")
    
    # df2.columns = ['用户名', '人数', '排名', '时代', '分数', '总数']
    code_df_build = GridOptionsBuilder.from_dataframe(df2)
    code_df_build.configure_selection('single')
    code_df_build.configure_pagination()
    code_df_build.configure_column('corporation', cellRenderer=image_nation)
    # ori_df_build.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
    ori_df_builder = code_df_build.build()
    AgGrid(
        df2, 
        width='100%',
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        fit_columns_on_grid_load=True,
        gridOptions=ori_df_builder,
        theme='streamlit'
        )