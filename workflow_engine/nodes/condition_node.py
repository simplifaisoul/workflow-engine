#!/usr/bin/env python3
"""
Condition Node - Conditional logic and branching
"""

from typing import Dict, Any

from workflow_engine.nodes.base_node import BaseNode

class ConditionNode(BaseNode):
    """Node for conditional logic"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute condition"""
        condition_type = self.get_parameter("condition_type", "equals")
        field = self.get_parameter("field", "")
        value = self.get_parameter("value", "")
        
        # Get field value from input
        field_value = None
        if field:
            if isinstance(input_data, dict):
                field_value = input_data.get(field)
            else:
                field_value = input_data
        
        # Evaluate condition
        result = False
        
        if condition_type == "equals":
            result = str(field_value) == str(value)
        elif condition_type == "not_equals":
            result = str(field_value) != str(value)
        elif condition_type == "greater_than":
            try:
                result = float(field_value) > float(value)
            except:
                result = False
        elif condition_type == "less_than":
            try:
                result = float(field_value) < float(value)
            except:
                result = False
        elif condition_type == "contains":
            result = str(value) in str(field_value)
        elif condition_type == "not_contains":
            result = str(value) not in str(field_value)
        elif condition_type == "exists":
            result = field_value is not None
        elif condition_type == "not_exists":
            result = field_value is None
        
        return {
            "condition_result": result,
            "field": field,
            "field_value": field_value,
            "expected_value": value,
            "condition_type": condition_type,
            "data": input_data
        }
