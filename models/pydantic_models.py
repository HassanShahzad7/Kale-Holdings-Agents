from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional, Any, Annotated
from datetime import datetime
import uuid
import operator

# Request Models
class MarketingRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str = Field(..., description="Marketing request or question")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(arbitrary_types_allowed=True)

# Department Task Models
class Department(BaseModel):
    justification: str
    task: str
    priority: int = Field(ge=1, le=5)
    context: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

class TaskBreakdown(BaseModel):
    selected_departments: Dict[str, Department]
    priority_order: List[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)

# Workflow State Model
class WorkflowState(BaseModel):
    request_id: str = Field(..., description="Unique identifier for the request")
    original_request: str = Field(..., description="Original marketing request")
    status: str = Field(default="pending", description="Current workflow status")
    selected_departments: Dict[str, Dict] = Field(
        default_factory=dict,
        description="Selected departments and their tasks"
    )
    # Modified to support concurrent updates
    department_responses: Annotated[Dict[str, Dict], operator.ior] = Field(
        default_factory=dict,
        description="Responses from each department"
    )
    summarized_response: Dict = Field(
        default_factory=dict,
        description="Summarized marketing strategy"
    )
    final_response: Dict = Field(
        default_factory=dict,
        description="Final marketing plan"
    )
    errors: Annotated[List[str], operator.add] = Field(
        default_factory=list,
        description="Any errors encountered during processing"
    )
    current_step: str = Field(
        default="initiation",
        description="Current step in the workflow"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

# Department Response Models
class SEOResponse(BaseModel):
    keywords: List[str]
    seo_strategies: List[str]
    metadata_recommendations: Dict[str, str]
    technical_requirements: List[str]
    content_optimization: List[str]
    timeline: Dict[str, str]

class ContentResponse(BaseModel):
    content_themes: List[str]
    content_types: List[str]
    distribution_channels: List[str]
    content_calendar: Dict[str, str]
    resource_requirements: List[str]
    success_metrics: List[str]

class StrategyResponse(BaseModel):
    strategic_goals: List[str]
    target_audience: Dict[str, str]
    channel_strategy: Dict[str, str]
    implementation_plan: List[str]
    success_metrics: List[str]
    budget_allocation: Dict[str, float]

class AdvertisingResponse(BaseModel):
    ad_platforms: List[str]
    campaign_types: List[str]
    targeting_strategy: Dict[str, str]
    budget_allocation: Dict[str, float]
    creative_requirements: List[str]
    performance_targets: Dict[str, str]

class SocialMediaResponse(BaseModel):
    platform_strategy: Dict[str, str]
    content_themes: List[str]
    posting_schedule: Dict[str, str]
    engagement_tactics: List[str]
    hashtag_strategy: List[str]
    success_metrics: Dict[str, str]

class EmailResponse(BaseModel):
    campaign_types: List[str]
    email_sequences: List[str]
    segmentation_strategy: Dict[str, str]
    content_strategy: List[str]
    automation_flows: List[str]
    performance_metrics: Dict[str, str]

class AnalyticsResponse(BaseModel):
    key_metrics: List[str]
    tracking_setup: List[str]
    reporting_framework: Dict[str, str]
    data_collection: List[str]
    analysis_approach: List[str]
    success_criteria: Dict[str, float]

# Summarizer Models
class PhaseTask(BaseModel):
    phase: str
    duration: str
    tasks: List[str]
    dependencies: List[str]

class RiskAssessment(BaseModel):
    risk: str
    impact: str
    mitigation: str

class DepartmentStrategy(BaseModel):
    key_points: List[str]
    implementation: str

class IntegratedStrategy(BaseModel):
    overview: str
    core_objectives: List[str]
    department_strategies: Dict[str, DepartmentStrategy]

class SummarizerResponse(BaseModel):
    integrated_strategy: IntegratedStrategy
    implementation_plan: List[PhaseTask]
    resource_requirements: Dict[str, List[str]]
    timeline: Dict[str, List[str]]
    success_metrics: Dict[str, List[str]]
    risk_assessment: List[RiskAssessment]

    model_config = ConfigDict(arbitrary_types_allowed=True)

# Final Response Model
class FinalResponse(BaseModel):
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    executive_summary: str
    strategic_approach: Dict[str, List[str]]
    department_strategies: Dict[str, Dict[str, Any]]
    timeline: Dict[str, List[Dict[str, str]]]
    expected_outcomes: Dict[str, List[str]]
    key_metrics: Dict[str, Dict[str, str]]
    resource_allocation: Dict[str, List[str]]
    next_steps: List[str]
    estimated_budget: Optional[Dict[str, float]]
    risk_mitigation: List[Dict[str, str]]

    model_config = ConfigDict(arbitrary_types_allowed=True)