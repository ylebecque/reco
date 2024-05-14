import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


########################################################
############## Configuration de la page   ##############
########################################################

st.set_page_config(
    page_title="Comparaison par genre",
    layout="centered",
    initial_sidebar_state="auto",
)

st.image("https://www.creuseconfluence.com/images/creuse-confluence.png")
st.title("🎥 Comparatif par genre")

# st.markdown("Analyse par genre")
st.sidebar.markdown("Analyse par genre")


########################################################
############## Chargement de la base      ##############
########################################################
# @st.cache_data
def load_df():
    return pd.read_csv("/Users/yann/jupyter/Projet 2/movies list def.csv")


# df_list bien chargée sur la page d'accueil ?
if "df_list" in st.session_state:
    df_list = st.session_state["df_list"]
else:
    df_list = load_df()

########################################################
############## Ajout des widgets :        ##############
##############    slider pour le choix de la période ###
##############    menus déroulants pour les genres #####
##############    menu déroulant pour le pays ##########
########################################################

annees = st.sidebar.slider("Période : ", 1940, 2022, (1970, 2020))


# liste_genres = set()
# for list_genres in list(df_list[("genres")].unique()):
#    genres = list_genres.split(",")
#    for genre in genres:
#        liste_genres.add(genre)
# liste_genres = list(liste_genres)
# liste_genres.sort()

liste_genres = [
    "Action",
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "News",
    "Reality-TV",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Talk-Show",
    "Thriller",
    "War",
    "Western",
]


genre_1 = st.sidebar.selectbox("Premier  genre : ", liste_genres)
genre_2 = st.sidebar.selectbox("Deuxième genre : ", liste_genres)

liste_pays = ["US", "FR", "GB", "IT", "ES"]
dico_langues = {"US": "en", "FR": "fr", "GB": "en", "IT": "it", "ES": "es"}


pays = st.sidebar.selectbox("Pays : ", liste_pays)

annee_min, annee_max = annees

df1 = df_list[
    (df_list["Année"] >= annee_min)
    & (df_list["Année"] <= annee_max)
    & (df_list["genres"].str.contains(genre_1))
    & (df_list["production_countries"].str.contains(pays))
    & (df_list["original_language"] == dico_langues[pays])
].sort_values(by="Année", ascending=True)

df2 = df_list[
    (df_list["Année"] >= annee_min)
    & (df_list["Année"] <= annee_max)
    & (df_list["genres"].str.contains(genre_2))
    & (df_list["production_countries"].str.contains(pays))
    & (df_list["original_language"] == dico_langues[pays])
].sort_values(by="Année", ascending=True)

########################################################
############## Tracé du graphique ######################
########################################################

fig, ax = plt.subplots(figsize=(10, 5))


########################################################
############## Graphe de comparaison ###################
########################################################

ax.set_title(
    f"Evolution de la note moyenne des films selon le genre pour les productions {pays}"
)
ax.set_xlabel("Années")
ax.set_ylabel("Note moyenne")
ax.plot(
    df1.groupby("Année")["averageRating"].mean(),
    color="royalblue",
    label=genre_1,
)
ax.plot(df2.groupby("Année")["averageRating"].mean(), color="red", label=genre_2)
ax.legend()


col1, col2 = st.columns([0.8, 0.2])

with col1:
    st.pyplot(fig)


########################################################
############## Import d'un poster aléatoire ############
############## dont la note appartient    ##############
############## au dernier décile          ##############
########################################################

note_ref = df1["note_ponderee"].quantile(0.9)

path = "https://image.tmdb.org/t/p/original"
img_url = df1[
    (df1["poster_path"].notnull())
    & (  # film disposant d'une affiche
        df1["note_ponderee"] >= note_ref
    )  # et dont la note est "bonne"
].sample()["poster_path"]
url = list(path + img_url)[0]

with col2:
    st.image(url, use_column_width=True)
