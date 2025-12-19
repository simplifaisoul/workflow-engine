#!/usr/bin/env python3
"""
Quick test without API keys - tests basic workflow structure
"""

import asyncio
import json
from workflow_engine.workflow_engine import WorkflowEngine
from workflow_engine.config import WorkflowConfigManager

async def test_basic_workflow():
    """Test basic workflow without API calls"""
    print("=" * 60)
    print("Quick Workflow Test (No API Keys Required)")
    print("=" * 60)
    
    # Initialize
    config = WorkflowConfigManager()
    engine = WorkflowEngine(config)
    
    # Create a simple test workflow (no API calls)
    test_workflow = {
        "name": "Basic Test Workflow",
        "nodes": [
            {
                "id": "trigger_1",
                "name": "Start",
                "type": "trigger",
                "parameters": {
                    "trigger_type": "manual"
                }
            },
            {
                "id": "transform_1",
                "name": "Transform Data",
                "type": "transform",
                "parameters": {
                    "operation": "merge",
                    "merge_data": {"test": "value", "status": "success"}
                }
            },
            {
                "id": "condition_1",
                "name": "Check Condition",
                "type": "condition",
                "parameters": {
                    "condition_type": "equals",
                    "field": "status",
                    "value": "success"
                }
            }
        ],
        "connections": {
            "trigger_1": ["transform_1"],
            "transform_1": ["condition_1"]
        }
    }
    
    # Load workflow
    print("\n📋 Loading workflow...")
    success = engine.load_workflow("basic_test", test_workflow)
    if not success:
        print("❌ Failed to load workflow")
        return
    
    print("✅ Workflow loaded successfully")
    
    # Run workflow
    print("\n🚀 Running workflow...")
    initial_data = {"input": "test data", "status": "success"}
    
    try:
        execution_id = await engine.execute_workflow("basic_test", initial_data)
        print(f"✅ Execution started: {execution_id}")
        
        # Wait for completion
        await asyncio.sleep(2)
        
        # Check status
        status = engine.get_execution_status(execution_id)
        if status:
            print(f"\n📊 Execution Status: {status['status']}")
            
            if status.get("data"):
                print("\n📝 Node Results:")
                for node_id, result in status["data"].items():
                    print(f"\n  Node: {node_id}")
                    if result.get("success"):
                        print(f"    ✅ Success")
                        data = result.get("data", {})
                        if isinstance(data, dict):
                            print(f"    Data keys: {list(data.keys())}")
                            if "condition_result" in data:
                                print(f"    Condition result: {data['condition_result']}")
                    else:
                        print(f"    ❌ Error: {result.get('error')}")
            
            if status.get("errors"):
                print(f"\n⚠️  Errors: {status['errors']}")
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running workflow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_basic_workflow())
