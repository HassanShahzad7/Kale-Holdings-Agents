from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
from typing import Dict, Any
from datetime import datetime, UTC
import os
from dotenv import load_dotenv
import json
from contextlib import asynccontextmanager

# Import models and agents
from models.pydantic_models import MarketingRequest
from agents import initialize_agents, get_department_agents
from agents.summarizer_agent import SummarizerAgent
from workflow.langgraph_workflow import create_marketing_workflow, execute_workflow
from config.settings import get_settings
from utils.logger import logger  # Custom logger

# Load environment variables
load_dotenv()

# Get settings
settings = get_settings()

# Global variable for workflow
marketing_workflow = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for FastAPI app.
    Handles startup and shutdown of the application.
    """
    # Startup
    logger.logger.info("Starting Marketing Strategy API...")
    try:
        # Initialize all agents
        all_agents = initialize_agents()
        ceo_agent = all_agents["ceo"]
        summarizer_agent = all_agents["summarizer"]
        department_agents = get_department_agents()
        
        # Create workflow and assign to global variable
        global marketing_workflow
        marketing_workflow = create_marketing_workflow(
            ceo_agent=ceo_agent,
            department_agents=department_agents,
            summarizer_agent=summarizer_agent
        )
        logger.logger.info("Successfully initialized all agents and workflow")
    except Exception as e:
        logger.logger.error(f"Error initializing agents: {str(e)}")
        raise
    yield
    # Shutdown
    logger.logger.info("Shutting down Marketing Strategy API...")

# Initialize FastAPI app
app = FastAPI(
    title="Marketing Strategy Generator",
    description="Generate marketing strategies from simple prompts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.post(
    "/marketing-strategy",
    tags=["Marketing"],
    summary="Generate marketing strategy",
    description="Generate a comprehensive marketing strategy based on a simple prompt"
)
async def generate_marketing_strategy(
    request: MarketingRequest,
    background_tasks: BackgroundTasks
) -> Response:
    try:
        # Log request
        logger.log_request(request.request_id, request.prompt)
        background_tasks.add_task(
            logger.log_workflow_step,
            request.request_id,
            "start",
            {"prompt": request.prompt}
        )

        if marketing_workflow is None:
            raise HTTPException(
                status_code=503,
                detail="Service is initializing. Please try again in a moment."
            )

        # Execute workflow
        result = await execute_workflow(
            workflow=marketing_workflow,
            request_id=request.request_id,
            prompt=request.prompt
        )

        # Log success
        logger.log_workflow_step(request.request_id, "complete", {"status": "success"})

        # Create success response with complete data
        response_data = {
            "request_id": request.request_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": result["status"],
            "marketing_strategy": result["summary"],            # Include the summary
            "department_details": result["department_responses"] # Include department details
        }

        return Response(
            content=json.dumps(response_data, ensure_ascii=False),
            media_type="application/json"
        )

    except Exception as e:
        # Log error
        error_msg = f"Error processing request: {str(e)}"
        logger.log_error(request.request_id, error_msg)

        # Create error response
        error_response = {
            "error": error_msg,
            "request_id": request.request_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "error",
            "message": "Failed to generate marketing strategy. Please try again."
        }

        return Response(
            content=json.dumps(error_response, ensure_ascii=False),
            status_code=500,
            media_type="application/json"
        )
    
    
@app.get(
    "/health",
    tags=["System"],
    summary="Check system health",
    description="Verify if the API and all its components are healthy"
)
async def health_check() -> Dict[str, Any]:
    """
    Check if the API is running and all components are healthy.
    
    Returns:
        Dict[str, Any]: Health status of the API
    """
    try:
        is_ready = marketing_workflow is not None
        return {
            "status": "healthy" if is_ready else "initializing",
            "workflow_ready": is_ready,
            "timestamp": datetime.now(UTC).isoformat(),
            "version": settings.APP_VERSION,
            "environment": os.getenv("ENV", "development")
        }
    except Exception as e:
        logger.logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(UTC).isoformat()
        }

# Additional endpoints can be added here as needed