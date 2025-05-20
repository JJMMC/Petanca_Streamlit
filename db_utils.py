import sqlite3
import pandas as pd

DB_PATH = 'database.db'

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            photo_path TEXT,
            creation_date DATE          
            )
        ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            duracion INTEGER, -- Duración en segundos
            puntos_equipo1 INTEGER NOT NULL,
            puntos_equipo2 INTEGER NOT NULL,
            ganador TEXT NOT NULL -- Equipo ganador (Equipo 1 o Equipo 2)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            equipo_numero INTEGER NOT NULL, -- 1 para Equipo 1, 2 para Equipo 2
            FOREIGN KEY(partida_id) REFERENCES matches(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS teams_players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_id INTEGER NOT NULL,
            jugador_id INTEGER NOT NULL,
            FOREIGN KEY(equipo_id) REFERENCES teams(id),
            FOREIGN KEY(jugador_id) REFERENCES players(id)
        )
    ''')

    conn.commit()
    conn.close()

# CRUD Operations
def add_player(name, surname, photo_path, creation_date ):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO players (name, surname, photo_path, creation_date) VALUES (?, ?, ?, ?)', (name, surname, photo_path, creation_date))
    conn.commit()
    conn.close()

def update_player(player_id, name=None, surname=None, photo_path=None):
    """
    Actualiza los datos de un jugador en la tabla 'players'.

    Args:
        player_id (int): ID del jugador a actualizar.
        name (str, optional): Nuevo nombre del jugador.
        surname (str, optional): Nuevo apellido del jugador.
        photo_path (str, optional): Nueva ruta de la foto del jugador.
    """
    conn = get_connection()
    c = conn.cursor()
    updates = []
    params = []

    if name:
        updates.append("name = ?")
        params.append(name)
    if surname:
        updates.append("surname = ?")
        params.append(surname)
    if photo_path:
        updates.append("photo_path = ?")
        params.append(photo_path)

    params.append(player_id)
    query = f"UPDATE players SET {', '.join(updates)} WHERE id = ?"
    c.execute(query, params)
    conn.commit()
    conn.close()

def delete_player(player_id):
    """
    Elimina un jugador de la tabla 'players'.

    Args:
        player_id (int): ID del jugador a eliminar.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM players WHERE id = ?', (player_id,))
    conn.commit()
    conn.close()

def get_players():
    with get_connection() as conn:
        c = conn.cursor()
        players = c.execute('SELECT id, name FROM players').fetchall()
    return players

def get_player_by_id(player_id):
    """
    Obtiene los detalles de un jugador por su ID.

    Args:
        player_id (int): ID del jugador.

    Returns:
        tuple: Detalles del jugador (id, name, surname, photo_path, creation_date).
    """
    conn = get_connection()
    c = conn.cursor()
    jugador = c.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
    conn.close()
    return jugador

def add_match(fecha, puntos_equipo1, puntos_equipo2, ganador):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO matches (fecha, puntos_equipo1, puntos_equipo2, ganador) VALUES (?, ?, ?, ?)',
              (fecha, puntos_equipo1, puntos_equipo2, ganador))
    conn.commit()
    conn.close()

def get_matches():
    conn = get_connection()
    c = conn.cursor()
    matches = c.execute('SELECT * FROM matches').fetchall()
    conn.close()
    return matches

def delete_match(partida_id):
    """
    Elimina una partida de la tabla 'matches'.

    Args:
        partida_id (int): ID de la partida a eliminar.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM matches WHERE id = ?', (partida_id,))
    conn.commit()
    conn.close()

def add_team(partida_id, equipo_numero):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO teams (partida_id, equipo_numero) VALUES (?, ?)', (partida_id, equipo_numero))
    conn.commit()
    conn.close()
    
def get_teams():
    conn = get_connection()
    c = conn.cursor()
    teams = c.execute('SELECT * FROM teams').fetchall()
    conn.close()
    return teams

def add_team_player(equipo_id, jugador_id,):
    """
    Inserta un jugador en un equipo en la tabla 'teams_players'.

    Args:
        equipo_id (int): ID del equipo.
        jugador_id (int): ID del jugador.
        equipo_numero (int): Número del equipo (1 o 2).
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO teams_players (equipo_id, jugador_id) VALUES (?, ?)',
              (equipo_id, jugador_id))
    conn.commit()
    conn.close()

def get_team_player():
    conn = get_connection()
    c = conn.cursor()
    teams = c.execute('SELECT equipo_id, jugador_id FROM teams_players').fetchall()
    conn.close()
    return teams



# Functions to errase data in database 
def clear_tables_except_players():
    """
    Borra el contenido de todas las tablas excepto la tabla 'players'.
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Deshabilitar las restricciones de claves foráneas temporalmente
    c.execute('PRAGMA foreign_keys = OFF;')
    
    # Borrar el contenido de las tablas en el orden correcto para evitar conflictos
    c.execute('DELETE FROM teams_players;')
    c.execute('DELETE FROM teams;')
    c.execute('DELETE FROM matches;')
    
    # Habilitar las restricciones de claves foráneas nuevamente
    c.execute('PRAGMA foreign_keys = ON;')
    
    conn.commit()
    conn.close()

def clear_all_tables():
    """
    Borra el contenido de todas las tablas en la base de datos.
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Deshabilitar las restricciones de claves foráneas temporalmente
    c.execute('PRAGMA foreign_keys = OFF;')
    
    # Borrar el contenido de todas las tablas
    c.execute('DELETE FROM teams_players;')
    c.execute('DELETE FROM teams;')
    c.execute('DELETE FROM matches;')
    c.execute('DELETE FROM players;')
    
    # Habilitar las restricciones de claves foráneas nuevamente
    c.execute('PRAGMA foreign_keys = ON;')
    
    conn.commit()
    conn.close()

def export_db_to_excel(excel_path='export_petanca.xlsx'):
    """
    Exporta todas las tablas de la base de datos a un archivo Excel.
    Cada tabla será una hoja diferente.
    """
    conn = get_connection()
    tablas = ['players', 'matches', 'teams', 'teams_players']
    with pd.ExcelWriter(excel_path) as writer:
        for tabla in tablas:
            df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
            df.to_excel(writer, sheet_name=tabla, index=False)
    conn.close()
    print(f"Datos exportados a {excel_path}")

if __name__ == "__main__":
    #create_tables()
    #clear_all_tables()
    #export_db_to_excel()
    pass