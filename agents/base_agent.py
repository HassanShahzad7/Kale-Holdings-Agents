from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from typing import Dict, Any, Optional
import json
import os
from config.settings import get_settings

settings = get_settings()

class BaseAgent:
    def __init__(
        self,
        role_description: Optional[str] = None
    ):
        openai_config = settings.get_openai_config()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set!")
            
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name=openai_config["model"],
            temperature=openai_config["temperature"],
            max_tokens=openai_config["max_tokens"],
            frequency_penalty=openai_config["frequency_penalty"],
            presence_penalty=openai_config["presence_penalty"],
            top_p=openai_config["top_p"]
        )
        self.chain = None
        self.role_description = role_description

    def setup_chain(self, prompt_template: str) -> None:
        """Set up the processing chain with the given prompt template"""
        if self.role_description:
            prompt_template = f"{self.role_description}\n\n{prompt_template}"
            
        prompt = ChatPromptTemplate.from_template(prompt_template)
        self.chain = prompt | self.llm

    async def _validate_json_response(self, response: str) -> Dict[str, Any]:
        """Validate and parse JSON response"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            try:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
            except:
                return {"error": "Invalid JSON response", "raw_response": response}

    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process the request and return response"""
        if not self.chain:
            raise ValueError("Chain not initialized. Call setup_chain first.")
        
        try:
            response = await self.chain.ainvoke(request)
            content = response.content if hasattr(response, 'content') else str(response)
            return await self._validate_json_response(content)
        except Exception as e:
            return {
                "error": f"Processing failed: {str(e)}",
                "status": "failed"
            }