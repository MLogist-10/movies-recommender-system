
import os
import streamlit as st
import pickle
import pandas as pd
import requests

api_key= st.secrets["TMDB_API_KEY"]

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_l = pickle.load(open('movies.pkl','rb'))

movies = pd.DataFrame(movies_l)


import gdown

url = 'https://drive.google.com/uc?id=1vkvAE1_nQpwEtKUYUmsEWL0F-Y9dYllo'
output = 'similarity.pkl'

# Download only if file doesn't exist locally
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

st.title("Movie Recommender System")
movies_l = movies_l["title"].values
selected_movie_name = st.selectbox(
"Select the movie name...",
movies_l)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    import streamlit as st

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])