#!/usr/bin/env python3
"""
Test script for workflow engine
"""

import asyncio
import json
from workflow_engine.workflow_engine import WorkflowEngine
from workflow_engine.config import WorkflowConfigManager

async def test_simple_workflow():
    """Test a simple workflow"""
    print("=" * 50)
    print("Testing Workflow Engine")
    print("=" * 50)
    
    # Initialize
    config = WorkflowConfigManager()
    engine = WorkflowEngine(config)
    
    # Check if OpenRouter key is configured
    openrouter_key = config.get_credential("openrouter")
    if not openrouter_key:
        print("\n⚠️  WARNING: OpenRouter API key not found!")
        print("Please set OPENROUTER_API_KEY environment variable or")
        print("add it to workflow_config.json")
        print("\nYou can get a key from: https://openrouter.ai/keys")
        return
    
    print(f"\n✅ OpenRouter API key found: {openrouter_key[:10]}...")
    
    # Create a simple test workflow
    test_workflow = {
        "name": "Test Workflow",
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
                "id": "ai_1",
                "name": "AI Test",
                "type": "ai",
                "parameters": {
                    "provider": "openrouter",
                    "model": "openai/gpt-3.5-turbo",
                    "prompt": "Say hello in one sentence"
                }
            }
        ],
        "connections": {
            "trigger_1": ["ai_1"]
        }
    }
    
    # Load workflow
    engine.load_workflow("test", test_workflow)
    print("\n✅ Workflow loaded")
    
    # Run workflow
    print("\n🚀 Running workflow...")
    execution_id = await engine.execute_workflow("test", {"test": "data"})
    print(f"Execution ID: {execution_id}")
    
    # Wait for completion
    await asyncio.sleep(3)
    
    # Check status
    status = engine.get_execution_status(execution_id)
    if status:
        print(f"\n📊 Status: {status['status']}")
        if status.get("data"):
            print("\nResults:")
            for node_id, result in status["data"].items():
                print(f"\n  Node: {node_id}")
                if result.get("success"):
                    ai_response = result.get("data", {}).get("response", "No response")
                    print(f"    ✅ Success")
                    print(f"    Response: {ai_response[:100]}...")
                else:
                    print(f"    ❌ Error: {result.get('error')}")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_simple_workflow())
