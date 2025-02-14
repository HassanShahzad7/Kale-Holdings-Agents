from .base_agent import BaseAgent
from typing import Dict, Any

class CEOAgent(BaseAgent):
    def __init__(self):
        role_description = """You are a CEO of a marketing agency responsible for analyzing requests, 
        determining required departments, and creating comprehensive marketing plans."""
        super().__init__(role_description=role_description)

    async def determine_required_departments(self, request: str) -> Dict[str, Any]:
        """Analyze request and determine required departments"""
        prompt_template = """
        Analyze the following marketing request and determine which departments should be involved.
        
        Available departments:
        - seo: SEO Manager for search optimization and keyword strategy
        - content: Content Marketing Manager for content creation and strategy
        - strategy: Digital Strategy Manager for overall marketing strategy
        - advertising: Advertising Manager for paid campaigns
        - social: Social Media Manager for social media strategy
        - email: Email Marketing Manager for email campaigns
        - analytics: Analytics Manager for tracking and reporting
        
        Request: {request}
        
        Return a JSON with selected departments, including for each:
        1. Justification for why they're needed
        2. Specific task description
        3. Priority level (1-5, 1 being highest)
        4. Any relevant context or dependencies
        
        Format:
        {{
            "selected_departments": {{
                "department_code": {{
                    "justification": "reason for selection",
                    "task": "specific task description",
                    "priority": priority_number,
                    "context": {{"key": "value"}}
                }}
            }}
        }}
        """
        self.setup_chain(prompt_template)
        return await self.process({"request": request})

    async def create_final_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create final response from summarized data"""
        prompt_template = """
        Create a comprehensive final marketing plan based on the following information.
        
        Original Request: {original_request}
        Summarized Plan: {summary}
        Department Selection: {department_selection}
        
        Provide a detailed JSON response with the following structure:
        {{
            "executive_summary": {{
                "overview": "Brief overview of the complete marketing plan",
                "key_objectives": ["List main objectives"],
                "expected_outcomes": ["List expected outcomes"]
            }},
            "strategic_approach": {{
                "core_strategy": "Main strategic direction",
                "target_audience": "Description of target audience",
                "unique_value_proposition": "What sets this plan apart",
                "key_success_factors": ["List key success factors"]
            }},
            "department_strategies": {{
                "department_name": {{
                    "objectives": ["Department-specific objectives"],
                    "key_actions": ["Specific actions to take"],
                    "timeline": "Implementation timeline",
                    "resources_needed": ["Required resources"]
                }}
            }},
            "implementation_timeline": {{
                "phase": {{
                    "duration": "Time period",
                    "key_activities": ["Activities in this phase"],
                    "milestones": ["Key milestones"],
                    "dependencies": ["Dependencies"]
                }}
            }},
            "resource_allocation": {{
                "department": {{
                    "budget_percentage": "Allocated budget",
                    "key_resources": ["Required resources"],
                    "success_metrics": ["Metrics to track"]
                }}
            }},
            "risk_assessment": [
                {{
                    "risk_area": "Area of risk",
                    "probability": "Likelihood",
                    "impact": "Potential impact",
                    "mitigation_strategy": "How to address"
                }}
            ],
            "next_steps": {{
                "immediate_actions": ["Actions to take now"],
                "key_decisions": ["Decisions needed"],
                "review_points": ["When to review progress"]
            }}
        }}
        
        Ensure the response is actionable, measurable, and aligns with the department strategies provided.
        """
        self.setup_chain(prompt_template)
        return await self.process(data)