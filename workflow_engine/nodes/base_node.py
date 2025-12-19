#!/usr/bin/env python3
"""
Base Node - Base class for all workflow nodes
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseNode(ABC):
    """Base class for all workflow nodes"""
    
    def __init__(self, node_config: Dict, config_manager=None):
        self.node_config = node_config
        self.config_manager = config_manager
        self.node_id = node_config.get("id", "unknown")
        self.node_name = node_config.get("name", self.node_id)
        self.parameters = node_config.get("parameters", {})
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the node with input data"""
        pass
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get a parameter value"""
        return self.parameters.get(key, default)
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a value from config manager"""
        if self.config_manager:
            return self.config_manager.get_credential(key)
        return default
