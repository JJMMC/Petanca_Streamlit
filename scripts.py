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
    
    # Mostrar Partidas:
    st.subheader("Partidas Registradas")
    st.dataframe(partidas_df)
    
    # Filtro de fechas
        # Convertir las fechas a objetos datetime
    fechas = pd.to_datetime(partidas_df["Fecha"])
    print(fechas)
    print(type(fechas))
    fecha_min, fecha_max = fechas.min(), fechas.max()
            
        # Asegurarse de que fecha_min y fecha_max sean del tipo datetime
    if isinstance(fecha_min, pd.Timestamp):
        fecha_min = fecha_min.to_pydatetime()
        print(fecha_min, 'ESTO ES FECHA MIN')
        print(type(fecha_min))
    if isinstance(fecha_max, pd.Timestamp):
        fecha_max = fecha_max.to_pydatetime()
        print(fecha_max, 'ESTO ES FECHA MAX')
        print(type(fecha_max))
                
        # Crear el slider con las fechas convertidas
    fecha_rango = st.slider("Seleccionar rango de fechas", fecha_min, fecha_max, (fecha_min, fecha_max))

    # Estadísticas de jugadores
    st.subheader("🏅 Estadísticas de Jugadores")
    jugadores_victorias = partidas_df["Ganador"].value_counts()
    mejor_jugador = jugadores_victorias.idxmax()
    victorias_mejor_jugador = jugadores_victorias.max()

    st.write(f"**Mejor jugador:** {mejor_jugador} con {victorias_mejor_jugador} victorias.")

    # Estadísticas de equipos
    st.subheader("🤝 Estadísticas de Equipos")
    partidas_df["Equipo1"] = partidas_df["Jugador1_Equipo1"] + " y " + partidas_df["Jugador2_Equipo1"]
    partidas_df["Equipo2"] = partidas_df["Jugador1_Equipo2"] + " y " + partidas_df["Jugador2_Equipo2"]

    equipos_victorias = partidas_df["Ganador"].value_counts()
    mejor_equipo = equipos_victorias.idxmax()
    victorias_mejor_equipo = equipos_victorias.max()

    st.write(f"**Mejor combinación de equipo:** {mejor_equipo} con {victorias_mejor_equipo} victorias.")

    # Resumen general
    st.subheader("📊 Resumen General")
    total_partidas = len(partidas_df)
    total_puntos_equipo1 = partidas_df["Puntos_Equipo1"].sum()
    total_puntos_equipo2 = partidas_df["Puntos_Equipo2"].sum()

    st.write(f"- Total de partidas jugadas: {total_partidas}")
    st.write(f"- Total de puntos anotados por Equipo 1: {total_puntos_equipo1}")
    st.write(f"- Total de puntos anotados por Equipo 2: {total_puntos_equipo2}")    
    
    

