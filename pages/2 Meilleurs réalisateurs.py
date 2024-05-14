import streamlit as st
import pandas as pd


########################################################
############## Configuration de la page   ##############
########################################################

st.set_page_config(
    page_title="Top 3 des meilleurs réalisateurs par genre",
    layout="centered",
    initial_sidebar_state="auto",
)
st.image("https://www.creuseconfluence.com/images/creuse-confluence.png")
st.title("🎬 Top 3 des meilleurs réalisateurs par genre")


# st.markdown("Meilleurs réals")
st.sidebar.markdown("Meilleurs réals")


########################################################
############## Chargement de la base      ##############
########################################################
@st.cache_data
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


genre = st.sidebar.selectbox("Premier  genre : ", liste_genres)

liste_pays = ["US", "FR", "GB", "IT", "ES"]
dico_langues = {"US": "en", "FR": "fr", "GB": "en", "IT": "it", "ES": "es"}
# liste_pays.sort()

pays = st.sidebar.selectbox("Pays : ", liste_pays)

annee_min, annee_max = annees

df = df_list[
    (df_list["Année"] >= annee_min)
    & (df_list["Année"] <= annee_max)
    & (df_list["genres"].str.contains(genre))
    & (df_list["production_countries"].str.contains(pays))
    & (df_list["original_language"] == dico_langues[pays])
].sort_values(by="Année", ascending=True)

# Ajout du nom 'Inconnu' quand le réal n'est pas renseigné
# Afin de pouvoir appliquer la conversion :
# top_real["real"] = top_real["real"].apply(lambda x: eval(x)[0])
# Lors de la création des colonnes

df.fillna("['Inconnu']", inplace=True)


########################################################
############## Création des colonnes        ############
########################################################

col1, col2 = st.columns([0.5, 0.5])

# On définit la limite des films à prendre en compte
# En fonction de la période explorée
limit = (annee_max - annee_min) * 5

top_films = df.sort_values(by="note_ponderee", ascending=False)[:limit].copy()

top_real = top_films[["real", "Titre vo", "note_ponderee"]]

# On ne retient que le premier nom en cas de réalisateurs multiples
try:
    top_real["real"] = top_real["real"].apply(lambda x: eval(x)[0])
except:
    pass

# On écarte les films dont le réalisateur n'est pas indiqué
top_real = top_real[top_real["real"] != "Inconnu"]

# On regroupe les réalisateurs par nom
# On leur associe la liste de leurs films
# Ainsi que la somme des notes pondérées obtenues
top_real = (
    top_real.groupby("real")
    .agg({"Titre vo": lambda x: list(x), "note_ponderee": "sum"})
    .reset_index()
)

# On calcule le nombre de films par réalisateur
top_real["Nombre"] = top_real["Titre vo"].apply(lambda x: len(x))

# On calcule un score égale à :
# note_pondérée * nombre_films
top_real["score"] = top_real["note_ponderee"] * top_real["Nombre"]

# On trie les réalisateurs par score décroissant
top_real.sort_values("score", ascending=False, inplace=True)


########################################################
############## Affichage des réals          ############
########################################################
with col1:
    medailles = ["🥇", "🥈", "🥉"]
    for top in range(3):
        try:
            st.subheader(medailles[top] + top_real["real"].iloc[top])
            # st.write(f"Score : {top_real['score'].iloc[top]}")
            films_list = top_real["Titre vo"].iloc[top]
            for film in films_list[:3]:
                st.write(film)
        except:
            pass

########################################################
############## Import du poster           ##############
############## du film n°1                ##############
########################################################

try:
    for idx in range(3):
        top_nom = top_real["real"].iloc[idx]
        top_titre = top_real["Titre vo"].iloc[idx][0]
        img_url = df_list[
            (df_list["Titre vo"] == top_titre) & (df_list["real"].str.contains(top_nom))
        ]["poster_path"]
        path = "https://image.tmdb.org/t/p/original"
        url = list(path + img_url)[0]

        with col2:
            st.image(url, width=150)
except:
    pass
