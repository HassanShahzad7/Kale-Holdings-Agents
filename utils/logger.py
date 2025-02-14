import logging
import json
from datetime import datetime
import os
from typing import Any, Dict, Optional

class MarketingLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Set up logging
        self.logger = logging.getLogger('marketing_agents')
        self.logger.setLevel(logging.INFO)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('logs/marketing_agents.log')

        # Create formatters and add it to handlers
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log_request(self, request_id: str, prompt: str) -> None:
        """Log incoming request"""
        self.logger.info(f"New request {request_id}: {prompt}")

    def log_agent_start(self, request_id: str, agent_name: str) -> None:
        """Log when an agent starts processing"""
        self.logger.info(f"Request {request_id}: {agent_name} started processing")

    def log_agent_completion(self, request_id: str, agent_name: str, response: Dict[str, Any]) -> None:
        """Log when an agent completes processing"""
        self.logger.info(f"Request {request_id}: {agent_name} completed")
        self.logger.debug(f"Response from {agent_name}: {json.dumps(response, indent=2)}")

    def log_agent_error(self, request_id: str, agent_name: str, error: str) -> None:
        """Log agent errors"""
        self.logger.error(f"Request {request_id}: {agent_name} failed - {error}")

    def log_workflow_step(self, request_id: str, step: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Log workflow progress"""
        message = f"Request {request_id}: Workflow step '{step}'"
        if details:
            message += f" - {json.dumps(details)}"
        self.logger.info(message)

    def log_error(self, request_id: str, error: str) -> None:
        """Log general errors"""
        self.logger.error(f"Request {request_id}: Error - {error}")

logger = MarketingLogger()