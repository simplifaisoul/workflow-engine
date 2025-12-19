#!/usr/bin/env python3
"""
Trigger Node - Workflow entry points
"""

from typing import Dict, Any
from datetime import datetime

from workflow_engine.nodes.base_node import BaseNode

class TriggerNode(BaseNode):
    """Node for workflow triggers"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trigger"""
        trigger_type = self.get_parameter("trigger_type", "manual")
        
        if trigger_type == "manual":
            # Manual trigger - just pass through input data
            return input_data or {}
        
        elif trigger_type == "webhook":
            # Webhook trigger - expects input_data from webhook
            return input_data or {}
        
        elif trigger_type == "schedule":
            # Schedule trigger - return current time
            return {
                "triggered_at": datetime.now().isoformat(),
                "trigger_type": "schedule"
            }
        
        elif trigger_type == "event":
            # Event trigger
            event_name = self.get_parameter("event_name", "default")
            return {
                "event": event_name,
                "triggered_at": datetime.now().isoformat(),
                "data": input_data
            }
        
        else:
            return input_data or {}
