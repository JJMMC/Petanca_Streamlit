import streamlit as st
import pandas as pd
import datetime
import altair as alt
import sqlite3
from db_utils import create_tables
from scripts import incio, pag_add_players, save_match, estadisticas


def main():
    # Inicializar BD
    #create_tables()

    st.set_page_config(page_title="Petanca Manager", page_icon='resources/boule.png' ,layout="centered")
    st.title("Widget Partidas de petanca")
    

    # Sidebar Menu
    menu = st.sidebar.selectbox("Menu", ["Inicio","Agregar Jugadores","Editar Jugadores", "Registrar Partida", "Ver Estadísticas"])

    # Pages
    if menu == "Inicio":
        incio()

    elif menu == "Agregar Jugadores":
        pag_add_players()

    elif menu == "Editar Jugadores":
        pass

    elif menu == "Registrar Partida":
        save_match()

    elif menu == "Ver Estadísticas":
        estadisticas()


if __name__ == "__main__":
    #create_tables()
    main()