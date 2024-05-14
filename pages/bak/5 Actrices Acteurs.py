import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


#######  Import des données ########
@st.cache_data
def load_df():
    df_big = pd.read_csv("/Users/yann/jupyter/Projet 2/movies def.csv", sep=",")
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
st.title("FLASHBACK SUR LE CINEMA ! 🍿")

st.markdown("# 🔎 ZOOM SUR : Actrices Acteurs")
st.markdown("## Le nombre de films et le type de films ")

with st.sidebar:
    st.title("Options")
    st.markdown("Sélectionnez les options ci-dessous :")
    y_z = st.slider(
        "Nombre d'acteurs pour le top",
        min_value=5,
        max_value=20,
        value=10,
        step=1,
        key="slider_y_z",
    )
    d_z = st.slider(
        "Décennie",
        min_value=1900,
        max_value=2020,
        value=2020,
        step=10,
        key="slider_d_z",
    )


dec = df_big[df_big["Décennie"] == d_z]
dec["genres"] = dec["genres"].str.split(",").str[0]

# Triez les acteurs par Note_vote en ordre décroissant
dec_top = dec[
    (dec["Fonction"] == "actress") | (dec["Fonction"] == "actor")
].sort_values(by="Note_vote", ascending=False)

# Créez la table pivot
pivot_table = dec_top.pivot_table(
    index="Nom", columns="genres", values="tconst", aggfunc="count", fill_value=0
)
pivot_table["Nombre de films"] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values(["Nombre de films"], ascending=False)
top = pivot_table.head(y_z)
del top["Nombre de films"]

# Créez le graphique en barres empilées
top.plot(kind="bar", stacked=True, figsize=(10, 6), cmap="tab20")

plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
plt.xlabel("Acteurs")
plt.ylabel("Nombre de films")
plt.title(
    f"Répartition des genres de films : Top {y_z} acteurs les plus prolifiques de la décennie {d_z}"
)

st.pyplot(plt)
