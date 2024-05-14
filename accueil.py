import streamlit as st
import pandas as pd


# Chargement de la base
# @st.cache_data
def load_df():
    return pd.read_csv("movies list def 2.csv")


def bar():
    pass
def foo():
    pass


# df_list bien chargée sur la page d'accueil ?
if "df_list" in st.session_state:
    df_list = st.session_state["df_list"]
else:
    df_list = load_df()
    st.session_state["df_list"] = df_list

st.set_page_config(
    page_title="Analyse et recommandation de films",
    layout="centered",
    initial_sidebar_state="auto",
)
st.image("https://www.creuseconfluence.com/images/creuse-confluence.png")


st.title("PROJET :")
st.header("Analyse et recommandation de films")
st.subheader("À l'aide des bases IMDB/TMDB")
