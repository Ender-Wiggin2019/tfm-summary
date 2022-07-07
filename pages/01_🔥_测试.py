import streamlit as st
import pandas as pd


import sqlite3


@st.experimental_singleton
def get_db_sessionmaker():
    ana = sqlite3.connect('./game_analysis.db', check_same_thread=False)
    return ana

con = get_db_sessionmaker()

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")
# con = get_db_sessionmaker()

sql = """
select player,
       players,
               avg(rank)                           as rank,
        avg(playerScore)                    as score,
        avg(generations)                    as generations,
        count(corporation)                  as total_games
from ods_game_results
group by player, players
having players in (4)
-- and (card_name like '%Border Che%' or card_name like '%Fencing%' or card_name like '%Antigravity Experiment%' or card_name like '%Hay Maker%' or card_name like '%Venus Uni%'
--     or card_name like '%Fleet Re%' or card_name like '%Smuggling%')
order by players, total_games desc
;
"""
df = pd.read_sql(sql, con=con)
st.dataframe(df)