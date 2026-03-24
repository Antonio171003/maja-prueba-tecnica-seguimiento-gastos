# Maja — Seguimiento de Gastos

## Candidato: Luis Antonio Peñuelas López

Aplicación para el control financiero personal. Se busca evaluar el manejo de datos numéricos y consultas con filtros.

## Stack

**Backend:** Python · Flask · SQLAlchemy · PostgreSQL · Flask-Migrate  
**Frontend:** Angular 19 · Angular Material  
**Infraestructura:** Docker · Docker Compose · Nginx  

## Funcionalidades

- CRUD de gastos y categorías
- Filtros combinables: fecha, categoría, rango de monto, ordenamiento
- Paginación de resultados
- Resumen con total y desglose por categoría
- Validaciones en backend con errores descriptivos
- Manejo de errores global (400, 404, 422, 500)

## Requisitos

- Docker y Docker Compose

## Instalación y ejecución
```bash
# 1. Clonar el repositorio
git clone git@github.com:Antonio171003/maja-prueba-tecnica-seguimiento-gastos.git
cd maja-prueba-tecnica-seguimiento-gastos

# 2. Levantar los servicios
docker compose up --build
```

La app queda disponible en:
- **Frontend:** http://localhost:4200
- **Backend:** http://localhost:5000

> Los datos de ejemplo se cargan automáticamente al iniciar.

## Desarrollo local (sin Docker)

> Solo necesario si no se usa Docker.

**Backend:**
```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar base de datos
flask --app run db upgrade

# Correr servidor
flask --app run run
```

**Frontend:**
```bash
cd web
npm install
ng serve
```

## API

### Categorías

- `GET /categories` — Lista todas las categorías
- `POST /categories` — Crea una categoría
- `PUT /categories/:id` — Actualiza una categoría
- `DELETE /categories/:id` — Elimina una categoría (falla si tiene gastos asociados)

### Gastos

- `GET /expenses` — Lista gastos con soporte de filtros y paginación
- `POST /expenses` — Crea un gasto
- `PUT /expenses/:id` — Actualiza un gasto
- `DELETE /expenses/:id` — Elimina un gasto
- `GET /expenses/summary` — Devuelve el total general y el desglose por categoría

### Filtros de `GET /expenses`

Todos los parámetros son opcionales y combinables entre sí.

- `category_id` — Filtra por categoría
- `start_date` / `end_date` — Rango de fechas en formato `YYYY-MM-DD`
- `min_amount` / `max_amount` — Rango de monto
- `sort` — Ordenamiento: `date_asc`, `date_desc`, `amount_asc`, `amount_desc`
- `page` / `limit` — Paginación de resultados

**Ejemplo:**
```
GET /expenses?category_id=1&start_date=2026-03-01&sort=amount_desc&page=1&limit=10
```

## Tests
```bash
cd server
pytest tests/ -v
```

67 tests cubriendo servicios, rutas y casos de error.
