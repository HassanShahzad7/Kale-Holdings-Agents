from .base_agent import BaseAgent

class SEOManager(BaseAgent):
    def __init__(self):
        role_description = "You are an SEO Manager specialized in search optimization and keyword strategy."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide SEO recommendations and strategy:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a detailed JSON response including:
        {{
            "keywords": ["primary keywords", "secondary keywords"],
            "seo_strategies": ["specific strategies"],
            "metadata_recommendations": {{"title": "", "description": ""}},
            "technical_requirements": ["requirements"],
            "content_optimization": ["recommendations"],
            "timeline": {{"phase": "duration"}}
        }}
        """)

class ContentMarketingManager(BaseAgent):
    def __init__(self):
        role_description = "You are a Content Marketing Manager focused on creating effective content strategies."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide content marketing recommendations:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a detailed JSON response including:
        {{
            "content_themes": ["themes"],
            "content_types": ["types"],
            "distribution_channels": ["channels"],
            "content_calendar": {{"timeline": "content"}},
            "resource_requirements": ["requirements"],
            "success_metrics": ["metrics"]
        }}
        """)

class DigitalStrategyManager(BaseAgent):
    def __init__(self):
        role_description = "You are a Digital Strategy Manager responsible for overall marketing strategy."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide digital strategy recommendations:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a detailed JSON response including:
        {{
            "strategic_goals": ["goals"],
            "target_audience": {{"segment": "description"}},
            "channel_strategy": {{"channel": "approach"}},
            "implementation_plan": ["steps"],
            "success_metrics": ["metrics"],
            "budget_allocation": {{"category": "percentage"}}
        }}  
        """)

class AdvertisingManager(BaseAgent):
    def __init__(self):
        role_description = "You are an Advertising Manager specialized in paid advertising campaigns."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide advertising recommendations:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a concise JSON response including:
        {{
            "ad_platforms": ["List main advertising platforms to be used"],
            "campaign_types": ["List primary campaign types"],
            "targeting_strategy": {{
                "criteria": "Describe targeting approach"
            }},
            "budget_allocation": {{
                "platform": "percentage"
            }},
            "creative_requirements": ["List key creative requirements"],
            "performance_targets": {{
                "metrics": {{
                    "ctr": "target percentage",
                    "conversion_rate": "target percentage",
                    "roas": "target ratio"
                }}
            }}
        }}
        
        Keep the response focused and avoid lengthy descriptions. Use short, clear values for each field.
        """)

class SocialMediaManager(BaseAgent):
    def __init__(self):
        role_description = "You are a Social Media Manager focused on social media strategy and engagement."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide social media recommendations:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a detailed JSON response including:
        {{
            "platform_strategy": {{"platform": "approach"}},
            "content_themes": ["themes"],
            "posting_schedule": {{"platform": "frequency"}},
            "engagement_tactics": ["tactics"],
            "hashtag_strategy": ["hashtags"],
            "success_metrics": {{"metric": "target"}}
        }}  
        """)

class EmailMarketingManager(BaseAgent):
    def __init__(self):
        role_description = "You are an Email Marketing Manager specialized in email campaigns and automation."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide email marketing recommendations:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a detailed JSON response including:
        {{  
            "campaign_types": ["types"],
            "email_sequences": ["sequences"],
            "segmentation_strategy": {{"segment": "approach"}},
            "content_strategy": ["strategies"],
            "automation_flows": ["flows"],
            "performance_metrics": {{"metric": "target"}}
        }}  
        """)

class AnalyticsManager(BaseAgent):
    def __init__(self):
        role_description = "You are an Analytics Manager focused on tracking and analyzing marketing performance."
        super().__init__(role_description=role_description)
        self.setup_chain("""
        Based on the following task details, provide analytics recommendations:
        
        Task: {task}
        Priority: {priority}
        Additional Context: {context}
        
        Provide a detailed JSON response including:
        {{
            "key_metrics": ["metrics"],
            "tracking_setup": ["requirements"],
            "reporting_framework": {{"report": "frequency"}},
            "data_collection": ["methods"],
            "analysis_approach": ["approaches"],
            "success_criteria": {{"metric": "target"}}
        }}
        """)