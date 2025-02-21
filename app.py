import streamlit as st
import json
from datetime import datetime

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
st.title("🎵 Filtrador de Músicas do Spotify por Data 🎵")

# Criar seletores de ano, mês e dia
years = sorted(set(parse_date(song["release_date"]) for song in songs if parse_date(song["release_date"]) is not None))
months = list(range(1, 13))
days = list(range(1, 32))

year = st.selectbox("Selecione o Ano", [None] + years)
month = st.selectbox("Selecione o Mês", [None] + months)
day = st.selectbox("Selecione o Dia", [None] + days)

# Filtrar músicas com base na seleção
filtered_songs = filter_songs(year, month, day)

# Mostrar resultados
st.subheader(f"🎶 {len(filtered_songs)} músicas encontradas:")
for song in filtered_songs:
    col1, col2 = st.columns([1, 4])
    with col1:
        if song.get("album_cover"):
            st.image(song["album_cover"], width=80)
    with col2:
        st.write(f"**{song['name']}** - {song['artist']} ({song['release_date']})")
        st.markdown(f"[Ouvir no Spotify]({song['spotify_url']})")
