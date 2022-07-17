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
import sqlite3
# import plotly.graph_objs as go
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title= '殖民火星数据',page_icon='🔥', initial_sidebar_state='auto',)

@st.experimental_singleton
def get_db_sessionmaker(db_name):
    ana = sqlite3.connect(db_name, check_same_thread=False)
    return ana

con = get_db_sessionmaker('./game.db')
ana = get_db_sessionmaker('./game_analysis.db')


# @st.experimental_singleton
# def get_db_sessionmaker():
#     ana = sqlite3.connect('./game_analysis.db', check_same_thread=False)
#     return ana

# con = get_db_sessionmaker()
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

name = st.text_input('请输入用户名')
pwd = st.text_input('请输入密码', type='password')
bu = st.button('Log In')

if bu:
    verify = pd.read_sql_query("select password from users where lower(name) = '{pwd}' limit 1".format(pwd=pwd), con=con)
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
        if verify.iloc[0,0] == md5_pwd.hexdigest():
            st.success('登陆成功！')
            st.session_state.permission = True
            st.session_state.user = name
            
        elif pwd != '':
            st.error('密码错误')
            st.session_state.permission = False
        
        