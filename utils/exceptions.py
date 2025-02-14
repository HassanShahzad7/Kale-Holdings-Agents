from typing import Optional, Dict, Any

class MarketingAgentException(Exception):
    """Base exception for Marketing Agents"""
    def __init__(
        self,
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class WorkflowException(MarketingAgentException):
    """Exception raised for errors in the workflow process"""
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="WORKFLOW_ERROR",
            details=details
        )

class AgentProcessingException(MarketingAgentException):
    """Exception raised when an agent fails to process a request"""
    def __init__(
        self,
        agent_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"{agent_type} processing failed: {message}",
            error_code="AGENT_PROCESSING_ERROR",
            details=details
        )

class InvalidResponseException(MarketingAgentException):
    """Exception raised when agent response is invalid"""
    def __init__(
        self,
        agent_type: str,
        message: str,
        response: Any
    ):
        super().__init__(
            message=f"Invalid response from {agent_type}: {message}",
            error_code="INVALID_RESPONSE",
            details={"response": str(response)}
        )

class TimeoutException(MarketingAgentException):
    """Exception raised when processing times out"""
    def __init__(
        self,
        operation: str,
        timeout: int,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Operation '{operation}' timed out after {timeout} seconds",
            error_code="TIMEOUT_ERROR",
            details=details
        )