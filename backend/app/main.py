from fastapi import FastAPI
from .db.session import engine # engine is used, init_db is not directly called here anymore
from .db import models # Import models to ensure Base knows about them
from .api.endpoints import auth as auth_router # Import the auth router
from .api.endpoints import verkada as verkada_router # Import the Verkada router

# Create all tables in the database if they don't exist yet.
# This should ideally be handled by Alembic for migrations in a production app,
# but for simplicity, we'll call it directly on startup.
models.Base.metadata.create_all(bind=engine) # More direct way to create tables

app = FastAPI(
    title="Verkada Access Control Dashboard API",
    description="API for the Verkada Access Control Dashboard.",
    version="0.1.0",
)

@app.on_event("startup")
async def on_startup():
    """
    Actions to perform on application startup.
    Initializes the database.
    """
    # models.Base.metadata.create_all(bind=engine) # This is already done at module level

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    Provides a welcome message.
    """
    return {"message": "Welcome to the Verkada Access Control Dashboard API"}

# Include API routers
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(verkada_router.router, prefix="/api/v1/verkada", tags=["verkada"])

# Further imports and other routers will be added here.