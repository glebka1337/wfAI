import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from dishka.integrations.fastapi import setup_dishka
from app.infrastructure.di.container import make_container
from app.infrastructure.bootstrap import AppBootstrapper
from app.core.config import settings

# Import all document models for Beanie initialization
from app.adapters.mongo.models import ALL_DOCUMENT_MODELS

# Import Routers
from app.adapters.api.routers import chat, sessions, settings as settings_router, commands, icons, memories

from app.adapters.qdrant.initializer import QdrantInitializer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize container globally so it can be used in lifespan and setup_dishka
container = make_container()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 1. Infrastructure Initialization ---
    # Container is already created globally
    
    async with container() as request_container:
        # Resolve dependencies needed for initialization
        mongo_client = await request_container.get(AsyncIOMotorClient)
        qdrant_initializer = await request_container.get(QdrantInitializer)
        
        # We need repos for bootstrapping
        from app.domain.interfaces.repositories.user import IUserProfileRepository
        from app.domain.interfaces.repositories.persona import IPersonaRepository
        
        user_repo = await request_container.get(IUserProfileRepository)
        persona_repo = await request_container.get(IPersonaRepository)
        bootstrapper = AppBootstrapper(user_repo, persona_repo)

        # --- 2. Database (Beanie) ---
        logger.info("Initializing Beanie (MongoDB)...")
        await init_beanie(
            database=mongo_client[settings.DB_NAME],
            document_models=ALL_DOCUMENT_MODELS
        )
        
        # --- 3. Vector DB (Qdrant) ---
        logger.info("Initializing Qdrant...")
        await qdrant_initializer.run()
        
        # --- 4. Application Bootstrap ---
        await bootstrapper.run()
    
    yield
    
    # --- Cleanup ---
    await container.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Setup Dishka (Dependency Injection)
    # Must be called here to add middleware before app starts
    setup_dishka(container, app)
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include Routers
    app.include_router(chat.router)
    app.include_router(sessions.router)
    app.include_router(settings_router.router)
    app.include_router(commands.router)
    app.include_router(icons.router)
    app.include_router(memories.router)
    
    return app

app = create_app()
