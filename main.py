from dotenv import load_dotenv
import os
import uvicorn
from api.endpoints import app
from config.settings import Settings

# Load environment variables before anything else
load_dotenv()

settings = Settings()

if __name__ == "__main__":
    # Verify environment variables are loaded
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set!")
        
    uvicorn.run(
        "api.endpoints:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level="info"
    )