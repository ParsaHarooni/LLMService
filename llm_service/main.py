from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import router
from .core.config import settings

app = FastAPI(
    title="LLM Service",
    description="A gateway service for LLM-based code analysis",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router, prefix="/api/v1")
