import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib
import difflib

########################################################
############## Configuration de la page   ##############
########################################################

st.set_page_config(
    page_title="Recommandation",
    layout="centered",
    initial_sidebar_state="auto",
)

st.image("https://www.creuseconfluence.com/images/creuse-confluence.png")
st.title("🔎 Recherche et recommandation")


########################################################
############## Chargement de la base      ##############
########################################################
# @st.cache_data
def load_df():
    return pd.read_csv("movies list def 2.csv")


# df_list bien chargée sur la page d'accueil ?
if "df_list" in st.session_state:
    df_list = st.session_state["df_list"]
else:
    df_list = load_df()
    st.session_state["df_list"] = df_list


########################################################
############## Création du modèle IA      ##############
############## et de la fonction de       ##############
############## recommandation             ##############
########################################################


# @st.cache_data
def model_reco_0():
    df_ia = df_list[["tconst", "Titre vo", "description"]]
    tfidf = TfidfVectorizer(max_df=0.8, min_df=50, stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df_ia.description)
    modelKNN = NearestNeighbors(n_neighbors=50)
    modelKNN.fit(tfidf_matrix)
    return modelKNN, tfidf_matrix


def model_reco():
    modelKNN = joblib.load("./pages/model.pkl")
    tfidf_matrix = joblib.load("./pages/tfidf.pkl")
    return modelKNN, tfidf_matrix


def recommandation(index, tfidf_matrix, genre, filtre_note):
    reco = modelKNN.kneighbors(tfidf_matrix.getrow(index), return_distance=True)
    df_reco = df_list.iloc[reco[1][0]]
    # Supression du titre servant d'index
    df_reco = df_reco[1:]
    df_reco = df_reco[(df_reco["genres"].str.contains(genre)) | (genre == "-")]
    # Tri par ordre décroissant de note si filtre_note = True
    if filtre_note:
        df_reco.sort_values(by="note_ponderee", ascending=False, inplace=True)
    return df_reco.head(15)


# modelKNN bien chargé ?
if ("modelKNN" in st.session_state) and ("tfidf_matrix" in st.session_state):
    modelKNN = st.session_state["modelKNN"]
    tfidf_matrix = st.session_state["tfidf_matrix"]
else:
    modelKNN, tfidf_matrix = model_reco()
    st.session_state["modelKNN"] = modelKNN
    st.session_state["tfidf_matrix"] = tfidf_matrix

# Sélection du film de référence par l'utilisateur
if "genre" in st.session_state:
    genre = st.session_state["genre"]
else:
    genre = "-"

liste_genres = [
    "-",
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

if "titre" in st.session_state:
    titre = st.session_state["titre"]
else:
    titre = "Star Wars"

with st.sidebar:
    # Choix du filtrage sur la note
    filtre_note = st.toggle("Meilleures notes", value=True)

    # Sélection du genre
    genre = st.sidebar.selectbox("Genre recherché : ", liste_genres)

    # Sélection du titre
    titre = st.text_input("Titre du film recherché : ", titre).title()

    # Y a-t-il des films dont le titre est exactement celui-là ?
    selections_films_exact = df_list[
        (df_list["Titre vo"].apply(lambda x: x.title()) == titre)
        & ((df_list["genres"].str.contains(genre)) | (genre == "-"))
    ]

    # Recherche des films dont le titre contient celui qui est donné
    # On utilise la méthode title() pour uniformiser les titres US/FR
    selections_films_contient = df_list[
        (df_list["Titre vo"].apply(lambda x: x.title()).str.contains(titre))
        & ((df_list["genres"].str.contains(genre)) | (genre == "-"))
    ].sort_values(by="note_ponderee", ascending=False)

    # Si aucun film trouvé, on cherche plus largement
    if len(selections_films_contient) < 10:
        possibilities = list(df_list["Titre vo"])
        close_matches = difflib.get_close_matches(titre, possibilities, 9, 0.5)
        # st.write(close_matches)
        selections_films_proposes = (
            df_list[
                (df_list["Titre vo"].isin(close_matches))
                & ((df_list["genres"].str.contains(genre)) | (genre == "-"))
            ]
            .sort_values(by="note_ponderee", ascending=False)
            .head(10 - len(selections_films_contient))
        )
    else:
        selections_films_proposes = pd.DataFrame()

    selections_films = pd.concat(
        [selections_films_exact, selections_films_contient, selections_films_proposes]
    ).head(15)

    liste_titres = list(selections_films["Titre vo"])
    list_reals = list(selections_films["real"])
    liste_dates = list(selections_films["Année"])
    liste_propos = []
    for i in range(len(liste_titres)):
        liste_propos.append(
            liste_titres[i] + " de " + list_reals[i] + f"({int(liste_dates[i])})"
        )

    liste_clefs = list(selections_films.index)
    dico_films = dict(zip(liste_propos, liste_clefs))
    choix = st.selectbox("Propositions : ", liste_propos)


if len(dico_films) > 0:
    with st.sidebar:
        st.header("Vous avez sélectionné : ")

        # Affichage du film sélectionné
        index = dico_films[choix]
        st.write(choix)
        st.write("Genres : ", df_list.iloc[index]["genres"])
        try:
            img_url = df_list.iloc[index]["poster_path"]
            path = "https://image.tmdb.org/t/p/original"
            url = path + img_url
            st.image(url, width=150)
        except:
            pass

    # Affichage des reco et liens IMDB
    st.header("Nous vous recommandons : ")

    df_reco = recommandation(index, tfidf_matrix, genre, filtre_note)

    url_diapo = """
        <style>
            .scroll-container {
            background-color: #ffff;
            overflow: auto;
            white-space: nowrap;
            padding: 10px;
        }

        .image-container {
            display: inline-block;
            text-align: center;
            margin-right: 20px; /* Espace entre les images */
        }

        .caption {
            margin-top: 5px;
            font-style: italic;
            /* Ajoutez d'autres styles de légende selon votre préférence */
        }
                </style>
    <div class="scroll-container">"""

    url_images = ""

    for idx in range(10):
        try:
            img_url = df_reco.iloc[idx]["poster_path"]
            path = "https://image.tmdb.org/t/p/original"
            url = path + img_url
            # st.image(url, width=150, caption=df_reco.iloc[idx]["Titre vo"])
            url_images += (
                '<div class="image-container"><a href="https://www.imdb.com/title/'
                + df_reco.iloc[idx]["tconst"]
                + '"target="_blank">'
                + '<img src="'
                + url
                + '" width="300"></a><p class="caption">'
                + df_reco.iloc[idx]["Titre vo"]
                + "</p></div>"
            )
        except:
            pass

    url_diapo += url_images + "</div>"
    st.markdown(url_diapo, unsafe_allow_html=True)

else:
    st.header("Nous n'avons pas trouvé ce titre…")
