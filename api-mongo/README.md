# api-mongo

API REST construida con **FastAPI** y **MongoDB** para la gestión de órdenes, clientes y productos.

---

## Requisitos

- [uv](https://docs.astral.sh/uv/) (gestor de paquetes de Python)
- Python 3.12+
- Instancia de MongoDB (local o Atlas)

---

## Configuración


**1. Instalar dependencias:**
```bash
uv sync
```

**2. Crear un archivo `.env`** en la raíz del proyecto:
```env
MONGO_URI="mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB="mi_base_datos"
```

---

## Levantar el Servidor

**Desarrollo (con recarga automática):**
```bash
uv run python main.py
```

O con uvicorn directamente indicando el puerto:
```bash
uv run uvicorn main:app --reload --port 8000
```

El servidor inicia en `http://localhost:8000`

**Documentación interactiva de la API:** `http://localhost:8000/docs`

---

## Estructura del Proyecto

```
api-mongo/
├── main.py            # Punto de entrada de la app
├── config/
│   ├── __init__.py
│   └── database.py    # Configuración del cliente MongoDB
├── routers/
│   ├── __init__.py
│   ├── orders.py      # Endpoints de órdenes
│   ├── clients.py     # Endpoints de clientes
│   └── products.py    # Endpoints de productos
├── pyproject.toml
└── uv.lock
```

---

## Endpoints

Todas las rutas tienen el prefijo `/api/mongo`.

| Recurso | Método | Endpoint | Descripción |
|---------|--------|----------|-------------|
| Órdenes | GET | `/orders` | Listar todas las órdenes |
| Órdenes | GET | `/orders/{id}` | Listar una orden específica |
| Órdenes | POST | `/orders` | Crear una orden |
| Órdenes | PUT | `/orders/{id}` | Actualizar una orden |
| Órdenes | DELETE | `/orders/{id}` | Eliminar una orden |
| Clientes | GET | `/clients` | Listar todos los clientes |
| Clientes | GET | `/clients/{id}` | Listar un cliente específico |
| Productos | GET | `/products` | Listar todos los productos |
| Productos | GET | `/products/{id}` | Listar un producto específico |

---

## Dependencias

| Paquete | Uso |
|---------|-----|
| `fastapi[standard]` | Framework web + CLI + uvicorn |
| `pymongo` | Driver de MongoDB |
| `pydantic-settings` | Gestión de configuración via `.env` |
| `python-dotenv` | Carga del archivo `.env` |

---

