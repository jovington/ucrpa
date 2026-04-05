Aquí tienes el contenido organizado en un archivo Markdown (`.md`) listo para copiar y usar en **Antigravity** o cualquier gestor de documentación. He consolidado toda la arquitectura, el código y la estrategia de seguridad que hemos diseñado.

---

# 📑 Documentación de Infraestructura Web: FastAPI + Vue.js + MongoDB

Esta documentación detalla la configuración de una infraestructura de contenedores aislada, segura y persistente para el despliegue de una aplicación web con manejo de documentos PDF.

## 🏗️ Arquitectura del Sistema
La solución utiliza **Docker Compose** para orquestar 5 servicios principales en una red privada, exponiendo únicamente el tráfico cifrado a través de un Reverse Proxy.

* **Frontend:** Vue.js (Servido por Nginx).
* **Backend:** FastAPI (Python 3.12).
* **Base de Datos:** MongoDB (NoSQL).
* **Admin DB:** Mongo Express (Interfaz visual).
* **Gateway:** Nginx Proxy Manager (Gestión de SSL y Dominios).

---

## 📁 Estructura de Carpetas
Para garantizar la persistencia de los datos y el aislamiento del código, se debe seguir esta jerarquía:

```text
proyecto-root/
├── docker-compose.yml           # Orquestador principal
├── .env                         # Secretos y credenciales
├── app/
│   ├── api/                     # Código FastAPI + Dockerfile
│   └── web/                     # Código Vue.js + Dockerfile
├── infra/
│   ├── proxy_data/              # Configuración del Proxy (Auto)
│   └── letsencrypt/             # Certificados SSL (Auto)
└── storage/
    ├── documents/               # ALMACENAMIENTO DE PDFs
    └── mongodb_data/            # Datos de la DB
```

---

## 🚀 Configuración de Docker

### 1. Variables de Entorno (`.env`)
Crea este archivo en la raíz para centralizar la seguridad:
```env
MONGO_USER=admin_db
MONGO_PASSWORD=tu_clave_segura_2026
```

### 2. Orquestador (`docker-compose.yml`)
```yaml
services:
  # Gateway de entrada con SSL
  proxy:
    image: 'jc21/nginx-proxy-manager:latest'
    container_name: app_gateway
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'   # Panel Admin
      - '443:443' # HTTPS
    volumes:
      - ./infra/proxy_data:/data
      - ./infra/letsencrypt:/etc/letsencrypt
    networks:
      - private_network

  # Base de Datos NoSQL
  db:
    image: mongo:latest
    container_name: app_mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - ./storage/mongodb_data:/data/db
    networks:
      - private_network

  # API Backend
  api:
    build: ./app/api
    container_name: app_api
    restart: unless-stopped
    environment:
      MONGO_URI: mongodb://${MONGO_USER}:${MONGO_PASSWORD}@db:27017/
      STORAGE_PATH: /app/data/documents
    volumes:
      - ./storage/documents:/app/data/documents
    depends_on:
      - db
    networks:
      - private_network

  # Frontend Web
  web:
    build: ./app/web
    container_name: app_vue_frontend
    restart: unless-stopped
    depends_on:
      - api
    networks:
      - private_network

  # Interfaz de Base de Datos
  mongo-ui:
    image: mongo-express
    container_name: app_mongo_visual
    restart: unless-stopped
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: ${MONGO_USER}
      ME_CONFIG_MONGODB_ADMINPASSWORD: ${MONGO_PASSWORD}
      ME_CONFIG_MONGODB_URL: mongodb://${MONGO_USER}:${MONGO_PASSWORD}@db:27017/
    depends_on:
      - db
    networks:
      - private_network

networks:
  private_network:
    driver: bridge
```

---

## 🔒 Estrategia de Seguridad Aplicada

1.  **Aislamiento de Red:** Los contenedores `api`, `db`, `web` y `mongo-ui` **no exponen puertos** al exterior. Solo el `proxy` es accesible desde internet.
2.  **Cifrado TLS:** Nginx Proxy Manager gestiona certificados Let's Encrypt para que toda la comunicación entre el cliente y el servidor sea HTTPS.
3.  **Persistencia Segura:** Los volúmenes están mapeados a carpetas locales fuera del ciclo de vida de los contenedores. Si un contenedor se actualiza o falla, los PDFs y la DB permanecen intactos en `/storage`.
4.  **Invisibilidad del Backend:** La web se comunica con la API internamente a través de la red de Docker (`http://api:8000`), evitando ataques directos al backend.

---

## 🛠️ Pasos para el Despliegue

1.  **Preparar archivos:** Colocar los `Dockerfile` correspondientes en las carpetas `app/api` y `app/web`.
2.  **Lanzar servicios:**
    ```bash
    docker-compose up -d --build
    ```
3.  **Configurar Proxy:** * Acceder a `http://tu-ip:81`.
    * Configurar un **Proxy Host** para tu dominio apuntando al contenedor `web` (puerto 80).
    * Configurar un subdominio (ej: `api.tusitio.com`) apuntando al contenedor `api` (puerto 8000).
    * Activar **SSL (Let's Encrypt)** en cada Host configurado.

---
*Documentación generada para el proyecto de gestión de documentos PDF - 2026.*