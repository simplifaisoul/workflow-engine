#!/usr/bin/env python3
"""
AI Node - Interact with AI APIs (OpenRouter, OpenAI, etc.)
"""

import aiohttp
from typing import Dict, Any
import json

from workflow_engine.nodes.base_node import BaseNode

class AINode(BaseNode):
    """Node for AI API interactions"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI request"""
        provider = self.get_parameter("provider", "openrouter")
        model = self.get_parameter("model", "openai/gpt-3.5-turbo")
        prompt = self.get_parameter("prompt", "")
        messages = self.get_parameter("messages", [])
        temperature = self.get_parameter("temperature", 0.7)
        max_tokens = self.get_parameter("max_tokens", 1000)
        
        # Get API key
        api_key = None
        if provider == "openrouter":
            api_key = self.get_config_value("openrouter_api_key") or self.get_parameter("api_key")
            if not api_key:
                raise ValueError("OpenRouter API key is required")
        elif provider == "openai":
            api_key = self.get_config_value("openai_api_key") or self.get_parameter("api_key")
            if not api_key:
                raise ValueError("OpenAI API key is required")
        
        # Prepare messages
        if not messages and prompt:
            # Simple template replacement for {{$json.field}} syntax
            if isinstance(input_data, dict):
                for key, value in input_data.items():
                    prompt = prompt.replace(f"{{{{$json.{key}}}}}", str(value))
            messages = [{"role": "user", "content": prompt}]
        elif not messages:
            # Try to extract from input_data
            if "message" in input_data:
                messages = [{"role": "user", "content": str(input_data["message"])}]
            elif "text" in input_data:
                messages = [{"role": "user", "content": str(input_data["text"])}]
            else:
                messages = [{"role": "user", "content": str(input_data)}]
        
        # Prepare request
        if provider == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",  # Optional
                "X-Title": "Workflow Engine"  # Optional
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        elif provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"AI API error: {response.status} - {error_text}")
                
                result = await response.json()
                
                # Extract response
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    return {
                        "response": content,
                        "full_response": result,
                        "model": model,
                        "usage": result.get("usage", {})
                    }
                else:
                    return {
                        "response": str(result),
                        "full_response": result
                    }
