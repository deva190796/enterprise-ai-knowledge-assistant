from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import Base, engine
import app.models

from app.database.database import engine

from app.api.users import router as user_router

from app.api.documents import router as document_router

from app.routes.chat import router as chat_router

from app.routes import dashboard

app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

app.include_router(document_router)

app.include_router(chat_router)

app.include_router(dashboard.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Enterprise AI Knowledge Assistant 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "message": "Database connected successfully!"
    }