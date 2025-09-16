# API de Destinos Turísticos 🌎

API desarrollada en FastAPI para una plataforma de venta de destinos turísticos con sistema de puntos.

## Características

- **Gestión de usuarios**: Registro y administración de usuarios
- **Catálogo de destinos**: CRUD completo de destinos turísticos
- **Sistema de compras**: Compra de paquetes turísticos
- **Sistema de puntos**: Los usuarios ganan puntos con cada compra
- **Canje de puntos**: Conversión de puntos en descuentos (1 punto = $0.10)

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno (copiar .env.example a .env):
```bash
cp .env.example .env
```

3. Poblar base de datos con datos de ejemplo:
```bash
python poblar_bd.py
```

4. Ejecutar la aplicación:
```bash
python main.py
```

## Uso

La API estará disponible en: http://localhost:8000

- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc

## Endpoints Principales

### Usuarios
- `POST /api/v1/usuarios/` - Crear usuario
- `GET /api/v1/usuarios/` - Listar usuarios
- `GET /api/v1/usuarios/{id}` - Obtener usuario con compras y canjes
- `GET /api/v1/usuarios/{id}/estadisticas` - Estadísticas del usuario

### Destinos
- `POST /api/v1/destinos/` - Crear destino
- `GET /api/v1/destinos/` - Listar destinos disponibles
- `GET /api/v1/destinos/{id}` - Obtener destino específico

### Compras
- `POST /api/v1/compras/` - Realizar compra
- `GET /api/v1/compras/usuario/{id}` - Compras de un usuario

### Sistema de Puntos
- `POST /api/v1/puntos/canjear/` - Canjear puntos por descuento
- `GET /api/v1/puntos/usuario/{id}/canjes` - Canjes de un usuario
- `GET /api/v1/puntos/usuario/{id}/saldo` - Saldo de puntos

## Estructura del Proyecto

```
├── app/
│   ├── api/           # Endpoints de la API
│   ├── crud/          # Operaciones de base de datos
│   ├── db/            # Configuración de base de datos
│   ├── models/        # Modelos SQLAlchemy
│   └── schemas/       # Esquemas Pydantic
├── main.py           # Aplicación principal
├── poblar_bd.py      # Script para poblar BD
└── requirements.txt  # Dependencias
```

---
*Segundo curso integrador de software - UTP*
