from typing import Dict, List, Any, TypedDict, Annotated, Union
from langgraph.graph import Graph, StateGraph, END
from datetime import datetime
from agents.base_agent import BaseAgent
from agents.ceo_agent import CEOAgent
from agents.summarizer_agent import SummarizerAgent
from utils.logger import logger
from functools import partial
import json
import operator

def choose_latter(a: str, b: str) -> str:
    """Return the second value, implementing a proper reducer signature."""
    return b

class WorkflowState(TypedDict, total=False):
    request_id: str
    original_request: str
    status: Annotated[str, choose_latter]
    selected_departments: Dict[str, Dict]
    department_responses: Annotated[Dict[str, Dict], operator.ior]
    summarized_response: Dict
    final_response: Dict
    errors: Annotated[List[str], operator.add]
    current_step: str

def create_marketing_workflow(
    ceo_agent: CEOAgent,
    department_agents: Dict[str, BaseAgent],
    summarizer_agent: SummarizerAgent
) -> Graph:
    """Create the marketing workflow graph."""
    
    workflow = StateGraph(WorkflowState)
    
    async def route_to_departments(state: Dict) -> Dict[str, Any]:
        """Route initial request to departments."""
        try:
            logger.logger.info(f"CEO Agent processing request: {state['original_request']}")
            departments = await ceo_agent.determine_required_departments(state["original_request"])
            selected = departments.get("selected_departments", {})
            
            logger.logger.info(f"CEO Agent selected departments: {json.dumps(selected, indent=2)}")
            
            if not isinstance(selected, dict):
                raise ValueError("CEO response format invalid")
                
            selected = {k.lower(): v for k, v in selected.items()}
            
            return {
                "selected_departments": selected,
                "department_responses": {},
                "status": "departments_assigned"
            }
        except Exception as e:
            logger.logger.error(f"CEO Process Failed: {str(e)}")
            return {"status": "failed", "errors": [str(e)]}

    async def process_department(state: Dict, department: str) -> Dict[str, Any]:
        """Process department task."""
        logger.log_agent_start(state["request_id"], department)
        try:
            if department in state["selected_departments"]:
                task_info = state["selected_departments"][department]
                logger.logger.info(f"{department.upper()} Agent received task: {json.dumps(task_info, indent=2)}")
                
                response = await department_agents[department].process({
                    "task": task_info["task"],
                    "priority": task_info.get("priority", 1),
                    "context": task_info.get("context", {})
                })
                
                logger.logger.info(f"{department.upper()} Agent response: {json.dumps(response, indent=2)}")
                
                return {
                    "department_responses": {department: response}
                }
            
            logger.logger.info(f"{department.upper()} Agent skipped - not in selected departments")
            return {}
                
        except Exception as e:
            logger.log_agent_error(state["request_id"], department, str(e))
            return {
                "errors": [f"{department} processing failed: {str(e)}"]
            }

    async def join_responses(state: Dict) -> Dict[str, Any]:
        """Join all department responses."""
        logger.logger.info("Starting response join process")
        current_responses = state.get("department_responses", {})
        logger.logger.info(f"Current responses: {json.dumps(current_responses, indent=2)}")
        
        return {
            "status": "responses_collected" if len(current_responses) >= len(state["selected_departments"]) else "processing"
        }

    async def summarize_results(state: Dict) -> Dict[str, Any]:
        """Summarize all department responses."""
        logger.log_agent_start(state["request_id"], "Summarizer")
        try:
            responses = state.get("department_responses", {})
            logger.logger.info(f"Responses to summarize: {json.dumps(responses, indent=2)}")
            
            if len(responses) >= len(state["selected_departments"]):
                logger.logger.info("Starting summarization process")
                
                summary = await summarizer_agent.compile_responses({
                    "responses": responses,
                    "original_request": state["original_request"],
                    "selected_departments": state["selected_departments"]
                })
                
                logger.logger.info(f"Generated summary: {json.dumps(summary, indent=2)}")
                
                return {
                    "summarized_response": summary,
                    "status": "summarized"
                }
            
            logger.logger.warning("Incomplete responses for summarization")
            return {"status": "incomplete"}
            
        except Exception as e:
            logger.logger.error(f"Summarization error: {str(e)}")
            return {
                "errors": [f"Summarization failed: {str(e)}"],
                "status": "failed"
            }

    async def create_final_report(state: Dict) -> Dict[str, Any]:
        """Create final report from CEO."""
        logger.log_agent_start(state["request_id"], "CEO Final Report")
        try:
            if state["status"] == "summarized":
                final_response = await ceo_agent.create_final_response({
                    "original_request": state["original_request"],
                    "summary": state["summarized_response"],
                    "department_selection": state["selected_departments"]
                })
                
                logger.logger.info(f"Generated final response: {json.dumps(final_response, indent=2)}")
                
                return {
                    "final_response": final_response,
                    "status": "completed"
                }
            
            return {"status": "waiting_for_summary"}
            
        except Exception as e:
            logger.logger.error(f"Final report creation error: {str(e)}")
            return {
                "errors": [f"Final report creation failed: {str(e)}"],
                "status": "failed"
            }

    # Create department processors
    department_processors = {
        dept: partial(process_department, department=dept)
        for dept in ["seo", "content", "strategy", "advertising", "social", "email", "analytics"]
    }

    # Add nodes
    workflow.add_node("route", route_to_departments)
    for dept, processor in department_processors.items():
        workflow.add_node(dept, processor)
    workflow.add_node("join", join_responses)
    workflow.add_node("summarize", summarize_results)
    workflow.add_node("finalize", create_final_report)

    # Add edges
    for dept in department_processors:
        workflow.add_edge("route", dept)
        workflow.add_edge(dept, "join")
    
    workflow.add_edge("join", "summarize")
    workflow.add_edge("summarize", "finalize")
    workflow.add_edge("finalize", END)

    workflow.set_entry_point("route")
    
    compiled = workflow.compile()
    logger.logger.info("Workflow compiled successfully")
    return compiled

async def execute_workflow(
    workflow: Graph,
    request_id: str,
    prompt: str
) -> Dict[str, Any]:
    """Execute the marketing workflow."""
    logger.log_request(request_id, prompt)
    
    initial_state = WorkflowState(
        request_id=request_id,
        original_request=prompt,
        status="pending",
        selected_departments={},
        department_responses={},
        summarized_response={},
        final_response={},
        errors=[],
        current_step="start"
    )
    
    try:
        logger.logger.info(f"Starting workflow execution with state: {json.dumps(initial_state, indent=2)}")
        final_state = await workflow.ainvoke(initial_state)
        logger.logger.info(f"Final workflow state: {json.dumps(final_state, indent=2)}")
        
        if final_state["status"] == "failed":
            error_msg = f"Workflow failed: {final_state.get('errors', [])}"
            logger.log_error(request_id, error_msg)
            raise Exception(error_msg)
        
        result = {
            "status": "success",
            "summary": final_state.get("summarized_response", {}),
            "department_responses": final_state.get("department_responses", {})
        }
        logger.logger.info(f"Workflow result: {json.dumps(result, indent=2)}")
        return result
        
    except Exception as e:
        error_msg = f"Workflow execution failed: {str(e)}"
        logger.log_error(request_id, error_msg)
        raise Exception(error_msg)