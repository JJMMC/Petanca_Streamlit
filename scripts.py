import streamlit as st
import datetime
import pandas as pd
import datetime
import altair as alt
import sqlite3
from db_utils import create_tables, add_jugador, add_equipo, add_partida, get_jugadores, get_equipos, get_partidas

# Conexiones
jugadores = get_jugadores()
equipos = get_equipos()

def incio():
    st.header("¿Parqué es esta aplicación?")
    st.write('Descripcion de la aplicación')

def add_players():
    st.header("👤 Agregar nuevo jugador")
    nombre = st.text_input("Nombre del jugador")
    apellido = st.text_input("Apellido del jugador")
    
    if st.button("Guardar jugador"):
        add_jugador(nombre)
        st.success(f"Jugador '{nombre}' agregado correctamente.")
        st.rerun()

def save_match():
    st.header("⚔️ Registrar nueva partida")

    if len(jugadores) < 4:
        st.warning("Agrega al menos 4 jugadores para crear una partida.")
    else:
        jugadores_dict = {nombre: id for id, nombre in jugadores}

        equipo1_nombre = st.text_input("Nombre del Equipo 1")
        col1, col2 = st.columns(2)
        with col1:
            jugador1 = st.selectbox("Jugador 1", jugadores_dict.keys())
        with col2:
            jugador2 = st.selectbox("Jugador 2", jugadores_dict.keys())

        equipo2_nombre = st.text_input("Nombre del Equipo 2")
        col3, col4 = st.columns(2)
        with col3:
            jugador3 = st.selectbox("Jugador 3", jugadores_dict.keys())
        with col4:
            jugador4 = st.selectbox("Jugador 4", jugadores_dict.keys())

        puntos1 = st.number_input("Puntos del Equipo 1", 0, 13, step=1)
        puntos2 = st.number_input("Puntos del Equipo 2", 0, 13, step=1)

        if st.button("Guardar Partida"):
            add_equipo(equipo1_nombre, jugadores_dict[jugador1], jugadores_dict[jugador2])
            add_equipo(equipo2_nombre, jugadores_dict[jugador3], jugadores_dict[jugador4])

            equipos_actualizados = get_equipos()
            equipo1_id = next(id for id, nombre in equipos_actualizados if nombre == equipo1_nombre)
            equipo2_id = next(id for id, nombre in equipos_actualizados if nombre == equipo2_nombre)

            ganador_id = equipo1_id if puntos1 > puntos2 else equipo2_id
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            add_partida(fecha, equipo1_id, equipo2_id, puntos1, puntos2, ganador_id)
            st.success("Partida registrada exitosamente.")
            st.rerun()

def estadisticas():
    st.header("📈 Estadísticas de Partidas")

    partidas = get_partidas()
    if not partidas:
        st.info("No hay partidas registradas.")
    else:
        conn = None
        equipos = dict(get_equipos())
        jugadores = dict(get_jugadores())

        partidas_df = pd.DataFrame(partidas, columns=["ID", "Fecha", "Equipo1", "Equipo2", "Puntos1", "Puntos2", "Ganador"])

        # Filtro de fechas
            # Convertir las fechas a objetos datetime
        fechas = pd.to_datetime(partidas_df["Fecha"])
        fecha_min, fecha_max = fechas.min(), fechas.max()
            
            # Asegurarse de que fecha_min y fecha_max sean del tipo datetime
        if isinstance(fecha_min, pd.Timestamp):
            fecha_min = fecha_min.to_pydatetime()
        if isinstance(fecha_max, pd.Timestamp):
            fecha_max = fecha_max.to_pydatetime()
                
            # Crear el slider con las fechas convertidas
        fecha_rango = st.slider("Seleccionar rango de fechas", fecha_min, fecha_max, (fecha_min, fecha_max))
            
        partidas_df["Fecha"] = pd.to_datetime(partidas_df["Fecha"])
        partidas_filtradas = partidas_df[(partidas_df["Fecha"] >= fecha_rango[0]) & (partidas_df["Fecha"] <= fecha_rango[1])]

        st.dataframe(partidas_filtradas)

        # Conteo de victorias
        victorias = partidas_filtradas["Ganador"].value_counts().reset_index()
        victorias.columns = ["Equipo_ID", "Victorias"]
        victorias["Equipo"] = victorias["Equipo_ID"].map(equipos)

        # Gráfico de victorias
        chart = alt.Chart(victorias).mark_bar().encode(
            x='Equipo',
            y='Victorias',
            color='Equipo'
        ).properties(
            title="Victorias por Equipo"
        )

        st.altair_chart(chart, use_container_width=True)

        # Estadísticas individuales
        st.subheader("🏅 Estadísticas por Jugador")

        jugadores_estadisticas = {nombre: 0 for nombre in jugadores.values()}

        for partida in partidas_filtradas.itertuples():
            ganador_equipo_id = partida.Ganador
            jugador_ids = []

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            equipo = c.execute('SELECT jugador1_id, jugador2_id FROM equipos WHERE id=?', (ganador_equipo_id,)).fetchone()
            conn.close()

            if equipo:
                jugador_ids.extend(equipo)

            for j_id in jugador_ids:
                jugadores_estadisticas[jugadores[j_id]] += 1

        estadisticas_df = pd.DataFrame(list(jugadores_estadisticas.items()), columns=["Jugador", "Victorias"])
        estadisticas_df = estadisticas_df.sort_values(by="Victorias", ascending=False)

        st.dataframe(estadisticas_df)

        chart_jugadores = alt.Chart(estadisticas_df).mark_bar().encode(
            x='Jugador',
            y='Victorias',
            color='Jugador'
        ).properties(
            title="Victorias por Jugador"
        )

        st.altair_chart(chart_jugadores, use_container_width=True)