import pandas as pd
import numpy as np
import pickle
with open('songlist.pkl', 'rb') as f:
    music = pickle.load(f)


with open('top_k_similarity_faiss.pkl', 'rb') as r:
    similarity = pickle.load(r)

df = pd.DataFrame(similarity)
#print(df.head())
print(music.head())
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(name):
    recommended_list = []
    recommended_music_posters = []

    idx = music[music['song'] == name].index[0]
    recommended_indices = df.iloc[idx, 1:6]
    for i in recommended_indices:
        song_name = music.iloc[i]['song']
        tags = music.iloc[i]['tags']
        artist = tags.split()[0]

        recommended_music_posters.append(get_song_album_cover_url(song_name, artist))
        recommended_list.append(song_name)

    return recommended_list,recommended_music_posters


st.header('Music Recommender System')
music_list = music['song'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)
if st.button('Show Recommendation'):
    recommended_music_names,recommended_music_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])

    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
