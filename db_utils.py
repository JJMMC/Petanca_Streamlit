import sqlite3

DB_PATH = 'database.db'

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            photo_path TEXT,
            creation_date DATE          
            )
        ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            duracion INTEGER, -- Duración en segundos
            puntos_equipo1 INTEGER NOT NULL,
            puntos_equipo2 INTEGER NOT NULL,
            ganador TEXT NOT NULL -- Equipo ganador (Equipo 1 o Equipo 2)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            equipo_numero INTEGER NOT NULL, -- 1 para Equipo 1, 2 para Equipo 2
            FOREIGN KEY(partida_id) REFERENCES partidas(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS equipos_jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_id INTEGER NOT NULL,
            jugador_id INTEGER NOT NULL,
            FOREIGN KEY(equipo_id) REFERENCES equipos(id),
            FOREIGN KEY(jugador_id) REFERENCES jugadores(id)
        )
    ''')

    conn.commit()
    conn.close()

# CRUD Operations
def add_player(name, surname, photo_path, creation_date ):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO jugadores (name, surname, photo_path, creation_date) VALUES (?, ?, ?, ?)', (name, surname, photo_path, creation_date))
    conn.commit()
    conn.close()

def update_player(player_id, name=None, surname=None, photo_path=None):
    """
    Actualiza los datos de un jugador en la tabla 'jugadores'.

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
    query = f"UPDATE jugadores SET {', '.join(updates)} WHERE id = ?"
    c.execute(query, params)
    conn.commit()
    conn.close()

def delete_player(player_id):
    """
    Elimina un jugador de la tabla 'jugadores'.

    Args:
        player_id (int): ID del jugador a eliminar.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM jugadores WHERE id = ?', (player_id,))
    conn.commit()
    conn.close()

def get_jugadores():
    with get_connection() as conn:
        c = conn.cursor()
        jugadores = c.execute('SELECT id, name FROM jugadores').fetchall()
    return jugadores

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
    jugador = c.execute('SELECT * FROM jugadores WHERE id = ?', (player_id,)).fetchone()
    conn.close()
    return jugador

def add_partida(fecha, puntos_equipo1, puntos_equipo2, ganador):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO partidas (fecha, puntos_equipo1, puntos_equipo2, ganador) VALUES (?, ?, ?, ?)',
              (fecha, puntos_equipo1, puntos_equipo2, ganador))
    conn.commit()
    conn.close()

def get_partidas():
    conn = get_connection()
    c = conn.cursor()
    partidas = c.execute('SELECT * FROM partidas').fetchall()
    conn.close()
    return partidas

def delete_partida(partida_id):
    """
    Elimina una partida de la tabla 'partidas'.

    Args:
        partida_id (int): ID de la partida a eliminar.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM partidas WHERE id = ?', (partida_id,))
    conn.commit()
    conn.close()

def add_equipo(partida_id, equipo_numero):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO equipos (partida_id, equipo_numero) VALUES (?, ?)', (partida_id, equipo_numero))
    conn.commit()
    conn.close()
    
def get_equipos():
    conn = get_connection()
    c = conn.cursor()
    equipos = c.execute('SELECT * FROM equipos').fetchall()
    conn.close()
    return equipos

def add_equipo_jugador(equipo_id, jugador_id,):
    """
    Inserta un jugador en un equipo en la tabla 'equipos_jugadores'.

    Args:
        equipo_id (int): ID del equipo.
        jugador_id (int): ID del jugador.
        equipo_numero (int): Número del equipo (1 o 2).
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO equipos_jugadores (equipo_id, jugador_id) VALUES (?, ?)',
              (equipo_id, jugador_id))
    conn.commit()
    conn.close()

def get_equipo_jugador():
    conn = get_connection()
    c = conn.cursor()
    equipos = c.execute('SELECT equipo_id, jugador_id FROM equipos_jugadores').fetchall()
    conn.close()
    return equipos



# Functions to errase data in database 
def clear_tables_except_jugadores():
    """
    Borra el contenido de todas las tablas excepto la tabla 'jugadores'.
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Deshabilitar las restricciones de claves foráneas temporalmente
    c.execute('PRAGMA foreign_keys = OFF;')
    
    # Borrar el contenido de las tablas en el orden correcto para evitar conflictos
    c.execute('DELETE FROM equipos_jugadores;')
    c.execute('DELETE FROM equipos;')
    c.execute('DELETE FROM partidas;')
    
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
    c.execute('DELETE FROM equipos_jugadores;')
    c.execute('DELETE FROM equipos;')
    c.execute('DELETE FROM partidas;')
    c.execute('DELETE FROM jugadores;')
    
    # Habilitar las restricciones de claves foráneas nuevamente
    c.execute('PRAGMA foreign_keys = ON;')
    
    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()
    #clear_all_tables()
