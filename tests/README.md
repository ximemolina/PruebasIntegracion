# Pruebas de integración — tests/

Documentación de los casos de prueba en `test_api_integration.py`. Las pruebas usan Pytest y una base de datos SQLite en memoria que se crea y destruye en cada ejecución.

---

## Casos de prueba

### 1. `test_consultar_productos`

Hace un `GET /products` a la API y valida que la respuesta tenga la estructura correcta. Verifica que `data` sea una lista no vacía y que cada producto contenga los campos `_id`, `codigo_mongo`, `nombre`, `categoria` y `equivalencias`.

No depende de la base de datos local — es una prueba directa contra la API.

---

### 2. `test_insertar_producto`

Consulta un producto y un cliente desde la API, los inserta en las tablas SQLite y crea una orden con un item asociado. Al final valida que todas las inserciones hayan quedado correctamente registradas.

Este test inicializa el estado que usan los tests siguientes a través de las variables globales `ORDEN_ID`, `PRODUCT_ID`, `PRECIO` y `CANTIDAD`.

---

### 3. `test_validar_total_cantidad_precio`

Recupera la orden creada en el test anterior y verifica que el total guardado coincida con `cantidad × precio_unit`. Valida que los valores sean exactamente los que se ingresaron al insertar.

---

### 4. `test_validar_reglas_de_negocio`

Recorre todas las órdenes en la tabla y por cada una verifica que:

- La cantidad sea mayor a cero
- El precio unitario sea mayor a cero
- El producto referenciado exista en la tabla `productos`
- El total coincida con la suma de `cantidad × precio_unit` de sus items

---

### 5. `test_no_insertar_item_con_producto_inexistente`

Intenta insertar un item referenciando un `producto_id` que no existe en la tabla `productos`. Espera que SQLite lance un `IntegrityError` por la restricción de llave foránea y verifica que no haya quedado ningún registro inválido.

---

### 6. `test_tiempo_respuesta_api`

Mide el tiempo que tarda la API en responder a `GET /products`. Valida que el status code sea `200` y que la respuesta llegue en menos de 1 segundo.

---

### 7. Contrato de datos

Cinco tests que recorren cada tabla en SQLite y verifican que los tipos de dato de cada columna sean los correctos. Si la API empieza a devolver un campo con un tipo distinto al esperado, estos tests lo detectan.

| Test | Tabla | Campos validados |
|------|-------|-----------------|
| `test_contrato_clientes` | `clientes` | `_id`, `nombre`, `email`, `genero`, `pais`, `creado` |
| `test_contrato_clientes_canales` | `clientes_canales` | `id`, `cliente_id`, `canal` |
| `test_contrato_productos` | `productos` | `_id`, `codigo_mongo`, `nombre`, `categoria`, `codigo_alt`, `sku` |
| `test_contrato_ordenes` | `ordenes` | `_id`, `cliente_id`, `fecha`, `canal`, `moneda`, `total`, `cupon` |
| `test_contrato_orden_items` | `orden_items` | `id`, `orden_id`, `producto_id`, `cantidad`, `precio_unit` |

---

### 8. `test_idempotencia_ordenes_duplicadas`

Crea dos órdenes con los mismos datos de negocio y verifica que ambas se registren sin conflicto, ya que cada una recibe un `_id` único generado con `ObjectId`. Confirma también que los items de cada orden tengan los valores correctos.

---

### 9. `test_manejo_errores_body_invalido`

Envía requests con bodies inválidos al endpoint `POST /orders` y documenta el `status_code` y el mensaje de error que retorna la API en cada caso. Los casos probados son:

- Body vacío `{}`
- Falta `cliente_id`
- Cantidad negativa en un item
- Tipo incorrecto (`cantidad` como string)
- `cliente_id` inexistente
- Lista de items vacía
- Body que no es JSON

El objetivo es documentar el comportamiento actual de la API ante inputs inválidos, no imponer códigos de error específicos.

---

### 10. `test_integracion_parcial_api_ok_db_falla`

Verifica qué ocurre cuando la API responde correctamente pero la base de datos no está disponible. Simula el fallo cerrando la conexión SQLite e intenta una inserción para capturar el error. Al final verifica que la API siga respondiendo aunque la DB haya fallado.

Comportamiento esperado en producción:
- La API debería retornar `503`, no `200`
- La transacción no debería quedar en estado inconsistente
- El error debería quedar registrado en logs
- El cliente debería poder reintentar de forma segura

Riesgo identificado: si la API retorna `200` antes de confirmar la escritura en DB, el cliente asume éxito pero la orden se pierde.

---

## Notas

- Los tests se ejecutan en orden secuencial. `test_insertar_producto` debe correr antes que los tests de validación de totales, reglas de negocio e idempotencia, ya que estos dependen del estado que ese test inicializa.
- La base de datos SQLite se crea en memoria para cada ejecución — no persiste entre corridas.
- Los tests de contrato y el de tiempo de respuesta son independientes y pueden correr en cualquier orden siempre que la API esté activa.