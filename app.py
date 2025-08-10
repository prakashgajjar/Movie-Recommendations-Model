import streamlit as st
import pickle, gzip
import pandas as pd
import requests

def getPoster(name):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key=53255c2ac6abcdeab85fb67ec45fe8e2&query={name}",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ Could not fetch poster for {name}: {e}")
    return None


def recommendMovie(name):
    idx = movies[movies['title'] == name].index[0]
    distances = similarity[idx]
    sorted_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in sorted_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(getPoster(movie_title))
    return recommended_movies, recommended_posters


with gzip.open("movie_dict.pkl.gz", "rb") as f:
    movies_dict = pickle.load(f)

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movies_dict)

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox("Choose a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommendMovie(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster or "https://via.placeholder.com/200x300?text=No+Image", caption=name)
