import streamlit as st
import json
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Top Songs Filter")

# Carrega os dados do arquivo JSON
with open("songs.json", "r", encoding="utf-8") as file:
    songs = json.load(file)

# Função para converter datas de diferentes formatos
def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%Y"):  # Primeiro tenta YYYY-MM-DD, depois apenas YYYY
        try:
            return datetime.strptime(date_str, fmt).year
        except ValueError:
            continue
    return None  # Retorna None se não conseguir converter

# Função para filtrar músicas por data
def filter_songs(year=None, month=None, day=None):
    filtered = []
    for song in songs:
        try:
            release_date = datetime.strptime(song["release_date"], "%Y-%m-%d")
            if (year and release_date.year != year) or \
               (month and release_date.month != month) or \
               (day and release_date.day != day):
                continue
            filtered.append(song)
        except ValueError:
            continue  # Pula músicas sem data válida
    return filtered

# Interface do Streamlit
st.markdown(
    """
    <div style="display:flex; align-items:center; justify-content:center; gap:10px; font-family: 'Circular', sans-serif; font-size: 32px; font-weight: bold; margin-bottom: 10px;">
        <a href="https://www.spotify.com" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg" width="40" height="40" style="transition: transform 0.3s ease-in-out;">
        </a>
        <span>Top Songs Filter - Spotify</span>
    </div>
    <div style="text-align:center; font-size: 20px; color: #f0f0f0; margin-bottom: 20px; font-weight: 500;">
        Encontre suas músicas favoritas com precisão! Use o filtro para explorar hits por ano, mês e dia e reviva momentos inesquecíveis através da música!
    </div>
    <style>
        a:hover img {
            transform: scale(1.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Criar seletores de ano, mês e dia
years = sorted(set(parse_date(song["release_date"]) for song in songs if parse_date(song["release_date"]) is not None))
months = list(range(1, 13))
days = list(range(1, 32))

year = st.selectbox("Selecione o Ano:", [None] + years)
month = st.selectbox("Selecione o Mês:", [None] + months)
day = st.selectbox("Selecione o Dia:", [None] + days)

# Filtrar músicas com base na seleção
filtered_songs = filter_songs(year, month, day)

# Mostrar resultados
st.subheader(f"🎶 {len(filtered_songs)} música(s) encontrada(s):")
for song in filtered_songs:
    col1, col2 = st.columns([1, 4])
    with col1:
        if song.get("album_cover"):
            st.image(song["album_cover"], width=80)
    with col2:
        st.write(f"**{song['name']}** - {song['artist']} ({song['release_date']})")
        st.markdown(
            f'<a href="{song["spotify_url"]}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none; display:flex; align-items:center; gap:8px;">'
            f'<img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg" width="20" height="20" style="vertical-align:middle; transition: transform 0.2s ease-in-out;">'
            f' <span style="transition: color 0.2s ease-in-out;">Ouvir no Spotify</span></a>'
            f'<style>a:hover img {{ transform: scale(1.1); }} a:hover span {{ color: #17a34a; }}</style>',
            unsafe_allow_html=True
        )

# Rodapé
st.markdown(
    """
    <div style="text-align:center; margin-top:40px; font-size:14px; color:white; padding:15px; border-radius:5px;">
        <strong>Top Songs Filter - Spotify</strong>
        <br><br>
        <strong>Samuel Lisboa, 2025</strong>
        <br>
        <a href="https://github.com/SamuelLisboaCodes" target="_blank" style="text-decoration:none; color:inherit; display:flex; align-items:center; justify-content:center; gap:8px; margin-top:10px;">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20" height="20" style="vertical-align:middle; filter: invert(1);">
            <span>SamuelLisboaCodes</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
