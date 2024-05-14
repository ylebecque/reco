import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


#######  Import des données ########
@st.cache_data
def load_df():
    df_big = pd.read_csv("/Users/yann/jupyter/Projet 2/movies list def.csv", sep=",")
    df_affiche = pd.read_csv(
        "/Users/yann/jupyter/Projet 2/movies list def.csv", sep=","
    )
    df_big = df_big.merge(
        df_affiche[["tconst", "poster_path"]], on="tconst", how="left"
    )
    df_films = df_big.drop_duplicates(subset=["tconst"])
    return df_big, df_affiche, df_films


df_big, df_affiche, df_films = load_df()


#######  Configuration de la page ########

st.image("https://www.creuseconfluence.com/images/creuse-confluence.png")
st.title("Flashback sur les plus beaux succès 🍿")

st.markdown("# FILMS ET PAYS DE PRODUCTION 🎬")
st.markdown("## 🌍 Les pays producteurs des meilleurs films ")

with st.sidebar:
    st.title("Options")
    st.markdown("Sélectionnez les options ci-dessous :")
    x = st.slider(
        "🌍 Nombre de films pour le top",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        key="slider_x_p",
    )
    y = st.slider(
        "Nombre de résultat pour le top",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
        key="slider_y_p",
    )
    d = st.slider(
        "Décennie",
        min_value=1900,
        max_value=2020,
        value=2020,
        step=10,
        key="slider_d_p",
    )


dec = df_films[(df_films["Décennie"] == d)]
dec_top = dec.sort_values(by="numVotes", ascending=False).head(x)
pc_counts = dec_top["production_countries"].value_counts()
top_pc = pc_counts.head(y)


plt.figure(figsize=(10, 6))
plt_barh_pc = plt.barh(top_pc.index, top_pc, color="powderblue")
plt.bar_label(plt_barh_pc, label_type="edge", fontsize=10, color="black")
plt.xlabel("Nombre de films")
plt.ylabel("Pays de production")
plt.title(
    f"TOP {y} des Pays de production des {x} meilleurs films de la décennie : {d}"
)
plt.gca().invert_yaxis()
st.pyplot(plt)


### Les meilleurs films de production française
st.markdown("## 🥐 Les meilleurs films de production française ")


dec = df_films[(df_films["Décennie"] == d)]
dec_top = dec.sort_values(by="numVotes", ascending=False)

top_films_fr = dec_top[
    (dec_top["production_countries"] == "['FR']")
    & (dec_top["original_language"] == "fr")
].head(y)

plt.figure(figsize=(10, 6))
bars_fr = plt.barh(
    top_films_fr["Titre vo"], top_films_fr["numVotes"], color="powderblue"
)
for bar, label in zip(bars_fr, top_films_fr["averageRating"]):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f"{label:.2f}",
        ha="left",
        va="center",
        fontsize=10,
        color="black",
    )
plt.xlabel("Note vote")
plt.ylabel("Film (filtre par 'Note_vote')")
plt.title(f"TOP {y} des films de production française de la décennie : {d}")
plt.gca().invert_yaxis()
st.pyplot(plt)

col1, col2, col3 = st.columns(3)

# Afficher les affiches des trois premiers films
path = "https://image.tmdb.org/t/p/original"
affiches = top_films_fr["poster_path_y"].head(3).tolist()

with col1:
    st.image(
        path + affiches[0], width=150, caption=top_films_fr.iloc[0]["primaryTitle"]
    )

with col2:
    st.image(
        path + affiches[1], width=150, caption=top_films_fr.iloc[1]["primaryTitle"]
    )

with col3:
    st.image(
        path + affiches[2], width=150, caption=top_films_fr.iloc[2]["primaryTitle"]
    )


### Les films de production française les mieux notés
st.markdown("## 🥐 Les films de production française les mieux notés")


dec = df_films[(df_films["Décennie"] == d)]
dec_top = dec.sort_values(by="averageRating", ascending=False)

top_films_fr_2 = dec_top[
    (dec_top["production_countries"] == "['FR']")
    & (dec_top["original_language"] == "fr")
].head(y)


plt.figure(figsize=(10, 6))
bars_fr = plt.barh(
    top_films_fr_2["Titre vo"], top_films_fr_2["averageRating"], color="powderblue"
)
for bar, label in zip(bars_fr, top_films_fr_2["averageRating"]):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f"{label:.2f}",
        ha="left",
        va="center",
        fontsize=10,
        color="black",
    )
plt.xlabel("Nombre de vu / vote)")
plt.ylabel("Film")
plt.title(
    f"TOP {y} des films de production française les mieux notés de la décennie : {d}"
)
plt.gca().invert_yaxis()
st.pyplot(plt)

col1, col2, col3 = st.columns(3)

# Afficher les affiches des trois premiers films
path = "https://image.tmdb.org/t/p/original"
affiches_2 = top_films_fr_2["poster_path_y"].head(3).tolist()

with col1:
    st.image(
        path + str(affiches_2[0]),
        width=150,
        caption=top_films_fr_2.iloc[0]["primaryTitle"],
    )

with col2:
    st.image(
        path + str(affiches_2[1]),
        width=150,
        caption=top_films_fr_2.iloc[1]["primaryTitle"],
    )

with col3:
    st.image(
        path + str(affiches_2[2]),
        width=150,
        caption=top_films_fr_2.iloc[2]["primaryTitle"],
    )
