# Resumen Arquitectónico y Dockerización del Proyecto "Liquor POS"

Este documento resume la evolución arquitectónica del proyecto y el proceso paso a paso de su dockerización, pasando de ser una aplicación de escritorio nativa a una solución web escalable y en contenedores.

## 1. Evolución de la Arquitectura (De Escritorio a Web)
El proyecto originalmente estaba construido como un **monolito de escritorio** utilizando **PySide6 (Qt)**. Sin embargo, gracias a que desde el inicio se implementó una excelente **Clean Architecture (Domain-Driven Design)**, toda la lógica de negocio (las carpetas `core` y `application`) estaba completamente desacoplada de la interfaz gráfica.

Para poder "dockerizar" el sistema con un enfoque moderno Cliente-Servidor (que es el estándar de la industria), realizamos una transición a una **Arquitectura Web**:
- **Backend (API):** Reemplazamos la capa de presentación de PySide6 por **FastAPI**, exponiendo los "Casos de Uso" originales de Python (como el registro de productos) mediante endpoints REST.
- **Frontend (Web):** Creamos una interfaz de usuario completamente nueva y moderna utilizando **React con Vite y TypeScript**.

## 2. Reestructuración del Proyecto
Organizamos el repositorio en dos micro-entornos independientes:

- **`/backend`**: Contiene todo el código Python original (DDD), la base de datos SQLite, los nuevos `routers` de FastAPI y sus dependencias.
- **`/frontend`**: Contiene el código fuente de React, estilos CSS y componentes web.

## 3. Proceso de Dockerización (Paso a Paso)

### A. Dockerización del Backend (Python)
Creamos un `Dockerfile` en la carpeta `/backend` usando la imagen ligera `python:3.11-slim`:
1. Configuramos el entorno de Python.
2. Copiamos el `requirements.txt` e instalamos las nuevas dependencias requeridas para la web (`fastapi`, `uvicorn`, `pydantic`).
3. Exponemos el puerto `8000`.
4. Utilizamos `uvicorn` para levantar el servidor de la API de forma automática al iniciar el contenedor.

### B. Dockerización del Frontend (React/Node)
Creamos un `Dockerfile` en la carpeta `/frontend` basado en la imagen `node:20-slim`:
1. Copiamos los archivos de manifiesto e instalamos dependencias mediante `npm install`.
2. Exponemos el puerto `5173` (puerto por defecto del servidor Vite).
3. Configuramos el comando de arranque para lanzar el entorno con la bandera `--host`, permitiendo que el servidor web sea accesible desde fuera del contenedor de Docker.

### C. Orquestación general con Docker Compose
Para unificar ambos servicios, creamos el archivo `docker-compose.yml` en la raíz del proyecto. Sus responsabilidades son:
- Construir y levantar ambos contenedores (`backend` y `frontend`) con un solo comando (`docker-compose up --build`).
- Habilitar la comunicación entre ellos.
- **Manejo de Volúmenes (Crucial):**
  - Se configuró un volumen para el archivo `liquor_pos.db` asegurando la persistencia de datos (si el contenedor se apaga, no se pierden los productos).
  - Se montó el código fuente del frontend como volumen, aislando al mismo tiempo la carpeta `node_modules` interna del contenedor. Esto permite editar código en Windows y ver los cambios inmediatamente en el navegador sin reconstruir Docker.

## 4. Prueba de Concepto Implementada
Para validar que los contenedores se comunican correctamente, conectamos un flujo completo *End-to-End*:
1. **Backend:** Construimos el endpoint `POST /api/products/` en FastAPI. Este inyecta la base de datos directamente al `RegisterProductUseCase` de la Clean Architecture original.
2. **Frontend:** Diseñamos un formulario en React con estilos *Glassmorphism* (diseño premium y moderno) que captura los datos del producto (SKU, volumen, grados de alcohol, etc).
3. **Flujo:** Al guardar en el Frontend (puerto 5173), la petición viaja por la red interna de Docker hacia FastAPI (puerto 8000), el cual procesa las reglas de negocio y almacena los datos, validando el éxito total de la dockerización y el rediseño arquitectónico.

## 5. Hitos Recientes e Integración Final

Durante las sesiones más recientes, completamos el ciclo de vida de la aplicación con integraciones avanzadas:

### A. Integración del "Punto de Venta" (POS) con la Base de Datos
- **Backend:** Se construyó el endpoint `GET /api/products/`, implementando la función `get_all` dentro del Protocolo del Repositorio y su adaptador de SQLAlchemy.
- **Frontend:** La Caja Registradora (`POSPage.tsx`) pasó de tener datos estáticos a hacer consultas dinámicas en tiempo real a la API. Ahora, el buscador escanea y filtra productos reales usando el Código de Barras (Barcode), el SKU o el Nombre del producto.

### B. Diseño Premium y "Dashboard" Analítico
- Se diseñó el `DashboardPage.tsx` empleando un estilo "Glassmorphism" (paneles de vidrio semitransparentes).
- Se instaló e integró la biblioteca `recharts` directamente en el contenedor del frontend, logrando visualizar el flujo de ventas a través de una gráfica de Área interactiva y sofisticada con colores en gradiente.

### C. Restricción de Acceso y Reglas de Negocio (Domain-Driven Design)
- **Login Restringido:** Se configuró un control estricto en la vista de Login (`LoginPage.tsx`), el cual permite la entrada exclusiva a las credenciales administrativas (`admin` / `admin`).
- **Manejo Estricto del INVIMA:** Gracias al núcleo en DDD, la regla que exige Registro INVIMA para productos alcohólicos provocó rechazos ante la falta de este campo. Se solucionó (1) agregando el campo en la interfaz web de creación de productos y (2) programando un "fallback" a nivel de API (`routers/products.py`) para evitar problemas con la caché del navegador.
- **Validaciones de Códigos de Barras:** Se evidenció en tiempo real la robustez de las validaciones de Dominio (ej. rechazo de códigos de barras con espacios o guiones no alfanuméricos).

### D. Ajustes Finales de Infraestructura Docker
- Se mejoró el mapeo de volúmenes en `docker-compose.yml`. En lugar de sincronizar únicamente el archivo `liquor_pos.db`, se montó toda la carpeta `./backend:/app` completa. Esto asegura que el código modificado externamente (en Windows) se refleje inmediatamente dentro del contenedor de Python.
