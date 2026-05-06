# Laboratorio sobre pruebas de integración

Suite de pruebas de integración para el servicio `api-mongo` construido con FastAPI. Usa colecciones de Postman y Pytest para pruebas manuales y Newman para ejecución automatizada desde la terminal.

---

## Estructura del repositorio

```
PruebasIntegracion/
├── api-mongo/                                        # API FastAPI + MongoDB (ver su propio README)
├── postman/
│   ├── Integración_API_Servicios.coleccion.json      # Colección de endpoints con sus pruebas
│   └── QA_API_LAB.postman_environment.json           # Ambiente de pruebas
└── tests/
    ├── test_api_integration.py
    └── conftest.py
```

---

## Prerequisitos

- [Node.js](https://nodejs.org/) — requerido para Newman
- [Postman](https://www.postman.com/downloads/) — para pruebas manuales
- Newman: `npm install -g newman` o usar `npx`
- El servidor `api-mongo` corriendo localmente

---

## Levantar la API

Antes de correr cualquier prueba, asegurarse de que la API esté activa:

```bash
cd api-mongo
uv run python main.py
```

El servidor estará disponible en `http://localhost:8000`.

---

## Pruebas manuales (Postman)

1. Abrir Postman
2. Importar la colección desde `postman/Integración_API_Servicios.coleccion.json`
3. Importar el entorno desde `postman/QA_API_LAB.postman_environment.json`
4. Seleccionar el entorno **QA_API_LAB** en el menú desplegable superior derecho
5. Ejecutar requests individuales o usar el **Collection Runner**

---

## Pruebas automatizadas (Newman)

Antes de ejecutar, rellenar los valores de `base_url`, `client_id` y `product_id` en el entorno de Postman o pasarlos directamente como variables:

```bash
npx newman run postman/Integración_API_Servicios.coleccion.json \
  -e postman/QA_API_LAB.postman_environment.json \
  --env-var "base_url=TU_BASE_URL" \
  --env-var "product_id=TU_PRODUCTO_ID" \
  --env-var "client_id=TU_CLIENTE_ID"
```

> `order_id` se obtiene automáticamente del flujo — no se requiere configuración manual.

### Cobertura

| Recurso | Operaciones |
|---------|-------------|
| Órdenes | Crear, Leer, Actualizar, Eliminar |
| Clientes | Leer |
| Productos | Leer |

---

## Mock server — simulación de proveedor externo caído

Para simular escenarios donde un proveedor externo no está disponible, se cuenta con un mock server en Postman que responde con `503 Service Unavailable` en todos los endpoints.

```
https://a42ea3d1-f9a9-46d3-84a3-096d4956c646.mock.pstmn.io
```

Ejemplos de uso:

```
GET https://a42ea3d1-f9a9-46d3-84a3-096d4956c646.mock.pstmn.io/clients/
GET https://a42ea3d1-f9a9-46d3-84a3-096d4956c646.mock.pstmn.io/orders/
GET https://a42ea3d1-f9a9-46d3-84a3-096d4956c646.mock.pstmn.io/products/
```

Todos los endpoints retornarán:

```json
{
  "error": "Service Unavailable",
  "message": "El proveedor externo no está disponible en este momento."
}
```

> El mock server es independiente del backend real — puede usarse sin necesidad de tener `api-mongo` corriendo localmente.

---

## Pruebas de integración (Pytest)

Las pruebas en `tests/` usan Pytest con una base de datos SQLite en memoria. Ver `tests/README.md` para el detalle de cada caso de prueba.

### Instalación

```bash
cd tests
uv init
uv venv
uv pip install pytest requests pymongo
```

### Ejecución

```bash
uv run pytest
uv run pytest -s    # Para ver los prints de cada test
```

---

## Desarrollado por

- Susana Feng
- Ximena Molina