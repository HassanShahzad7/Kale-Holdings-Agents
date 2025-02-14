# Marketing Strategy Generator API

This project is an AI agentic workflow created in LangGraph with multiple agents. The CEO agent acts as the planner and orchestrator, while multiple manager agents are responsible for their respective tasks. The code runs using a FastAPI endpoint to generate comprehensive marketing strategies based on simple prompts.

## Features

- **CEO Agent**: Acts as the planner and orchestrator.
- **Manager Agents**: Handle specific tasks within the workflow.
- **Summarizer Agent**: Summarizes the final marketing strategy.
- **FastAPI**: Provides a RESTful API for generating marketing strategies.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/marketing-strategy-generator.git
    cd marketing-strategy-generator
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add the necessary environment variables.

## Running the API

1. Start the FastAPI server:
    ```bash
    uvicorn api.endpoints:app --reload
    ```

2. The API will be available at `http://localhost:8000`.

## Usage

### Generate Marketing Strategy

Endpoint: `POST /marketing-strategy`

Generate a comprehensive marketing strategy based on a simple prompt.

- **URL**: `http://localhost:8000/marketing-strategy`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "prompt": "Create a marketing plan for our new eco-friendly phone case company"
    }
    ```

- **Response**:
    ```json
    {
        "request_id": "unique-request-id",
        "timestamp": "2023-10-01T12:00:00Z",
        "status": "success",
        "marketing_strategy": "Your marketing strategy summary...",
        "department_details": {
            "department1": "Details...",
            "department2": "Details..."
        }
    }
    ```

### Health Check

Endpoint: `GET /health`

Verify if the API and all its components are healthy.

- **URL**: `http://localhost:8000/health`
- **Method**: `GET`
- **Response**:
    ```json
    {
        "status": "healthy",
        "workflow_ready": true,
        "timestamp": "2023-10-01T12:00:00Z",
        "version": "1.0.0",
        "environment": "development"
    }
    ```

## Logging

The API uses a custom logger to log requests, workflow steps, and errors. Logs are stored in the specified log directory.
