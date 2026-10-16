from fastapi import FastAPI
import database
import models
from router import router as livros_router

# Cria as tabelas no banco de dados SQLite caso ainda não existam
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="API de Livros",
    description="API para gerenciamento e cadastro de livros",
    version="1.0.0",
)

app.include_router(livros_router)


@app.get("/")
def root():
    return {"message": "API de Livros rodando com sucesso!"}