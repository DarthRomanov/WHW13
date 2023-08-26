"""
Main FastAPI Application

This module initializes the FastAPI application and includes various routers for different functionalities.

Attributes:
    origins (list): List of allowed origins for CORS.

Example:
    To start the FastAPI application, you can run this script using a command like:

    ```
    uvicorn main:app --reload
    ```

    This will start the server and make it accessible at `http://localhost:8000`.

    To access the different routes and endpoints defined in the routers, you can use tools like `curl` or Postman.

    For example, to create a new user, you can send a POST request to `http://localhost:8000/api/register/` with the necessary data.

Note:
    Make sure to customize the `origins` list to include the allowed origins for Cross-Origin Resource Sharing (CORS).
"""

from fastapi import FastAPI
from src.routes import contacts, users, auth, token
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter



app = FastAPI()


limiter = FastAPILimiter(
    key_func=lambda request: request.client.host,
    default_limits=["10 per minute"]
)

app.include_router(contacts.router, prefix="/api")  # Можете додати префікс "/api"
app.include_router(users.router, prefix="/api")     # Можете додати префікс "/api"
app.include_router(auth.router, prefix="/api/auth") # Додайте маршрути з авторизацією
app.include_router(token.router, prefix="/api/token") # Додайте маршрути для токенів
@app.get("/")
def read_root():
    """Root Endpoint

    Returns a simple message indicating the server is up and running.

    Returns:
        dict: A dictionary containing a message.
    """
    return {"message": "Hello World"}


# Налаштування CORS
origins = [
    "http://localhost",
    "http://localhost:8080",  # Додайте адреси, з яких дозволяєте запити
    "http://example.com",
    "https://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)