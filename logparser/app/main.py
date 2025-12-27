from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import threading
import asyncio
from app.config.settings import settings
from app.messaging.consumer import start_consumer
from app.messaging.rabbitmq import get_rabbitmq_connection
from app.api.routes import router
from app.database.mongodb import mongodb

# Lifespan pour démarrer consumer en background
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("🚀 Starting LogParser...")
    
    # Initialize DB (Offline safe)
    mongodb.connect()
    
    # Démarrer consumer RabbitMQ dans un thread séparé
    # Only if not in strict offline mode (but user wants to test rabbit, so we try)
    consumer_thread = threading.Thread(
        target=start_consumer, 
        daemon=True
    )
    consumer_thread.start()
    
    yield  # Application tourne
    
    # SHUTDOWN
    print("🛑 Shutting down LogParser...")

# Créer app FastAPI
app = FastAPI(
    title="LogParser (Refactored)",
    version="2.0.0",
    lifespan=lifespan
)

# Inclure routes
app.include_router(router)

# Health check
@app.get("/health")
async def health():
    # Check RabbitMQ
    rmq_status = "disconnected"
    try:
        # Quick check using existing logic helper or direct connection
        # Since logic is in message loop, let's just do a basic socket check or reuse logic
        # For simplicity/speed in offline mode, reusing connection factory with timeout:
        params = get_rabbitmq_connection().close()
        rmq_status = "connected"
    except:
        pass
    
    if not mongodb.is_connected:
        raise HTTPException(
            status_code=503, 
            detail={
                "status": "unhealthy",
                "service": "LogParser", 
                "mongodb": "disconnected",
                "rabbitmq": rmq_status
            }
        )

    return {
        "status": "healthy",
        "service": "LogParser",
        "mongodb": "connected",
        "rabbitmq": rmq_status,
        "mode": "production"
    }