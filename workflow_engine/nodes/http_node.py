#!/usr/bin/env python3
"""
HTTP Node - Make HTTP requests
"""

import aiohttp
from typing import Dict, Any
import json

from workflow_engine.nodes.base_node import BaseNode

class HTTPNode(BaseNode):
    """Node for making HTTP requests"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute HTTP request"""
        method = self.get_parameter("method", "GET").upper()
        url = self.get_parameter("url", "")
        headers = self.get_parameter("headers", {})
        body = self.get_parameter("body", {})
        auth_type = self.get_parameter("authentication", "none")
        
        if not url:
            raise ValueError("URL is required for HTTP node")
        
        # Handle authentication
        if auth_type == "bearer":
            token = self.get_config_value("bearer_token") or self.get_parameter("bearer_token")
            if token:
                headers["Authorization"] = f"Bearer {token}"
        elif auth_type == "basic":
            username = self.get_parameter("username") or self.get_config_value("http_username")
            password = self.get_parameter("password") or self.get_config_value("http_password")
            if username and password:
                import base64
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                headers["Authorization"] = f"Basic {credentials}"
        
        # Prepare body
        body_data = None
        if method in ["POST", "PUT", "PATCH"] and body:
            if isinstance(body, str):
                body_data = body
            else:
                body_data = json.dumps(body)
                headers.setdefault("Content-Type", "application/json")
        
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                data=body_data
            ) as response:
                response_data = {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": await response.text()
                }
                
                # Try to parse JSON
                try:
                    response_data["json"] = await response.json()
                except:
                    pass
                
                return response_data
