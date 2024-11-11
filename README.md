# DNA Mutant Detection API

API desarrollada con FastAPI para detectar mutantes basándose en secuencias de ADN. La API recibe secuencias de ADN en formato de listas de cadenas de caracteres y determina si pertenecen a un mutante o no, almacenando los resultados en una base de datos MongoDB.

El servicio se encuentra corriendo en Render y puede ser accedido en la siguiente URL:
[https://genai-ffb-meli-desafiotecnico.onrender.com](https://genai-ffb-meli-desafiotecnico.onrender.com)

## Funcionalidades

- **Health Check (`/health`)**: Verifica si la API está activa.
- **Detección de Mutantes (`/mutant/`)**: Recibe una secuencia de ADN y determina si es de un mutante.
- **Estadísticas (`/stats`)**: Muestra el número de ADN de mutantes y humanos y su relación.

## Requisitos

- Python 3.7 o superior
- MongoDB
- Certifi (para asegurar la conexión con MongoDB)
- Pydantic
- FastAPI
- python-dotenv (para gestionar variables de entorno)

## Instalación

1. **Clona este repositorio:**
    ```bash
    git clone https://github.com/gnavarte/GenAI_FFB_MELI_DesafioTecnico.git
    cd GenAI_FFB_MELI_DesafioTecnico
    ```

2. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configura las variables de entorno:**
    Crea un archivo `.env` en el directorio raíz del proyecto y agrega la variable `MONGO_URI` con la URI de conexión a tu base de datos MongoDB:
    ```bash
    MONGO_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/<nombre_base_de_datos>?retryWrites=true&w=majority
    ```

## Uso

1. **Ejecuta el servidor:**
    ```bash
    python -m uvicorn main:app
    ```

2. **Accede a la documentación de la API en:**
    [http://localhost:8000/docs](http://localhost:8000/docs)

## EndPoints disponibles:

### **GET `/`**
Devuelve un mensaje de bienvenida.

- **Respuesta:**
    ```json
    {
      "message": "Welcome to the DNA Mutant Detection API!"
    }
    ```

### **GET `/health`**
Devuelve el estado de la API.

- **Respuesta:**
    ```json
    {
      "status": "ok"
    }
    ```

### **POST `/mutant/`**
Recibe una secuencia de ADN y determina si es de un mutante.

- **Cuerpo de la solicitud (JSON):**
    ```json
    {
      "dna": [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
      ]
    }
    ```

- **Respuestas:**
    - Si es un mutante:
        ```json
        {
          "message": "Mutant detected"
        }
        ```
    - Si no es un mutante (status 403):
        ```json
        {
          "detail": "Forbidden: Not a mutant"
        }
        ```

### **GET `/stats`**
Muestra estadísticas de los ADN de mutantes y humanos.

- **Respuesta:**
    ```json
    {
      "count_mutant_dna": 10,
      "count_human_dna": 100,
      "ratio": 0.1
    }
    ```
