from fastapi import FastAPI
from tasks.routers import router as signal_router

tags_metadata = [
    {
        "name": "signals",
        "description": "Operations for predicting buy/sell/hold signals based on gold and coin prices",
        "externalDocs": {
            "description": "Learn more about signal generation logic",
            "url": "https://example.com/docs/signals",
        },
    },
    {
        "name": "health",
        "description": "Health check and service status endpoints",
    },
]

signal_app = FastAPI(
    title="Gold & Coin Signal API",
    description="API for predicting buy/sell/hold signals based on gold and coin prices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags= tags_metadata,
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    }
)

signal_app.include_router(signal_router)