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

st.markdown("# Les Top Films 🎈")

with st.sidebar:
    st.title("Options")
    st.markdown("Sélectionnez les options ci-dessous :")
    y = st.slider(
        "Nombre de films dans le TOP", min_value=5, max_value=20, value=10, step=1
    )
    d = st.slider("Décennie", min_value=1900, max_value=2020, value=2020, step=10)

# Filtrer les données en fonction de la décennie
df_top = (
    df_films[df_films["Décennie"] == d]
    .sort_values(by="Note_vote", ascending=False)
    .head(y)
)

# Générer le graphique
plt.figure(figsize=(10, 6))
bars = plt.barh(df_top["primaryTitle"], df_top["Note_vote"], color="powderblue")
for bar, label in zip(bars, df_top["averageRating"]):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f"{label:.2f}",
        ha="left",
        va="center",
        fontsize=10,
        color="black",
    )
plt.xlabel("Note_vote")
plt.ylabel("Titre original du film")
plt.title(f"TOP {y} de la décennie {d}")
plt.gca().invert_yaxis()

# Afficher le graphique dans Streamlit
st.pyplot(plt)

# Afficher les affiches des trois premiers films
col1, col2, col3 = st.columns(3)

# Afficher les affiches des trois premiers films
path = "https://image.tmdb.org/t/p/original"
affiches = df_top["poster_path_y"].head(3).tolist()

with col1:
    st.image(path + affiches[0], width=150, caption=df_top.iloc[0]["primaryTitle"])

with col2:
    st.image(path + affiches[1], width=150, caption=df_top.iloc[1]["primaryTitle"])

with col3:
    st.image(path + affiches[2], width=150, caption=df_top.iloc[2]["primaryTitle"])


st.markdown("# Partagent-ils des caractéristiques communes ? 🧐")


#######  GENRES ########

st.markdown("## Genres ? ")

# Widgets
x = st.slider(
    "Combien de films souhaitez vous sélectionner : ",
    min_value=10,
    max_value=1000,
    value=100,
    step=10,
)

dec = df_films[(df_films["Décennie"] == d)]
dec_top = dec.sort_values(by="Note_vote", ascending=False).head(x)
genre_counts = dec_top["genres"].value_counts()
top_genres = genre_counts.head(y)

plt.figure(figsize=(10, 6))
plt_barh_genre = plt.barh(top_genres.index, top_genres, color="powderblue")
plt.bar_label(plt_barh_genre, label_type="edge", fontsize=10, color="black")
plt.xlabel("Nombre de films")
plt.ylabel("Genre")
plt.title(f"TOP {y} des genres des {x} meilleurs films de la décennie : {d}")
plt.gca().invert_yaxis()
st.pyplot(plt)


#######  ACTEURS ########

st.markdown("## Actrices / Acteurs ? ")

# Widgets
x_a = st.slider(
    "Combien de films souhaitez vous sélectionner : ",
    min_value=5,
    max_value=100,
    value=10,
    step=10,
)
y_a = st.slider(
    "Combien d'acteurs souhaitez vous sélectionner : ",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
)

# Dans toutes les lignes je filtre sur la décennie
dec = df_big[(df_big["Décennie"] == d)]
# Je trie la décennie par Note_vote en DESC
dec_top = dec.sort_values(by="Note_vote", ascending=False)
# Je veux prendre toutes les lignes qui correspondent aux {x} premiers films
top_tconst = dec_top["tconst"].unique()[:x_a]
# Dans ce top 5 films je veux prendre les lignes où la colonne "Fonction" est "actress" ou "actor"
actrice_acteur = dec_top[
    dec_top["tconst"].isin(top_tconst)
    & ((dec_top["Fonction"] == "actress") | (dec_top["Fonction"] == "actor"))
]
# Je compte le nombre de fois que le "Nom" apparaît pour le top acteurs {y}
actrice_acteur_count = actrice_acteur["Nom"].value_counts().head(y_a)

plt.figure(figsize=(10, 6))
plt_barh_a = plt.barh(
    actrice_acteur_count.index, actrice_acteur_count.values, color="powderblue"
)
plt.bar_label(plt_barh_a, label_type="edge", fontsize=10, color="black")
plt.xlabel("Nombre de films")
plt.ylabel("Actrices/Acteurs")
plt.title(
    f"TOP {y_a} des Actrices / Acteurs des {x_a} meilleurs films de la décennie : {d}"
)
plt.gca().invert_yaxis()
st.pyplot(plt)


#######  REALISATEURS ########
st.markdown("## Réalisatrices / Réalisateurs ? ")

# Widgets
x_r = st.slider(
    "Combien de films souhaitez vous sélectionner : ",
    min_value=10,
    max_value=100,
    value=50,
    step=10,
    key="slider_x_r",
)
y_r = st.slider(
    "Combien de réalisateurs souhaitez vous sélectionner : ",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
    key="slider_y_r",
)

dec = df_big[(df_big["Décennie"] == d)]
dec_top = dec.sort_values(by="Note_vote", ascending=False)

top_tconst = dec_top["tconst"].unique()[:x_r]

real = dec_top[dec_top["tconst"].isin(top_tconst) & (dec_top["Fonction"] == "director")]
real_count = real["Nom"].value_counts().head(y_r)

plt.figure(figsize=(10, 6))
plt_barh_a = plt.barh(real_count.index, real_count.values, color="powderblue")
plt.bar_label(plt_barh_a, label_type="edge", fontsize=10, color="black")
plt.xlabel("Nombre de films")
plt.ylabel("Réalisatrices / Réalisateurs")
plt.title(
    f"TOP {y_r} des Réalisatrices / Réalisateurs des {x_r} meilleurs films de la décennie : {d}"
)
plt.gca().invert_yaxis()
st.pyplot(plt)
