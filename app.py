import streamlit as st
import pickle as pk
import pandas as pd
import requests

def movie_poster(movie_id):
    resp = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = resp.json()
    path = data["poster_path"]
    img = "https://image.tmdb.org/t/p/w500/" + path
    return img



movies_dict = pk.load(open('movies_dict.pkl','rb'))
similarity = pk.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title("movie recomender system")
movie_names = st.selectbox("How would you like to connect?",(movies['title'].values))

def recomended_movies(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]

    watchList = []
    posters = []
    for i in movies_list:
        watchList.append((movies.iloc[i[0]].title))
        posters.append(movie_poster(movies.iloc[i[0]].movie_id))
    return watchList,posters

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recomended_movies(movie_names)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
