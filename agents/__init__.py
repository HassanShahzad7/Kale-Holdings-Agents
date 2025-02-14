from .base_agent import BaseAgent
from .ceo_agent import CEOAgent
from .summarizer_agent import SummarizerAgent
from .marketing_agents import (
    SEOManager,
    ContentMarketingManager,
    DigitalStrategyManager,
    AdvertisingManager,
    SocialMediaManager,
    EmailMarketingManager,
    AnalyticsManager
)

def initialize_agents() -> dict:
    """
    Initialize and return all agents in a structured dictionary.
    
    Returns:
        dict: Dictionary containing all initialized agents
    """
    return {
        "ceo": CEOAgent(),
        "summarizer": SummarizerAgent(),
        "seo": SEOManager(),
        "content": ContentMarketingManager(),
        "strategy": DigitalStrategyManager(),
        "advertising": AdvertisingManager(),
        "social": SocialMediaManager(),
        "email": EmailMarketingManager(),
        "analytics": AnalyticsManager()
    }

def get_agent_configurations() -> dict:
    """
    Get the configuration details for all agents.
    
    Returns:
        dict: Dictionary containing agent configurations
    """
    return {
        "ceo": {
            "description": "Chief Marketing Officer responsible for overall strategy and delegation",
            "responsibilities": ["Task decomposition", "Strategy planning", "Final decision making"]
        },
        "summarizer": {
            "description": "Agent responsible for compiling and summarizing department responses",
            "responsibilities": ["Data aggregation", "Report generation", "Executive summary creation"]
        },
        "seo": {
            "description": "SEO Manager specialized in search optimization and keyword strategy",
            "responsibilities": ["Keyword research", "SEO optimization", "Technical SEO audits"]
        },
        "content": {
            "description": "Content Marketing Manager focused on creating effective content strategies",
            "responsibilities": ["Content strategy", "Editorial planning", "Content performance analysis"]
        },
        "strategy": {
            "description": "Digital Strategy Manager responsible for overall marketing strategy",
            "responsibilities": ["Strategic planning", "Channel strategy", "Budget allocation"]
        },
        "advertising": {
            "description": "Advertising Manager specialized in paid advertising campaigns",
            "responsibilities": ["Campaign management", "Ad platform selection", "Performance optimization"]
        },
        "social": {
            "description": "Social Media Manager focused on social media strategy and engagement",
            "responsibilities": ["Social media planning", "Community management", "Influencer marketing"]
        },
        "email": {
            "description": "Email Marketing Manager specialized in email campaigns and automation",
            "responsibilities": ["Email campaign strategy", "List segmentation", "Automation workflows"]
        },
        "analytics": {
            "description": "Analytics Manager focused on tracking and analyzing marketing performance",
            "responsibilities": ["Data analysis", "Performance tracking", "Reporting"]
        }
    }

def get_department_agents() -> dict:
    """
    Get only the department-specific agents.
    
    Returns:
        dict: Dictionary containing department agents
    """
    agents = initialize_agents()
    return {k: v for k, v in agents.items() if k not in ["ceo", "summarizer"]}

# Export specific agents for direct access
__all__ = [
    'CEOAgent',
    'SummarizerAgent',
    'SEOManager',
    'ContentMarketingManager',
    'DigitalStrategyManager',
    'AdvertisingManager',
    'SocialMediaManager',
    'EmailMarketingManager',
    'AnalyticsManager',
    'initialize_agents',
    'get_agent_configurations',
    'get_department_agents'
]