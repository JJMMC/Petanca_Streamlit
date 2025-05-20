import streamlit as st
import datetime
import pandas as pd
import altair as alt
from db_utils import create_tables, add_player, add_team, add_match, add_team_player
from db_utils import get_players, get_teams, get_matches, get_team_player
from db_utils import get_matches_with_players, get_pareja_mas_ganadora,get_jugador_mas_ganador
# Conexiones
#jugadores = get_players()
#equipos = get_teams()
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
    jugadores = get_players()
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
            
            # Creamos la partida
            add_match(fecha, puntos1, puntos2, ganador)
            partida_id = get_matches()
            partida_id = partida_id[-1]
            
            #Creamos el equipo
            add_team(partida_id[0], 1)
            add_team(partida_id[0], 2)
            equipo_id = [equipo_id for equipo_id, _ , _ in get_teams()]

            # Generamos las entradas en la tabla relacional equipos-jugadores
            # Añadimos el Jugador 1 a la tabla equipo jugador
            if jugador1 in jugadores_dict:
                jugador_id = jugadores_dict[jugador1]
                add_team_player(equipo_id[-2], jugador_id)
            
            # Añadimos el Jugador 2 a la tabla equipo jugador
            if jugador2 in jugadores_dict:
                jugador_id = jugadores_dict[jugador2]
                add_team_player(equipo_id[-2], jugador_id)
            
            # Añadimos el Jugador 3 a la tabla equipo jugador
            if jugador3 in jugadores_dict:
                jugador_id = jugadores_dict[jugador3]
                add_team_player(equipo_id[-1], jugador_id)
            
            # Añadimos el Jugador 4 a la tabla equipo jugador
            if jugador4 in jugadores_dict:
                jugador_id = jugadores_dict[jugador4]
                add_team_player(equipo_id[-1], jugador_id)

            
            # add_team(partida_id, equipo_id)
            st.success("Partida registrada exitosamente.")

def estadisticas_v():
    st.header("📊 Estadísticas de Partidas de Petanca")

    # Obtener las partidas desde la base de datos
    partidas = get_matches()
    if not partidas:
        st.info("No hay partidas registradas.")
        return

    # Crear DataFrame con las partidas
    partidas_df = pd.DataFrame(partidas, columns=["ID", "Fecha", "Duración", "Puntos_Equipo1", "Puntos_Equipo2", "Ganador"])
    partidas_df["Fecha"] = pd.to_datetime(partidas_df["Fecha"])

    # Obtener datos adicionales de otras tablas
    jugadores = get_players()
    equipos = get_teams()
    equipos_jugadores = pd.DataFrame(get_team_player(), columns=["Equipo_ID", "Jugador_ID"])

    jugadores_df = pd.DataFrame(jugadores, columns=["ID", "Nombre"])
    equipos_df = pd.DataFrame(equipos, columns=["ID", "Partida_ID", "Equipo_Numero"])

    # 1. Jugadores más frecuentes en partidas
    jugadores_frecuencia = equipos_jugadores["Jugador_ID"].value_counts().reset_index()
    jugadores_frecuencia.columns = ["Jugador_ID", "Participaciones"]
    jugadores_frecuencia = jugadores_frecuencia.merge(jugadores_df, left_on="Jugador_ID", right_on="ID")
    st.subheader("👤 Jugadores más Frecuentes")
    st.dataframe(jugadores_frecuencia[["Nombre", "Participaciones"]])

    # # 2. Promedio de puntos por jugador
    # equipos_puntos = equipos_df.merge(partidas_df, left_on="Partida_ID", right_on="ID")
    # equipos_puntos["Puntos"] = equipos_puntos.apply(
    #     lambda row: row["Puntos_Equipo1"] if row["Equipo_Numero"] == 1 else row["Puntos_Equipo2"], axis=1
    # )
    # puntos_por_jugador = equipos_jugadores.merge(equipos_puntos, left_on="Equipo_ID", right_on="ID")
    # puntos_por_jugador = puntos_por_jugador.groupby("Jugador_ID")["Puntos"].mean().reset_index()
    # puntos_por_jugador = puntos_por_jugador.merge(jugadores_df, left_on="Jugador_ID", right_on="ID")
    # st.subheader("🎯 Promedio de Puntos por Jugador")
    # st.dataframe(puntos_por_jugador[["Nombre", "Puntos"]])

    # # 3. Duración promedio de partidas por equipo
    # duracion_por_equipo = equipos_df.merge(partidas_df, left_on="Partida_ID", right_on="ID")
    # duracion_promedio = duracion_por_equipo.groupby("Equipo_Numero")["Duración"].mean().reset_index()
    # duracion_promedio.columns = ["Equipo", "Duración Promedio (segundos)"]
    # st.subheader("⏱️ Duración Promedio de Partidas por Equipo")
    # st.dataframe(duracion_promedio)

    # 4. Rendimiento de jugadores por equipo
    victorias_por_equipo = partidas_df.groupby("Ganador").size().reset_index(name="Victorias")
    victorias_por_equipo.columns = ["Equipo", "Victorias"]
    rendimiento_jugadores = equipos_jugadores.merge(equipos_df, left_on="Equipo_ID", right_on="ID")
    rendimiento_jugadores = rendimiento_jugadores.merge(partidas_df, left_on="Partida_ID", right_on="ID")
    rendimiento_jugadores = rendimiento_jugadores[rendimiento_jugadores["Ganador"] == rendimiento_jugadores["Equipo_Numero"]]
    rendimiento_jugadores = rendimiento_jugadores.groupby("Jugador_ID").size().reset_index(name="Victorias")
    rendimiento_jugadores = rendimiento_jugadores.merge(jugadores_df, left_on="Jugador_ID", right_on="ID")
    st.subheader("🏆 Rendimiento de Jugadores por Equipo")
    st.dataframe(rendimiento_jugadores[["Nombre", "Victorias"]])

    # 5. Historial de equipos
    historial_equipos = equipos_jugadores.merge(jugadores_df, left_on="Jugador_ID", right_on="ID")
    historial_equipos = historial_equipos.merge(equipos_df, left_on="Equipo_ID", right_on="ID")
    historial_equipos = historial_equipos.groupby(["Equipo_ID", "Equipo_Numero"])["Nombre"].apply(list).reset_index()
    st.subheader("📋 Historial de Equipos")
    st.dataframe(historial_equipos)


def estadisticas():
    st.header("📊 Estadísticas de Partidas de Petanca")

        # Mostrar tabla de partidas con jugadores por equipo y ganador
    st.subheader("📋 Partidas con Jugadores por Equipo y Ganador")
    df_partidas = get_matches_with_players()
    st.dataframe(df_partidas)

    # Mostrar la pareja más ganadora
    st.subheader("🥇 Pareja más ganadora")
    pareja = get_pareja_mas_ganadora()
    if not pareja.empty:
        st.write(f"La pareja más ganadora es: **{pareja.iloc[0]['jugador1']}** y **{pareja.iloc[0]['jugador2']}** con **{pareja.iloc[0]['victorias']}** victorias.")
    else:
        st.write("No hay suficientes datos para mostrar la pareja más ganadora.")

    # Mostrar el jugador más ganador
    st.subheader("🏅 Jugador más ganador")
    jugador = get_jugador_mas_ganador()
    if not jugador.empty:
        st.write(f"El jugador con más victorias es: **{jugador.iloc[0]['jugador']}** con **{jugador.iloc[0]['victorias']}** victorias.")
    else:
        st.write("No hay suficientes datos para mostrar el jugador más ganador.")

    # Obtener las partidas desde la base de datos
    partidas = get_matches()
    if not partidas:
        st.info("No hay partidas registradas.")
        return

    # Crear DataFrame con las partidas
    partidas_df = pd.DataFrame(partidas, columns=["ID", "Fecha", "Duración", "Puntos_Equipo1", "Puntos_Equipo2", "Ganador"])
    partidas_df["Fecha"] = pd.to_datetime(partidas_df["Fecha"])

    # Mostrar tabla de partidas
    st.subheader("📋 Partidas Registradas")
    st.dataframe(partidas_df)

    # Gráfico 1: Distribución de puntos por equipo
    st.subheader("🎯 Distribución de Puntos por Equipo")
    puntos_df = partidas_df.melt(id_vars=["ID"], value_vars=["Puntos_Equipo1", "Puntos_Equipo2"], 
                                 var_name="Equipo", value_name="Puntos")
    puntos_df["Equipo"] = puntos_df["Equipo"].replace({"Puntos_Equipo1": "Equipo 1", "Puntos_Equipo2": "Equipo 2"})
    chart_puntos = alt.Chart(puntos_df).mark_bar().encode(
        x=alt.X("Equipo:N", title="Equipo"),
        y=alt.Y("sum(Puntos):Q", title="Total de Puntos"),
        color="Equipo:N",
        tooltip=["Equipo", "sum(Puntos)"]
    ).properties(width=600, height=400)
    st.altair_chart(chart_puntos)

    # Gráfico 2: Número de victorias por equipo
    st.subheader("🏆 Número de Victorias por Equipo")
    victorias_df = partidas_df["Ganador"].value_counts().reset_index()
    victorias_df.columns = ["Equipo", "Victorias"]
    chart_victorias = alt.Chart(victorias_df).mark_bar().encode(
        x=alt.X("Equipo:N", title="Equipo"),
        y=alt.Y("Victorias:Q", title="Número de Victorias"),
        color="Equipo:N",
        tooltip=["Equipo", "Victorias"]
    ).properties(width=600, height=400)
    st.altair_chart(chart_victorias)

    # Gráfico 3: Duración de las partidas a lo largo del tiempo
    st.subheader("⏱️ Duración de las Partidas a lo Largo del Tiempo")
    chart_duracion = alt.Chart(partidas_df).mark_line(point=True).encode(
        x=alt.X("Fecha:T", title="Fecha"),
        y=alt.Y("Duración:Q", title="Duración (segundos)"),
        tooltip=["Fecha", "Duración"]
    ).properties(width=600, height=400)
    st.altair_chart(chart_duracion)

    # Gráfico 4: Comparación de puntos anotados por partida
    st.subheader("⚔️ Comparación de Puntos por Partida")
    chart_comparacion = alt.Chart(partidas_df).mark_bar().encode(
        x=alt.X("ID:O", title="ID de Partida"),
        y=alt.Y("Puntos_Equipo1:Q", title="Puntos Equipo 1", axis=alt.Axis(titleColor="blue")),
        color=alt.value("blue"),
        tooltip=["ID", "Puntos_Equipo1"]
    ).properties(width=600, height=200).interactive() | alt.Chart(partidas_df).mark_bar().encode(
        x=alt.X("ID:O", title="ID de Partida"),
        y=alt.Y("Puntos_Equipo2:Q", title="Puntos Equipo 2", axis=alt.Axis(titleColor="red")),
        color=alt.value("red"),
        tooltip=["ID", "Puntos_Equipo2"]
    ).properties(width=600, height=200).interactive()
    st.altair_chart(chart_comparacion)

    # Resumen general
    st.subheader("📈 Resumen General")
    total_partidas = len(partidas_df)
    total_puntos_equipo1 = partidas_df["Puntos_Equipo1"].sum()
    total_puntos_equipo2 = partidas_df["Puntos_Equipo2"].sum()
    equipo_mas_victorias = victorias_df.loc[victorias_df["Victorias"].idxmax(), "Equipo"]

    st.write(f"- Total de partidas jugadas: **{total_partidas}**")
    st.write(f"- Total de puntos anotados por Equipo 1: **{total_puntos_equipo1}**")
    st.write(f"- Total de puntos anotados por Equipo 2: **{total_puntos_equipo2}**")
    st.write(f"- Equipo con más victorias: **{equipo_mas_victorias}**")

