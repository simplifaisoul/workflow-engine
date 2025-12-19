#!/usr/bin/env python3
"""
Workflow Engine - Main CLI and API interface
"""

import asyncio
import json
import sys
import argparse
from pathlib import Path

from workflow_engine.workflow_engine import WorkflowEngine
from workflow_engine.config import WorkflowConfigManager

async def run_workflow(engine: WorkflowEngine, workflow_id: str, data: dict = None):
    """Run a workflow"""
    try:
        execution_id = await engine.execute_workflow(workflow_id, data or {})
        print(f"Workflow execution started: {execution_id}")
        
        # Wait a bit and check status
        await asyncio.sleep(1)
        status = engine.get_execution_status(execution_id)
        if status:
            print(f"Status: {status['status']}")
            if status.get("data"):
                print(f"Results: {json.dumps(status['data'], indent=2)}")
        
        return execution_id
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    parser = argparse.ArgumentParser(description="Workflow Engine - Free N8N Alternative")
    parser.add_argument("command", choices=["run", "list", "load", "status"], help="Command to execute")
    parser.add_argument("--workflow-id", help="Workflow ID")
    parser.add_argument("--file", help="Workflow definition file")
    parser.add_argument("--data", help="Initial data (JSON string)")
    parser.add_argument("--execution-id", help="Execution ID for status check")
    
    args = parser.parse_args()
    
    # Initialize
    config_manager = WorkflowConfigManager()
    engine = WorkflowEngine(config_manager)
    
    if args.command == "load":
        if not args.workflow_id or not args.file:
            print("Error: --workflow-id and --file are required")
            sys.exit(1)
        
        if engine.load_workflow_from_file(args.workflow_id, args.file):
            print(f"Workflow '{args.workflow_id}' loaded successfully")
        else:
            print(f"Failed to load workflow '{args.workflow_id}'")
            sys.exit(1)
    
    elif args.command == "list":
        workflows = engine.list_workflows()
        if workflows:
            print("Loaded workflows:")
            for wf_id in workflows:
                print(f"  - {wf_id}")
        else:
            print("No workflows loaded")
    
    elif args.command == "run":
        if not args.workflow_id:
            print("Error: --workflow-id is required")
            sys.exit(1)
        
        data = {}
        if args.data:
            try:
                data = json.loads(args.data)
            except:
                print("Warning: Invalid JSON data, using empty dict")
        
        await run_workflow(engine, args.workflow_id, data)
    
    elif args.command == "status":
        if not args.execution_id:
            print("Error: --execution-id is required")
            sys.exit(1)
        
        status = engine.get_execution_status(args.execution_id)
        if status:
            print(json.dumps(status, indent=2))
        else:
            print(f"Execution '{args.execution_id}' not found")

if __name__ == "__main__":
    asyncio.run(main())
