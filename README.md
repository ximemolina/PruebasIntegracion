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


## Prerequisitos
- [Node.js](https://nodejs.org/) (para Newman)
- [Postman](https://www.postman.com/downloads/) (para pruebas manuales)
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

## Pruebas Manuales (Postman)

1. Abrir Postman
2. Importar las colecciones desde `postman/collections/`
3. Importar el entorno desde `postman/environments/local.json`
4. Seleccionar el entorno **local** en el menú desplegable superior derecho
5. Ejecutar requests individuales o usar el **Collection Runner**

---

## Pruebas Automatizadas (Newman)

Antes de ejecutar el comando, en el 'environment' de postman hay que rellenar los valores de 'base_url', 'client_id', 'product_id' y 'order_id'.

Ejecutar cada colección contra el entorno local:

```bash
npx newman run postman/Integración_API_Servicios.coleccion.json -e postman/QA_API_LAB.postman_environment.json --env-var "base_url=TU_BASE_URL" --env-var "product_id=TU_PRODUCTO_ID" --env-var "client_id=TU_CLIENTE_ID" --env-var "order_id=TU_ORDEN_ID"
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
