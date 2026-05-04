import requests
import sqlite3
from datetime import datetime
from bson import ObjectId
import pytest
import time

BASE_URL = "http://localhost:8000"  
ORDEN_ID = ""
PRECIO = 0
CANTIDAD = 0
PRODUCT_ID = ""

import requests

def test_consultar_productos():
    print(f"\n🔍 Test de consulta HTTP a la API de productos")

    response = requests.get(f"{BASE_URL}/products", timeout=10)
    assert response.status_code == 200, "❌ El API no respondió con 200 OK"
    print("✅ El API respondió con 200 OK")

    body = response.json()
    assert "data" in body, "❌ La respuesta no contiene la clave 'data'"
    print("✅ La respuesta contiene la clave 'data'")

    assert isinstance(body["data"], list), "❌ 'data' no es una lista"
    print("✅ 'data' es una lista")

    assert len(body["data"]) > 0, "❌ La lista 'data' está vacía"
    print("✅ La lista 'data' contiene elementos")

    product = body["data"][0]
    print(f"🔍 Validando producto con _id: {product.get('_id')}")

    # Validaciones según tu validator de productos
    assert "_id" in product and isinstance(product["_id"], str), "❌ '_id' debe existir y ser string"
    print("✅ '_id' existe y es string")

    assert "codigo_mongo" in product and isinstance(product["codigo_mongo"], str), "❌ 'codigo_mongo' debe existir y ser string"
    print("✅ 'codigo_mongo' existe y es string")

    assert "nombre" in product and isinstance(product["nombre"], str), "❌ 'nombre' debe existir y ser string"
    print("✅ 'nombre' existe y es string")

    assert "categoria" in product and isinstance(product["categoria"], str), "❌ 'categoria' debe existir y ser string"
    print("✅ 'categoria' existe y es string")

    assert "equivalencias" in product and isinstance(product["equivalencias"], dict), "❌ 'equivalencias' debe existir y ser dict"
    print("✅ 'equivalencias' existe y es dict")

    assert "codigo_alt" in product["equivalencias"], "❌ 'codigo_alt' debe existir en equivalencias"
    assert isinstance(product["equivalencias"]["codigo_alt"], str), "❌ 'codigo_alt' debe ser string"
    print("✅ 'codigo_alt' existe y es string")

    if "sku" in product["equivalencias"]:
        assert isinstance(product["equivalencias"]["sku"], str), "❌ 'sku' debe ser string si existe"
        print("✅ 'sku' existe y es string")

    print("🎉 Todas las validaciones de producto pasaron correctamente")

# Insertar un producto para crear una orden
def test_insertar_producto(db_connection):
    conn = db_connection
    cursor = conn.cursor()

    print("-----------------------------------------------------------------------------------------------------")
    print()
    print("🔍 Insertar un producto para crear una orden")

    # 1. Consultar producto desde tu API
    response = requests.get(f"{BASE_URL}/products", timeout=10)
    assert response.status_code == 200, "❌ Error: API productos no respondió con 200"
    print("✅ API productos respondió con 200 OK")

    body = response.json()
    assert "data" in body and len(body["data"]) > 0, "❌ Error: 'data' vacío en productos"
    print("✅ API productos devolvió lista con datos")

    producto = body["data"][0]
    print(f"✅ Producto consultado: {producto['_id']} - {producto['nombre']}")

    # 2. Consultar cliente desde tu API
    response = requests.get(f"{BASE_URL}/clients", timeout=10)
    assert response.status_code == 200, "❌ Error: API clientes no respondió con 200"
    print("✅ API clientes respondió con 200 OK")

    body = response.json()
    assert "data" in body and len(body["data"]) > 0, "❌ Error: 'data' vacío en clientes"
    print("✅ API clientes devolvió lista con datos")

    cliente = body["data"][0]
    print(f"✅ Cliente consultado: {cliente['_id']} - {cliente['nombre']}")

    # 3. Insertar producto en la tabla productos
    cursor.execute("""
        INSERT INTO productos (_id, codigo_mongo, nombre, categoria, codigo_alt, sku)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        producto["_id"],
        producto["codigo_mongo"],
        producto["nombre"],
        producto["categoria"],
        producto["equivalencias"]["codigo_alt"],
        producto["equivalencias"].get("sku")
    ))
    conn.commit()
    print("✅ Producto insertado en tabla productos")

    # 4. Insertar cliente en tabla clientes
    cursor.execute("""
        INSERT INTO clientes (_id, nombre, email, genero, pais, creado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        cliente["_id"],
        cliente["nombre"],
        cliente["email"],
        cliente["genero"],
        cliente["pais"],
        cliente.get("creado")
    ))
    print("✅ Cliente insertado en tabla clientes")

    # 5. Insertar canales de preferencias en tabla clientes_canales
    if "preferencias" in cliente and "canal" in cliente["preferencias"]:
        for canal in cliente["preferencias"]["canal"]:
            cursor.execute("""
                INSERT INTO clientes_canales (cliente_id, canal)
                VALUES (?, ?)
            """, (cliente["_id"], canal))
        print("✅ Canales de preferencias insertados en tabla clientes_canales")

    # 6. Crear orden usando cliente y producto
    global ORDEN_ID, CANTIDAD, PRECIO, PRODUCT_ID
    orden_id = str(ObjectId())
    ORDEN_ID = orden_id
    fecha = datetime.now().isoformat()
    canal = "WEB"
    moneda = "CRC"
    cantidad = 5
    CANTIDAD = cantidad
    precio_unit = 1500
    PRECIO = precio_unit
    total = cantidad * precio_unit
    cupon = ""

    PRODUCT_ID = producto["_id"]

    cursor.execute("""
        INSERT INTO ordenes (_id, cliente_id, fecha, canal, moneda, total, cupon)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        orden_id,
        cliente["_id"],
        fecha,
        canal,
        moneda,
        total,
        cupon
    ))
    print("✅ Orden insertada en tabla ordenes")

    cursor.execute("""
        INSERT INTO orden_items (orden_id, producto_id, cantidad, precio_unit)
        VALUES (?, ?, ?, ?)
    """, (
        orden_id,
        producto["_id"],
        cantidad,
        precio_unit
    ))
    conn.commit()
    print("✅ Item insertado en tabla orden_items")

    # 7. Validar inserciones
    cursor.execute("SELECT * FROM productos WHERE _id=?", (producto["_id"],))
    prod_row = cursor.fetchone()
    assert prod_row is not None, "❌ Producto no se insertó correctamente"
    print("✅ Validación producto insertado correctamente")

    cursor.execute("SELECT * FROM clientes WHERE _id=?", (cliente["_id"],))
    prod_row = cursor.fetchone()
    assert prod_row is not None, "❌ Cliente no se insertó correctamente"
    print("✅ Validación cliente insertado correctamente")

    cursor.execute("SELECT * FROM clientes_canales WHERE cliente_id=?", (cliente["_id"],))
    prod_row = cursor.fetchone()
    assert prod_row is not None, "❌ Canales de cliente no se insertaron correctamente"
    print("✅ Validación canales insertados correctamente")

    cursor.execute("SELECT * FROM ordenes WHERE _id=?", (orden_id,))
    orden_row = cursor.fetchone()
    assert orden_row is not None, "❌ Orden no se insertó correctamente"
    assert orden_row[1] == cliente["_id"], "❌ cliente_id en orden incorrecto"
    assert orden_row[5] == total, "❌ total en orden incorrecto"
    print("✅ Validación orden insertada correctamente")

    cursor.execute("SELECT * FROM orden_items WHERE orden_id=?", (orden_id,))
    items = cursor.fetchall()
    assert len(items) == 1, "❌ No se insertó item en orden_items"
    assert items[0][2] == producto["_id"], "❌ producto_id en item incorrecto"
    assert items[0][3] == cantidad, "❌ cantidad en item incorrecta"
    assert items[0][4] == precio_unit, "❌ precio_unit en item incorrecto"
    print("✅ Validación item insertado correctamente")

    print("🎉 Todas las validaciones pasaron correctamente")

# Validar total de cantidades coincida con lo insertado
def test_validar_total_cantidad_precio(db_connection):
    conn = db_connection
    cursor = conn.cursor()

    print("-----------------------------------------------------------------------------------------------------")
    print()
    print("🔍 Validar que el total de cantidades coincida con lo insertado")

    # 1. Seleccionar una orden existente
    cursor.execute("SELECT _id, total FROM ordenes LIMIT 1")
    orden = cursor.fetchone()
    assert orden is not None, "❌ No se encontró ninguna orden en la tabla"
    print("✅ Se encontró una orden en la tabla ordenes")

    orden_id, total_guardado = orden
    print(f"🔍 Orden seleccionada: {orden_id} con total guardado {total_guardado}")

    # 2. Seleccionar fila de orden_items
    cursor.execute("SELECT cantidad, precio_unit FROM orden_items WHERE orden_id=?", (orden_id,))
    orden_item = cursor.fetchone()
    assert orden_item is not None, f"❌ No se encontró item asociado a la orden {orden_id}"
    print(f"✅ Se encontró item asociado a la orden {orden_id}")

    cantidad, precio_unit = orden_item
    print(f"🔍 Item recuperado: cantidad={cantidad}, precio_unit={precio_unit}")

    # 3. Validar que las cantidades hayan sido las ingresadas al insertar la orden
    assert cantidad == CANTIDAD, f"❌ La cantidad {cantidad} no coincide con la esperada {CANTIDAD}"
    print("✅ La cantidad coincide con la esperada")

    assert precio_unit == PRECIO, f"❌ El precio_unit {precio_unit} no coincide con el esperado {PRECIO}"
    print("✅ El precio_unit coincide con el esperado")

    assert total_guardado == CANTIDAD * PRECIO, f"❌ El total guardado {total_guardado} no coincide con el cálculo {CANTIDAD * PRECIO}"
    print("✅ El total guardado coincide con la suma cantidad × precio_unit")

    print("🎉 Todas las validaciones de la orden pasaron correctamente")


# Validar cantidades de acuerdo con las reglas del negocio (que haya disponible, que existan, que no sean negativos, etc) 
def test_validar_reglas_de_negocio(db_connection):
    conn = db_connection
    cursor = conn.cursor()

    print("-----------------------------------------------------------------------------------------------------")
    print()
    print("🔍 Validar cantidades de acuerdo con las reglas del negocio")

    # 1. Seleccionar todas las órdenes
    cursor.execute("SELECT _id, total FROM ordenes")
    ordenes = cursor.fetchall()
    assert len(ordenes) > 0, "❌ No se encontraron órdenes en la tabla"
    print(f"✅ Se encontraron {len(ordenes)} órdenes en la tabla")

    for orden_id, total_guardado in ordenes:
        print(f"\n🔍 Validando orden {orden_id} con total guardado {total_guardado}")

        # 2. Obtener los items de cada orden
        cursor.execute("""
            SELECT producto_id, cantidad, precio_unit
            FROM orden_items
            WHERE orden_id=?
        """, (orden_id,))
        items = cursor.fetchall()
        assert len(items) > 0, f"❌ La orden {orden_id} no tiene items asociados"
        print(f"✅ La orden {orden_id} tiene {len(items)} items asociados")

        total_calculado = 0

        for producto_id, cantidad, precio_unit in items:
            print(f"🔍 Validando item con producto {producto_id}, cantidad={cantidad}, precio_unit={precio_unit}")

            # 3. Validar reglas de negocio
            assert cantidad > 0, f"❌ Cantidad inválida en orden {orden_id}"
            print("✅ Cantidad positiva")

            assert precio_unit > 0, f"❌ Precio inválido en orden {orden_id}"
            print("✅ Precio positivo")

            # El producto debe existir en la tabla productos
            cursor.execute("SELECT 1 FROM productos WHERE _id=?", (producto_id,))
            assert cursor.fetchone() is not None, f"❌ Producto {producto_id} no existe"
            print("✅ Producto existe en la tabla productos")

            # Acumular total
            total_calculado += cantidad * precio_unit

        # 4. Validar que el total de la orden coincide con la suma de sus items
        assert total_guardado == total_calculado, (
            f"❌ Total inconsistente en orden {orden_id}: "
            f"guardado={total_guardado}, calculado={total_calculado}"
        )
        print(f"✅ Total consistente en orden {orden_id}: guardado={total_guardado}, calculado={total_calculado}")

    print("\n🎉 Todas las validaciones de reglas de negocio pasaron correctamente")

# Validar el ingreso de un producto que no existe 
def test_no_insertar_item_con_producto_inexistente(db_connection):
    conn = db_connection
    cursor = conn.cursor()
    global ORDEN_ID, PRODUCT_ID

    print("-----------------------------------------------------------------------------------------------------")
    print()
    print("🔍 Validar el ingreso de un producto que no existe")

    # 1. Intentar insertar un item con producto inexistente
    producto_id_inexistente = "noexiste1234567890abcd"
    print(f"🚨 Intentando insertar item con producto inexistente: {producto_id_inexistente}")

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO orden_items (orden_id, producto_id, cantidad, precio_unit)
            VALUES (?, ?, ?, ?)
        """, (
            ORDEN_ID, producto_id_inexistente, 2, 500
        ))
        conn.commit()
    print("✅ Se lanzó IntegrityError como se esperaba (producto inexistente no permitido)")

    # 3. Validar que no se insertó nada en orden_items
    cursor.execute("SELECT * FROM orden_items WHERE orden_id=? and producto_id=?", (ORDEN_ID, producto_id_inexistente,))
    items = cursor.fetchall()
    print(f"🔍 Items encontrados para la orden {ORDEN_ID} y producto {producto_id_inexistente}: {items}")

    assert len(items) == 0, "❌ No debería haber items asociados a un producto inexistente"
    print("✅ Validación final: no se insertaron items inválidos")

    print("🎉 Todas las validaciones de producto inexistente pasaron correctamente")

# Medir tiempo de respuesta
def test_tiempo_respuesta_api():
    print("-----------------------------------------------------------------------------------------------------")
    print(f"\nTiempo de respuesta del API: {BASE_URL}/products")

    inicio = time.perf_counter()
    response = requests.get(f"{BASE_URL}/products")
    fin = time.perf_counter()

    duracion = fin - inicio
    print(f"⏱️ Tiempo de respuesta: {duracion:.3f} segundos")

    # Validaciones
    assert response.status_code == 200, "❌ El API no respondió con 200 OK"
    print("✅ Status code 200 OK")

    # Ejemplo: validar que el tiempo sea menor a 1 segundo
    assert duracion < 1.0, f"❌ El API tardó demasiado: {duracion:.3f} segundos, límite (<1s)"
    print("✅ Tiempo de respuesta dentro del límite (<1s)")

# Pruebas de contrato estricta
def test_contrato_clientes(db_connection):
    print("-----------------------------------------------------------------------------------------------------")
    print(f"\nPruebas de contrato estricta: clientes")
    conn = db_connection
    cursor = conn.cursor()

    cursor.execute("SELECT _id, nombre, email, genero, pais, creado FROM clientes")
    clientes = cursor.fetchall()

    for _id, nombre, email, genero, pais, creado in clientes:
        print(f"🔍 Validando cliente {_id}")
        assert isinstance(_id, str), "❌ _id debe ser string (ObjectId)"
        assert isinstance(nombre, str), "❌ nombre debe ser string"
        assert isinstance(email, str), "❌ email debe ser string"
        assert isinstance(genero, str), "❌ genero debe ser string"
        assert isinstance(pais, str), "❌ pais debe ser string"
        assert isinstance(creado, (str, type(None))), "❌ creado debe ser string ISO8601 o null"
        print(f"✅ Cliente {_id} cumple contrato")

def test_contrato_clientes_canales(db_connection):
    print("-----------------------------------------------------------------------------------------------------")
    print(f"\nPruebas de contrato estricta: clientes_canales")
    conn = db_connection
    cursor = conn.cursor()

    cursor.execute("SELECT id, cliente_id, canal FROM clientes_canales")
    canales = cursor.fetchall()

    for id_, cliente_id, canal in canales:
        print(f"🔍 Validando canal {canal} del cliente {cliente_id}")
        assert isinstance(id_, int), "❌ id debe ser entero"
        assert isinstance(cliente_id, str), "❌ cliente_id debe ser string"
        assert isinstance(canal, str), "❌ canal debe ser string"
        print(f"✅ Canal {canal} del cliente {cliente_id} cumple contrato")

def test_contrato_productos(db_connection):
    print("-----------------------------------------------------------------------------------------------------")
    print(f"\nPruebas de contrato estricta: productos")
    conn = db_connection
    cursor = conn.cursor()

    cursor.execute("SELECT _id, codigo_mongo, nombre, categoria, codigo_alt, sku FROM productos")
    productos = cursor.fetchall()

    for _id, codigo_mongo, nombre, categoria, codigo_alt, sku in productos:
        print(f"🔍 Validando producto {_id}")
        assert isinstance(_id, str), "❌ _id debe ser string (ObjectId)"
        assert isinstance(codigo_mongo, str), "❌ codigo_mongo debe ser string"
        assert isinstance(nombre, str), "❌ nombre debe ser string"
        assert isinstance(categoria, str), "❌ categoria debe ser string"
        assert isinstance(codigo_alt, str), "❌ codigo_alt debe ser string"
        assert isinstance(sku, (str, type(None))), "❌ sku debe ser string o null"
        print(f"✅ Producto {_id} cumple contrato")

def test_contrato_ordenes(db_connection):
    print("-----------------------------------------------------------------------------------------------------")
    print(f"\nPruebas de contrato estricta: ordenes")
    conn = db_connection
    cursor = conn.cursor()

    cursor.execute("SELECT _id, cliente_id, fecha, canal, moneda, total, cupon FROM ordenes")
    ordenes = cursor.fetchall()

    for _id, cliente_id, fecha, canal, moneda, total, cupon in ordenes:
        print(f"🔍 Validando orden {_id}")
        assert isinstance(_id, str), "❌ _id debe ser string (ObjectId)"
        assert isinstance(cliente_id, str), "❌ cliente_id debe ser string"
        assert isinstance(fecha, str), "❌ fecha debe ser string ISO8601"
        assert isinstance(canal, str), "❌ canal debe ser string"
        assert isinstance(moneda, str), "❌ moneda debe ser string"
        assert isinstance(total, int), "❌ total debe ser entero"
        assert isinstance(cupon, (str, type(None))), "❌ cupon debe ser string o null"
        print(f"✅ Orden {_id} cumple contrato")

def test_contrato_orden_items(db_connection):
    print("-----------------------------------------------------------------------------------------------------")
    print(f"\nPruebas de contrato estricta: orden_items")
    conn = db_connection
    cursor = conn.cursor()

    cursor.execute("SELECT id, orden_id, producto_id, cantidad, precio_unit FROM orden_items")
    items = cursor.fetchall()

    for id_, orden_id, producto_id, cantidad, precio_unit in items:
        print(f"🔍 Validando item {id_} de orden {orden_id}")
        assert isinstance(id_, int), "❌ id debe ser entero"
        assert isinstance(orden_id, str), "❌ orden_id debe ser string"
        assert isinstance(producto_id, str), "❌ producto_id debe ser string"
        assert isinstance(cantidad, int), "❌ cantidad debe ser entero"
        assert isinstance(precio_unit, int), "❌ precio_unit debe ser entero"
        print(f"✅ Item {id_} de orden {orden_id} cumple contrato")