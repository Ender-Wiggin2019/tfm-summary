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

st.set_page_config(page_title= '殖民火星数据',page_icon='🔥', initial_sidebar_state='auto',)

# @st.experimental_singleton
# def get_db_sessionmaker():
#     ana = sqlite3.connect('./game_analysis.db', check_same_thread=False)
#     return ana

# con = get_db_sessionmaker()
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")