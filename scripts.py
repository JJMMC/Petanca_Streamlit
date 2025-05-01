import streamlit as st
import datetime
import pandas as pd
import datetime
import altair as alt
import sqlite3
from db_utils import create_tables, add_player, add_equipo, add_partida, get_jugadores, get_equipos, get_partidas

# Conexiones
jugadores = get_jugadores()
#equipos = get_equipos()
photo_path = 'resources/users_photo'

def incio():
    st.header("¿Parqué es esta aplicación?")
    st.write('Descripcion de la aplicación')

def pag_add_players():
    st.header("👤 Agregar nuevo jugador")
    with st.form(key='form_reinicio', clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del jugador")
    
        with col2:
            apellido = st.text_input("Apellido del jugador")
    
        if st.form_submit_button("Guardar jugador"):
            add_player(nombre, apellido, photo_path, creation_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.success(f"Jugador '{nombre}' agregado correctamente.")
    st.rerun()

def save_match():
    st.header("⚔️ Registrar nueva partida")

    if len(jugadores) < 4:
        st.warning("Agrega al menos 4 jugadores para crear una partida.")
    else:
        jugadores_dict = {nombre: id for id, nombre in jugadores}
        jugadores_disponibles = list(jugadores_dict.keys())  # Lista de jugadores disponibles

        st.write('Equipo 1')
        col1, col2 = st.columns(2)
        with col1:
            jugador1 = st.selectbox("Jugador 1", jugadores_disponibles, index=0)
            jugadores_disponibles.remove(jugador1)  # Eliminar jugador seleccionado
        with col2:
            jugador2 = st.selectbox("Jugador 2", jugadores_disponibles, index=0)
            jugadores_disponibles.remove(jugador2)  # Eliminar jugador seleccionado

        st.write('Equipo 2')
        col3, col4 = st.columns(2)
        with col3:
            jugador3 = st.selectbox("Jugador 3", jugadores_disponibles, index=0)
            jugadores_disponibles.remove(jugador3)  # Eliminar jugador seleccionado
        with col4:
            jugador4 = st.selectbox("Jugador 4", jugadores_disponibles, index=0)
            jugadores_disponibles.remove(jugador4)  # Eliminar jugador seleccionado

        puntos1 = st.number_input("Puntos del Equipo 1", 0, 13, step=1)
        puntos2 = st.number_input("Puntos del Equipo 2", 0, 13, step=1)

        if st.button("Guardar Partida"):
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if puntos1 > puntos2:
                st.success(f'Equipo 1 - {jugador1} y {jugador2} GANARON')
                ganador = 'Equipo 1'
            else:
                st.success(f'Equipo 2 - {jugador3} y {jugador4} GANARON')
                ganador = 'Equipo 2'
            add_partida(fecha, jugador1, jugador2, jugador3, jugador4, puntos1, puntos2, ganador)
            st.success("Partida registrada exitosamente.")

            
def estadisticas():
    st.header("📈 Estadísticas de Partidas")

    partidas = get_partidas()
    if not partidas:
        st.info("No hay partidas registradas.")
        return

    # Crear DataFrame con las partidas
    partidas_df = pd.DataFrame(partidas, columns=["ID", "Fecha", "Jugador1_Equipo1", "Jugador2_Equipo1", "Jugador1_Equipo2", "Jugador2_Equipo2", "Puntos_Equipo1", "Puntos_Equipo2", "Ganador"])
    
    # Validar que las columnas críticas no tengan valores nulos
    partidas_df = partidas_df.dropna(subset=["Fecha", "Ganador", "Jugador1_Equipo1", "Jugador2_Equipo1", "Jugador1_Equipo2", "Jugador2_Equipo2"])
    
    # Convertir la columna de fechas a formato datetime
    partidas_df["Fecha"] = pd.to_datetime(partidas_df["Fecha"], errors="coerce")
    
    # Validar que haya fechas válidas
    if partidas_df["Fecha"].isnull().all():
        st.warning("No hay fechas válidas en las partidas registradas.")
        return
    
    # Mostrar Partidas:
    st.subheader("Partidas Registradas")
    st.dataframe(partidas_df)

    # # Filtro de rango de fechas
    # fecha_min, fecha_max = partidas_df["Fecha"].min(), partidas_df["Fecha"].max()
    # fecha_rango = st.slider("Seleccionar rango de fechas", fecha_min, fecha_max, (fecha_min, fecha_max))
    # partidas_filtradas = partidas_df[(partidas_df["Fecha"] >= fecha_rango[0]) & (partidas_df["Fecha"] <= fecha_rango[1])]

    # if partidas_filtradas.empty:
    #     st.warning("No hay partidas en el rango de fechas seleccionado.")
    #     return

    # # Mostrar partidas filtradas
    # st.subheader("📋 Partidas Registradas")
    # st.dataframe(partidas_filtradas)

    # # Conteo de victorias por equipo
    # st.subheader("🏆 Victorias por Equipo")
    # victorias = partidas_filtradas["Ganador"].value_counts().reset_index()
    # victorias.columns = ["Equipo", "Victorias"]

    # chart_victorias = alt.Chart(victorias).mark_bar().encode(
    #     x=alt.X("Equipo", sort="-y"),
    #     y="Victorias",
    #     color="Equipo"
    # ).properties(
    #     title="Victorias por Equipo"
    # )
    # st.altair_chart(chart_victorias, use_container_width=True)

    # # Estadísticas individuales por jugador
    # st.subheader("🎯 Estadísticas por Jugador")
    # jugadores_estadisticas = {}

    # for _, partida in partidas_filtradas.iterrows():
    #     for jugador in [partida["Jugador1_Equipo1"], partida["Jugador2_Equipo1"], partida["Jugador1_Equipo2"], partida["Jugador2_Equipo2"]]:
    #         if jugador not in jugadores_estadisticas:
    #             jugadores_estadisticas[jugador] = {"Victorias": 0, "Partidas_Jugadas": 0}
    #         jugadores_estadisticas[jugador]["Partidas_Jugadas"] += 1

    #     if partida["Ganador"] == "Equipo 1":
    #         jugadores_estadisticas[partida["Jugador1_Equipo1"]]["Victorias"] += 1
    #         jugadores_estadisticas[partida["Jugador2_Equipo1"]]["Victorias"] += 1
    #     elif partida["Ganador"] == "Equipo 2":
    #         jugadores_estadisticas[partida["Jugador1_Equipo2"]]["Victorias"] += 1
    #         jugadores_estadisticas[partida["Jugador2_Equipo2"]]["Victorias"] += 1

    # estadisticas_df = pd.DataFrame.from_dict(jugadores_estadisticas, orient="index").reset_index()
    # estadisticas_df.columns = ["Jugador", "Victorias", "Partidas_Jugadas"]
    # estadisticas_df["Porcentaje_Victorias"] = (estadisticas_df["Victorias"] / estadisticas_df["Partidas_Jugadas"] * 100).round(2)

    # st.dataframe(estadisticas_df.sort_values(by="Victorias", ascending=False))

    # chart_jugadores = alt.Chart(estadisticas_df).mark_bar().encode(
    #     x=alt.X("Jugador", sort="-y"),
    #     y="Victorias",
    #     color="Jugador"
    # ).properties(
    #     title="Victorias por Jugador"
    # )
    # st.altair_chart(chart_jugadores, use_container_width=True)