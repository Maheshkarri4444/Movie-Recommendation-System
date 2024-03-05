import streamlit as st
import pandas as pd
import pickle
import difflib
import requests

st.title("Movie Recommender")

movies_list=pickle.load(open('model.pkl','rb'))
movies=pd.DataFrame(movies_list)
movies.rename(columns={0:'index',1:'title',2:'mid'},inplace=True)

#print(type(movies))
#print(movies.columns)
print(movies.head())

similarity=pickle.load(open('similariy.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f2cad320eec71117737a1fab513ba1c7&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    finding = difflib.get_close_matches(movie, movies['title'], cutoff=0.5)
    matching = finding[0]
    index_movie = movies[movies['title'] == matching]['index'].values[0]
    sim_score = list(enumerate(similarity[index_movie]))
    sorted_sim_movies = sorted(sim_score, key=lambda x: x[1], reverse=True)
    recommendations = []
    recommended_posters=[]
    count = 1  
    for index, i in sorted_sim_movies:
        movie_id=movies.iloc[index]['mid']
        title_from_index = movies[movies['index'] == index]['title'].values[0]
        if count <= 8:
            recommendations.append(title_from_index)
            recommended_posters.append(fetch_poster(movie_id))
            count += 1
    return recommendations,recommended_posters
    


selected_movie=st.selectbox(
'Type the Movie Name',movies['title'].values )


if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    coll, col2, col3, col4, col5, col6  =st.columns(6)

    with coll:
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

    with col6:
        st.text(names[5])
        st.image(posters[5])





