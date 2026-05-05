# 👤 Users Microservice - E-commerce Platform
Microservicio de usuarios para una plataforma tipo e-commerce (compradores y vendedores en un solo sistema).

Incluye:
- Registro de usuarios
- Login
- Consulta de usuarios
- Base de datos MySQL
- Dockerizado
- Seed de 20,000 usuarios

---

# 🚀 Tecnologías

- Python 3.10+
- FastAPI
- MySQL 8
- SQLAlchemy
- Docker + Docker Compose
- Faker (para datos fake)

---

# 📦 Estructura del proyecto

- app/
  - crud.py
  - database.py
  - main.py
  - models.py
  - schemas.py
- seed_users.py
- Dockerfile
- docker-compose.yml
- requirements.txt

---

# ⚙️ Requisitos previos

Antes de ejecutar:

- Tener instalado:
  - Docker Desktop
  - Python 3.10+
  - Git

---

# 🐳 1. Levantar el proyecto con Docker

En la raíz del proyecto ejecutar:

```bash
docker-compose up --build
```

Esto levantará:
- API Users → http://localhost:8000
- MySQL → puerto 3307 (local)

---

# 🌐 2. Acceder a la API

Swagger UI:
```bash
http://localhost:8000/docs
```

OpenAPI:
```bash
http://localhost:8000/openapi.json
```

---
# 📌 3. Endpoints disponibles

- Auth
  - Registrar usuario
    ```bash
    POST /auth/register
    ```
    ```bash
    {
    "name": "Juan Perez",
    "email": "juan@gmail.com",
    "password": "123456"
    }
    ```
  - Login usuario
    ```bash
    POST /auth/login
    ```
    ```bash
    {
    "email": "juan@gmail.com",
    "password": "123456"
    }
    ```
- Usuarios
  - Obtener usuario por ID
    ```bash
    GET /users/{id}
    ```
    ```bash
    Por ejemplo:
    GET /users/1
    ```
  -  Listar usuarios
    ```bash
    GET /users
    ```
    
---

# 🧪 4. Insertar datos de prueba (20,000 usuarios)
Este script genera usuarios fake para pruebas y Data Science.
Docker debe estar corriendo antes.

- Ejecutar seed:
  ```bash
  python seed_users.py
  ```
  El resultado:
  ```bash
  0 usuarios insertados...
  1000 usuarios insertados...
  ...
  20000 usuarios insertados...
  ```

--- 

# 🐬 5. Base de datos (MySQL)

Configuración Docker:
- Host interno Docker: mysql
- Puerto local: 3307
- Base de datos: usersdb
- Usuario: root
- Password: root

Conexión desde otros microservicios:
Cuando se integren servicios dentro de Docker
```bash
http://users:8000
```
Conexión local (fuera de Docker):
```bash
http://localhost:8000
```

---

# 🐳 6. Docker - Reinicio del proyecto

Si apagas la laptop:
- Volver a levantar:
  ```bash
  docker-compose up
  ```
- Detener servicios:
  ```bash
  docker-compose down
  ```
⚠️ IMPORTANTE
NO usar: docker-compose down -v
Porque elimina la base de datos y los 20,000 usuarios.

---

# 📂 7. Variables de entorno
Crear archivo .env (si se requiere):
```bash
DATABASE_URL=mysql+pymysql://root:root@mysql:3306/usersdb
```
