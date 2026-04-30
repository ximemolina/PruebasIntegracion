# Laboratorio sobre pruebas de integración

Suite de pruebas de integración para el servicio `api-mongo` construido con FastAPI. Usa colecciones de Postman para pruebas manuales y Newman para ejecución automatizada desde la terminal.

---

## Estructura del Repositorio

```
PruebasIntegracion/
├── api-mongo/               # API FastAPI + MongoDB (ver su propio README)
└── postman/
    ├── collections/
    │   ├── orders.json
    │   ├── clients.json
    │   └── products.json
    └── environments/
        └── local.json       # Variables de entorno (URL base, etc.)
```

---

## Requisitos

- [Node.js](https://nodejs.org/) (para Newman)
- [Postman](https://www.postman.com/downloads/) (para pruebas manuales)
- El servidor `api-mongo` corriendo localmente

**Instalar Newman globalmente:**
```bash
npm install -g newman
```

---

## Levantar la API

Antes de correr cualquier prueba, asegurarse de que la API esté activa:
```bash
cd api-mongo
uv run python main.py
```

El servidor estará disponible en `http://localhost:8000`.

---

## Pruebas Manuales (Postman)

1. Abrir Postman
2. Importar las colecciones desde `postman/collections/`
3. Importar el entorno desde `postman/environments/local.json`
4. Seleccionar el entorno **local** en el menú desplegable superior derecho
5. Ejecutar requests individuales o usar el **Collection Runner**

---

## Pruebas Automatizadas (Newman)

Ejecutar cada colección contra el entorno local:

```bash
# Órdenes
newman run postman/collections/orders.json -e postman/environments/local.json

# Clientes
newman run postman/collections/clients.json -e postman/environments/local.json

# Productos
newman run postman/collections/products.json -e postman/environments/local.json
```

**Ejecutar todas a la vez:**
```bash
for collection in postman/collections/*.json; do
  newman run "$collection" -e postman/environments/local.json
done
```

**Generar reporte HTML:**
```bash
npm install -g newman-reporter-htmlextra

newman run postman/collections/orders.json \
  -e postman/environments/local.json \
  -r htmlextra --reporter-htmlextra-export reportes/orders.html
```

---

## Cobertura de Pruebas

| Recurso | Operaciones |
|---------|-------------|
| Órdenes | Crear, Leer, Actualizar, Eliminar |
| Clientes | Leer |
| Productos | Leer |

---

## Desarrollado por
- Susana Feng
- Ximena Molina
