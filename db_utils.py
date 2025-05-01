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
    
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS equipos (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL,
    #         jugador1_id INTEGER,
    #         jugador2_id INTEGER,
    #         FOREIGN KEY(jugador1_id) REFERENCES jugadores(id),
    #         FOREIGN KEY(jugador2_id) REFERENCES jugadores(id)
    #     )
    # ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            p1_t1 TEXT,
            p2_t1 TEXT,
            p1_t2 TEXT,
            p2_t2 TEXT,
            puntos_equipo1 INTEGER,
            puntos_equipo2 INTEGER,
            ganador TEXT
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

def update_player():
    pass

def get_jugadores():
    conn = get_connection()
    c = conn.cursor()
    jugadores = c.execute('SELECT id, name FROM jugadores').fetchall()
    conn.close()
    return jugadores

def add_equipo(name, jugador1_id, jugador2_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO equipos (name, jugador1_id, jugador2_id) VALUES (?, ?, ?)', (name, jugador1_id, jugador2_id))
    conn.commit()
    conn.close()

def get_equipos():
    conn = get_connection()
    c = conn.cursor()
    equipos = c.execute('SELECT id, name FROM equipos').fetchall()
    conn.close()
    return equipos

def add_partida(fecha, p1_t1, p2_t1, p1_t2, p2_t2, puntos1, puntos2, ganador):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO partidas (fecha, p1_t1, p2_t1, p1_t2, p2_t2, puntos_equipo1, puntos_equipo2, ganador) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (fecha, p1_t1, p2_t1, p1_t2, p2_t2, puntos1, puntos2, ganador))
    conn.commit()
    conn.close()

def get_partidas():
    conn = get_connection()
    c = conn.cursor()
    partidas = c.execute('SELECT * FROM partidas').fetchall()
    conn.close()
    return partidas

if __name__ == "__main__":
    create_tables()
    print(get_jugadores())
    print(len(get_jugadores()))
    print(type(get_jugadores()))