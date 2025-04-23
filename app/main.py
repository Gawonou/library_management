import os
import sys


# Ensure project root is in Python path
# so that "app" package can be imported when running as script
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)




import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.rest import api_router
from app.api.graphql.schema import schema

# Ensure project root is in Python path
# so that "app" package can be imported when running as script
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Gestionnaire de cycle de vie (startup et shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie de l'application.
    Code avant yield : startup
    Code après yield : shutdown
    """
    # Code de démarrage (avant le yield)
    print("L'application démarre...")
    Base.metadata.create_all(bind=engine)  # Création des tables dans la base de données
    
    # Code de fermeture (après le yield)
    yield
    print("L'application se ferme...")

# Initialisation de l'application FastAPI
title = settings.PROJECT_NAME
app = FastAPI(
    title=title,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,  # Utilisation du gestionnaire de cycle de vie
)

# Configuration du CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes de l'API REST
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["REST"])

# Monter l'endpoint GraphQL
app.add_route("/graphql", GraphQLApp(schema=schema))
app.add_websocket_route("/graphql", GraphQLApp(schema=schema))

# Point d'entrée de l'application
def main():
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )

if __name__ == "__main__":
    main()
