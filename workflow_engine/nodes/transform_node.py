#!/usr/bin/env python3
"""
Transform Node - Transform and manipulate data
"""

from typing import Dict, Any
import json

from workflow_engine.nodes.base_node import BaseNode

class TransformNode(BaseNode):
    """Node for data transformation"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data transformation"""
        operation = self.get_parameter("operation", "pass_through")
        
        if operation == "pass_through":
            return input_data
        
        elif operation == "extract_json":
            json_string = self.get_parameter("json_string", "")
            if not json_string and isinstance(input_data, dict):
                json_string = json.dumps(input_data)
            try:
                return json.loads(json_string)
            except:
                return {"error": "Invalid JSON"}
        
        elif operation == "to_json":
            return json.dumps(input_data)
        
        elif operation == "merge":
            merge_data = self.get_parameter("merge_data", {})
            if isinstance(input_data, dict):
                return {**input_data, **merge_data}
            return merge_data
        
        elif operation == "filter":
            filter_key = self.get_parameter("filter_key", "")
            filter_value = self.get_parameter("filter_value", "")
            if isinstance(input_data, dict):
                if filter_key in input_data and input_data[filter_key] == filter_value:
                    return input_data
                return {}
            return input_data
        
        elif operation == "map":
            map_key = self.get_parameter("map_key", "")
            if isinstance(input_data, list):
                return [item.get(map_key) for item in input_data if isinstance(item, dict)]
            elif isinstance(input_data, dict):
                return input_data.get(map_key)
            return None
        
        elif operation == "format_string":
            template = self.get_parameter("template", "{data}")
            if isinstance(input_data, dict):
                return template.format(**input_data)
            return template.format(data=input_data)
        
        else:
            return input_data
