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
            nombre TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            jugador1_id INTEGER,
            jugador2_id INTEGER,
            FOREIGN KEY(jugador1_id) REFERENCES jugadores(id),
            FOREIGN KEY(jugador2_id) REFERENCES jugadores(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            equipo1_id INTEGER,
            equipo2_id INTEGER,
            puntos_equipo1 INTEGER,
            puntos_equipo2 INTEGER,
            ganador_id INTEGER,
            FOREIGN KEY(equipo1_id) REFERENCES equipos(id),
            FOREIGN KEY(equipo2_id) REFERENCES equipos(id),
            FOREIGN KEY(ganador_id) REFERENCES equipos(id)
        )
    ''')
    conn.commit()
    conn.close()

# CRUD Operations
def add_jugador(nombre):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO jugadores (nombre) VALUES (?)', (nombre,))
    conn.commit()
    conn.close()

def get_jugadores():
    conn = get_connection()
    c = conn.cursor()
    jugadores = c.execute('SELECT id, nombre FROM jugadores').fetchall()
    conn.close()
    return jugadores

def add_equipo(nombre, jugador1_id, jugador2_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO equipos (nombre, jugador1_id, jugador2_id) VALUES (?, ?, ?)', (nombre, jugador1_id, jugador2_id))
    conn.commit()
    conn.close()

def get_equipos():
    conn = get_connection()
    c = conn.cursor()
    equipos = c.execute('SELECT id, nombre FROM equipos').fetchall()
    conn.close()
    return equipos

def add_partida(fecha, equipo1_id, equipo2_id, puntos1, puntos2, ganador_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO partidas (fecha, equipo1_id, equipo2_id, puntos_equipo1, puntos_equipo2, ganador_id) VALUES (?, ?, ?, ?, ?, ?)',
              (fecha, equipo1_id, equipo2_id, puntos1, puntos2, ganador_id))
    conn.commit()
    conn.close()

def get_partidas():
    conn = get_connection()
    c = conn.cursor()
    partidas = c.execute('SELECT * FROM partidas').fetchall()
    conn.close()
    return partidas
