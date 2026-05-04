import pytest
import sqlite3

@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(':memory:')
    conn.execute("PRAGMA foreign_keys = ON")   # activar desde el inicio
    cursor = conn.cursor()

    # Tabla clientes
    cursor.execute('''
        CREATE TABLE clientes (
            _id TEXT PRIMARY KEY,        -- ObjectId como string (24 hex)
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            genero TEXT NOT NULL,
            pais TEXT NOT NULL,
            creado TEXT,                 -- fecha ISO 8601
            -- preferencias se normaliza en tabla hija
            FOREIGN KEY (_id) REFERENCES clientes(_id)
        )
    ''')

    # Tabla hija para preferencias.canal (array de strings)
    cursor.execute('''
        CREATE TABLE clientes_canales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT NOT NULL,    -- referencia a clientes._id
            canal TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(_id)
        )
    ''')

    # Tabla productos
    cursor.execute('''
        CREATE TABLE productos (
            _id TEXT PRIMARY KEY,        -- ObjectId como string (24 hex)
            codigo_mongo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            codigo_alt TEXT NOT NULL,    -- requerido dentro de equivalencias
            sku TEXT                     -- opcional dentro de equivalencias
        )
    ''')

    # Tabla ordenes
    cursor.execute('''
        CREATE TABLE ordenes (
            _id TEXT PRIMARY KEY,
            cliente_id TEXT NOT NULL,
            fecha TEXT NOT NULL,
            canal TEXT NOT NULL,
            moneda TEXT NOT NULL,
            total INTEGER NOT NULL,
            cupon TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(_id)
        )
    ''')

    # Tabla orden_items (detalle de productos en cada orden)
    cursor.execute('''
        CREATE TABLE orden_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id TEXT NOT NULL,
            producto_id TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unit INTEGER NOT NULL,
            FOREIGN KEY (orden_id) REFERENCES ordenes(_id),
            FOREIGN KEY (producto_id) REFERENCES productos(_id)
        )
    ''')

    conn.commit()
    yield conn
    conn.close()