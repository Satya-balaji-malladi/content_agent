from fastapi import FastAPI
import logging
import uvicorn
from scheduler import start_scheduler, daily_content_job
from contextlib import asynccontextmanager

# Logging Setup
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler = start_scheduler()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "running", "service": "Headless Content Agent"}

@app.post("/trigger-now")
async def trigger_manual():
    """Manually trigger the job for testing."""
    await daily_content_job()
    return {"message": "Job triggered manually"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
