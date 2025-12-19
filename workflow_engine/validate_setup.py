#!/usr/bin/env python3
"""
Validation script to check if workflow engine is set up correctly
"""

import sys
import os

def check_imports():
    """Check if all required modules can be imported"""
    print("Checking imports...")
    errors = []
    
    try:
        import asyncio
        print("  ✅ asyncio")
    except ImportError as e:
        errors.append(f"asyncio: {e}")
        print(f"  ❌ asyncio: {e}")
    
    try:
        import aiohttp
        print("  ✅ aiohttp")
    except ImportError as e:
        errors.append(f"aiohttp: {e}")
        print(f"  ❌ aiohttp: {e}")
        print("     Install with: pip install aiohttp")
    
    try:
        from workflow_engine.workflow_engine import WorkflowEngine
        print("  ✅ WorkflowEngine")
    except ImportError as e:
        errors.append(f"WorkflowEngine: {e}")
        print(f"  ❌ WorkflowEngine: {e}")
    
    try:
        from workflow_engine.config import WorkflowConfigManager
        print("  ✅ WorkflowConfigManager")
    except ImportError as e:
        errors.append(f"WorkflowConfigManager: {e}")
        print(f"  ❌ WorkflowConfigManager: {e}")
    
    try:
        from workflow_engine.nodes.base_node import BaseNode
        print("  ✅ BaseNode")
    except ImportError as e:
        errors.append(f"BaseNode: {e}")
        print(f"  ❌ BaseNode: {e}")
    
    try:
        from workflow_engine.nodes.http_node import HTTPNode
        print("  ✅ HTTPNode")
    except ImportError as e:
        errors.append(f"HTTPNode: {e}")
        print(f"  ❌ HTTPNode: {e}")
    
    try:
        from workflow_engine.nodes.ai_node import AINode
        print("  ✅ AINode")
    except ImportError as e:
        errors.append(f"AINode: {e}")
        print(f"  ❌ AINode: {e}")
    
    try:
        from workflow_engine.nodes.youtube_node import YouTubeNode
        print("  ✅ YouTubeNode")
    except ImportError as e:
        errors.append(f"YouTubeNode: {e}")
        print(f"  ❌ YouTubeNode: {e}")
    
    try:
        from workflow_engine.nodes.database_node import DatabaseNode
        print("  ✅ DatabaseNode")
    except ImportError as e:
        errors.append(f"DatabaseNode: {e}")
        print(f"  ❌ DatabaseNode: {e}")
    
    try:
        from workflow_engine.nodes.image_node import ImageNode
        print("  ✅ ImageNode")
    except ImportError as e:
        errors.append(f"ImageNode: {e}")
        print(f"  ❌ ImageNode: {e}")
    
    try:
        from workflow_engine.nodes.voiceover_node import VoiceoverNode
        print("  ✅ VoiceoverNode")
    except ImportError as e:
        errors.append(f"VoiceoverNode: {e}")
        print(f"  ❌ VoiceoverNode: {e}")
    
    return errors

def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    dirs = [
        "workflow_engine",
        "workflow_engine/nodes",
        "workflow_engine/examples",
        "workflow_engine/examples/youtube_automation"
    ]
    
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ (missing)")

def check_files():
    """Check if required files exist"""
    print("\nChecking files...")
    files = [
        "workflow_engine/__init__.py",
        "workflow_engine/workflow_engine.py",
        "workflow_engine/config.py",
        "workflow_engine/main.py",
        "workflow_engine/nodes/__init__.py",
        "workflow_engine/nodes/base_node.py",
        "workflow_engine/nodes/http_node.py",
        "workflow_engine/nodes/ai_node.py",
        "workflow_engine/nodes/youtube_node.py",
        "workflow_engine/nodes/database_node.py",
        "workflow_engine/nodes/image_node.py",
        "workflow_engine/nodes/voiceover_node.py",
        "workflow_engine/examples/youtube_automation/main_orchestrator.json"
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")

def main():
    print("=" * 60)
    print("Workflow Engine Setup Validation")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Check imports
    errors = check_imports()
    
    # Check directories
    check_directories()
    
    # Check files
    check_files()
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("❌ Setup incomplete - some imports failed")
        print("\nTo fix:")
        print("  1. Install dependencies: pip install aiohttp")
        print("  2. Make sure you're in the project root directory")
        return 1
    else:
        print("✅ Setup looks good! All imports successful.")
        print("\nNext steps:")
        print("  1. Set OPENROUTER_API_KEY environment variable")
        print("  2. Run: python workflow_engine/test_workflow.py")
        return 0

if __name__ == "__main__":
    sys.exit(main())
