# -*- coding: utf-8 -*-

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json

# Carrega as credenciais do arquivo .env
load_dotenv()

# Autenticação com a API do Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private"
))

# Lista das playlists 
playlist_ids = [
    "7q6DU8dGQx2PNuO9kt7CBl",
    "6Sa8OHGCRwzXFDpPIV7alz",
    "3mnKaaHdILmHtgJAkZsRSP",
    "3F7jgnLHEozgfhf3RjLC1U"
]

songs_data = []

# Busca as músicas de cada playlist
for playlist_id in playlist_ids:
    results = sp.playlist_tracks(playlist_id)
    for item in results["items"]:
        track = item["track"]
        if track:
            song_info = {
                "playlist_id": playlist_id,
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "spotify_url": track["external_urls"]["spotify"],
                "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else None  # Adiciona a capa do álbum
            }
            songs_data.append(song_info)

# Salva os dados em um arquivo JSON
with open("songs.json", "w", encoding="utf-8") as json_file:
    json.dump(songs_data, json_file, ensure_ascii=False, indent=4)

print("Arquivo 'songs.json' atualizado com sucesso!")
