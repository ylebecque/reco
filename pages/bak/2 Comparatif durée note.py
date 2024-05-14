import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


########################################################
############## Configuration de la page   ##############
########################################################

st.set_page_config(
    page_title="Comparatif durée/genre",
    layout="centered",
    initial_sidebar_state="auto",
)
st.image("https://www.creuseconfluence.com/images/creuse-confluence.png")
st.title("🕓 Comparatif durée / note")


########################################################
############## Chargement de la base      ##############
########################################################
@st.cache_data
def load_df():
    return pd.read_csv("movies list def.csv")


# df_list bien chargée sur la page d'accueil ?
if "df_list" in st.session_state:
    df_list = st.session_state["df_list"]
else:
    df_list = load_df()


# suppression des outliers liés aux documentaires
df_list = df_list[df_list["Durée"] < 180]


########################################################
############## Ajout des widgets :        ##############
##############    slider pour le choix de la période ###
##############    menus déroulants pour les genres #####
##############    menu déroulant pour le pays ##########
########################################################

annees = st.sidebar.slider("Période : ", 1940, 2022, (1970, 2020))

annee_min, annee_max = annees

########################################################
############## Evolution de la durée /note   ###########
########################################################

df = df_list[
    (df_list["Année"] >= annee_min) & (df_list["Année"] <= annee_max)
].sort_values(by="Année", ascending=True)

# fig, ax = plt.subplots(2, 1, figsize = (12,12))
fig, ax1 = plt.subplots(figsize=(12, 4))

ax1.set_title("Evolution de la durée et de la note moyenne des films selon les années")
ax1.set_xlabel("Années")
ax1.set_ylabel("Durée moyenne (minutes)")
ax1.plot(df.groupby("Année")["Durée"].mean(), color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.set_xlabel("Années")
ax2.set_ylabel("Note moyenne")
ax2.plot(
    df.groupby("Année")["averageRating"].mean(),
    color="tab:red",
)
ax2.tick_params(axis="y", labelcolor="tab:red")

st.pyplot(fig)
