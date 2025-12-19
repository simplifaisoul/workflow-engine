#!/usr/bin/env python3
"""
Workflow Engine - Core execution engine for workflows
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

from workflow_engine.nodes.base_node import BaseNode
from workflow_engine.nodes.http_node import HTTPNode
from workflow_engine.nodes.ai_node import AINode
from workflow_engine.nodes.transform_node import TransformNode
from workflow_engine.nodes.trigger_node import TriggerNode
from workflow_engine.nodes.condition_node import ConditionNode
from workflow_engine.nodes.youtube_node import YouTubeNode
from workflow_engine.nodes.database_node import DatabaseNode
from workflow_engine.nodes.image_node import ImageNode
from workflow_engine.nodes.voiceover_node import VoiceoverNode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

class WorkflowEngine:
    """Main workflow execution engine"""
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.workflows: Dict[str, Dict] = {}
        self.executions: Dict[str, Dict] = {}
        self.node_registry = {
            "http": HTTPNode,
            "ai": AINode,
            "transform": TransformNode,
            "trigger": TriggerNode,
            "condition": ConditionNode,
            "youtube": YouTubeNode,
            "database": DatabaseNode,
            "image": ImageNode,
            "voiceover": VoiceoverNode,
        }
        self.running_workflows: Dict[str, asyncio.Task] = {}
    
    def register_node_type(self, node_type: str, node_class):
        """Register a custom node type"""
        self.node_registry[node_type] = node_class
    
    def load_workflow(self, workflow_id: str, workflow_def: Dict):
        """Load a workflow definition"""
        try:
            # Validate workflow structure
            if "nodes" not in workflow_def:
                raise ValueError("Workflow must have 'nodes' array")
            if "connections" not in workflow_def:
                raise ValueError("Workflow must have 'connections' object")
            
            # Validate nodes
            for node in workflow_def["nodes"]:
                if "type" not in node:
                    raise ValueError(f"Node {node.get('id', 'unknown')} missing 'type'")
                if node["type"] not in self.node_registry:
                    raise ValueError(f"Unknown node type: {node['type']}")
            
            self.workflows[workflow_id] = workflow_def
            logger.info(f"Workflow '{workflow_id}' loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading workflow: {e}")
            return False
    
    def load_workflow_from_file(self, workflow_id: str, file_path: str):
        """Load workflow from JSON file"""
        try:
            with open(file_path, 'r') as f:
                workflow_def = json.load(f)
            return self.load_workflow(workflow_id, workflow_def)
        except Exception as e:
            logger.error(f"Error loading workflow from file: {e}")
            return False
    
    async def execute_workflow(self, workflow_id: str, initial_data: Optional[Dict] = None) -> str:
        """Execute a workflow asynchronously"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        if workflow_id in self.running_workflows:
            raise ValueError(f"Workflow '{workflow_id}' is already running")
        
        execution_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create execution task
        task = asyncio.create_task(
            self._execute_workflow_internal(workflow_id, execution_id, initial_data or {})
        )
        self.running_workflows[workflow_id] = task
        
        return execution_id
    
    async def _execute_workflow_internal(self, workflow_id: str, execution_id: str, initial_data: Dict):
        """Internal workflow execution"""
        workflow = self.workflows[workflow_id]
        nodes = workflow["nodes"]
        connections = workflow.get("connections", {})
        
        execution = {
            "id": execution_id,
            "workflow_id": workflow_id,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "data": {},
            "errors": []
        }
        self.executions[execution_id] = execution
        
        try:
            # Find trigger nodes (entry points)
            trigger_nodes = [n for n in nodes if n.get("type") == "trigger"]
            
            if not trigger_nodes:
                # If no triggers, start from first node
                trigger_nodes = [nodes[0]] if nodes else []
            
            # Execute from trigger nodes
            node_data = {}
            for trigger_node in trigger_nodes:
                node_id = trigger_node["id"]
                result = await self._execute_node(trigger_node, initial_data, execution_id)
                node_data[node_id] = result
            
            # Execute connected nodes
            await self._execute_connected_nodes(
                trigger_nodes, nodes, connections, node_data, execution_id
            )
            
            execution["status"] = "completed"
            execution["completed_at"] = datetime.now().isoformat()
            execution["data"] = node_data
            
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            execution["status"] = "error"
            execution["error"] = str(e)
            execution["errors"].append(str(e))
        
        finally:
            if workflow_id in self.running_workflows:
                del self.running_workflows[workflow_id]
        
        return execution
    
    async def _execute_node(self, node: Dict, input_data: Dict, execution_id: str) -> Dict:
        """Execute a single node"""
        node_id = node["id"]
        node_type = node["type"]
        
        logger.info(f"Executing node: {node_id} (type: {node_type})")
        
        try:
            # Get node class
            node_class = self.node_registry.get(node_type)
            if not node_class:
                raise ValueError(f"Unknown node type: {node_type}")
            
            # Create node instance
            node_instance = node_class(node, self.config_manager)
            
            # Execute node
            result = await node_instance.execute(input_data)
            
            return {
                "node_id": node_id,
                "success": True,
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing node {node_id}: {e}")
            return {
                "node_id": node_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_connected_nodes(
        self, 
        source_nodes: List[Dict], 
        all_nodes: List[Dict],
        connections: Dict,
        node_data: Dict,
        execution_id: str
    ):
        """Execute nodes connected to source nodes"""
        visited = set()
        queue = [(node["id"], node_data.get(node["id"], {})) for node in source_nodes]
        
        while queue:
            current_node_id, current_data = queue.pop(0)
            
            if current_node_id in visited:
                continue
            
            visited.add(current_node_id)
            
            # Find connected nodes
            connected_node_ids = connections.get(current_node_id, [])
            
            for connected_node_id in connected_node_ids:
                if connected_node_id in visited:
                    continue
                
                # Find node definition
                connected_node = next(
                    (n for n in all_nodes if n["id"] == connected_node_id), 
                    None
                )
                
                if not connected_node:
                    continue
                
                # Execute connected node
                result = await self._execute_node(connected_node, current_data, execution_id)
                node_data[connected_node_id] = result
                
                # Add to queue if successful
                if result.get("success"):
                    queue.append((connected_node_id, result.get("data", {})))
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict]:
        """Get execution status"""
        return self.executions.get(execution_id)
    
    def stop_workflow(self, workflow_id: str):
        """Stop a running workflow"""
        if workflow_id in self.running_workflows:
            task = self.running_workflows[workflow_id]
            task.cancel()
            del self.running_workflows[workflow_id]
            logger.info(f"Workflow '{workflow_id}' stopped")
            return True
        return False
    
    def list_workflows(self) -> List[str]:
        """List all loaded workflows"""
        return list(self.workflows.keys())
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow definition"""
        return self.workflows.get(workflow_id)
