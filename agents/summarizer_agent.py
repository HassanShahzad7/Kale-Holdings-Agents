from typing import Dict, Any
from .base_agent import BaseAgent

class SummarizerAgent(BaseAgent):
    def __init__(self):
        role_description = """You are a Summarizer Agent responsible for consolidating and integrating 
        responses from different marketing departments into a cohesive plan."""
        
        # Create the prompt template with escaped braces for output JSON structure
        prompt_template = """
        Review and integrate the following department responses into a comprehensive marketing plan:
        
        Original Request: {original_request}
        Department Responses: {responses}
        Selected Departments: {selected_departments}
        
        Based on the department responses and considering their strategies, create a cohesive summary that includes:
        1. Executive Summary
        2. Integrated Marketing Strategy
        3. Department-Specific Recommendations
        4. Implementation Timeline
        5. Resource Requirements
        6. Success Metrics
        7. Risk Assessment and Mitigation Plans
        
        Do not miss any important information from the department responses.
        Return a JSON response with the following structure:
        {{
            "executive_summary": "Brief overview of the complete marketing plan",
            "integrated_strategy": {{
                "overview": "Main strategic direction",
                "key_objectives": ["objective1", "objective2"],
                "target_audience": "Description of target audience",
                "positioning": "Brand positioning statement"
            }},
            "department_strategies": {{
                "department_name": {{
                    "recommendations": ["rec1", "rec2"],
                    "implementation": "Implementation approach"
                }}
            }},
            "timeline": {{
                "phase1": {{
                    "duration": "timeframe",
                    "key_activities": ["activity1", "activity2"]
                }}
            }},
            "resource_requirements": {{
                "department": ["requirement1", "requirement2"]
            }},
            "success_metrics": {{
                "metric_category": ["metric1", "metric2"]
            }},
            "risk_assessment": [
                {{
                    "risk": "description",
                    "impact": "severity",
                    "mitigation": "strategy"
                }}
            ]
        }}
        """
        
        super().__init__(role_description=role_description)
        self.setup_chain(prompt_template)

    async def compile_responses(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Compile and integrate responses from all departments"""
        return await self.process(data)