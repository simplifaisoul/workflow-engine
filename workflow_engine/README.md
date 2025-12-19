# Workflow Engine - Free N8N Alternative

A Python-based workflow automation engine that provides N8N-like functionality for free.

## Features

- ✅ **Free and Open Source** - No licensing fees
- ✅ **Multiple Node Types** - HTTP, AI (OpenRouter/OpenAI), Transform, Conditions, Triggers
- ✅ **Async Execution** - Fast, non-blocking workflow execution
- ✅ **Easy Configuration** - Simple JSON-based workflow definitions
- ✅ **API Key Management** - Secure credential handling
- ✅ **Extensible** - Easy to add custom node types

## Installation

```bash
# Install dependencies
pip install aiohttp

# Or add to requirements.txt
echo "aiohttp>=3.9.0" >> requirements.txt
pip install -r requirements.txt
```

## Quick Start

### 1. Configure API Keys

Create `workflow_config.json`:

```json
{
  "api_keys": {
    "openrouter": "your-openrouter-api-key-here",
    "openai": "your-openai-api-key-here",
    "github": "your-github-token-here"
  }
}
```

Or set environment variables:
```bash
export OPENROUTER_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export GITHUB_TOKEN="your-token"
```

### 2. Create a Workflow

Create a JSON file (e.g., `my_workflow.json`):

```json
{
  "name": "My First Workflow",
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
      "name": "AI Processing",
      "type": "ai",
      "parameters": {
        "provider": "openrouter",
        "model": "openai/gpt-3.5-turbo",
        "prompt": "Hello, how are you?"
      }
    }
  ],
  "connections": {
    "trigger_1": ["ai_1"]
  }
}
```

### 3. Run the Workflow

```bash
# Load workflow
python -m workflow_engine.main load --workflow-id my_workflow --file my_workflow.json

# Run workflow
python -m workflow_engine.main run --workflow-id my_workflow

# Check status
python -m workflow_engine.main status --execution-id my_workflow_20240101_120000
```

## Node Types

### Trigger Node
Entry point for workflows.

```json
{
  "id": "trigger_1",
  "type": "trigger",
  "parameters": {
    "trigger_type": "manual"  // or "webhook", "schedule", "event"
  }
}
```

### HTTP Node
Make HTTP requests.

```json
{
  "id": "http_1",
  "type": "http",
  "parameters": {
    "method": "GET",
    "url": "https://api.example.com/data",
    "headers": {},
    "body": {},
    "authentication": "none"  // or "bearer", "basic"
  }
}
```

### AI Node
Interact with AI APIs (OpenRouter, OpenAI).

```json
{
  "id": "ai_1",
  "type": "ai",
  "parameters": {
    "provider": "openrouter",  // or "openai"
    "model": "openai/gpt-3.5-turbo",
    "prompt": "Your prompt here",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

### Transform Node
Transform and manipulate data.

```json
{
  "id": "transform_1",
  "type": "transform",
  "parameters": {
    "operation": "merge",  // or "extract_json", "to_json", "filter", "map", "format_string"
    "merge_data": {"key": "value"}
  }
}
```

### Condition Node
Conditional logic and branching.

```json
{
  "id": "condition_1",
  "type": "condition",
  "parameters": {
    "condition_type": "equals",  // or "not_equals", "greater_than", "contains", etc.
    "field": "status",
    "value": "success"
  }
}
```

## Python API Usage

```python
import asyncio
from workflow_engine.workflow_engine import WorkflowEngine
from workflow_engine.config import WorkflowConfigManager

async def main():
    # Initialize
    config = WorkflowConfigManager()
    engine = WorkflowEngine(config)
    
    # Load workflow
    engine.load_workflow_from_file("my_workflow", "my_workflow.json")
    
    # Run workflow
    execution_id = await engine.execute_workflow("my_workflow", {"text": "Hello"})
    
    # Check status
    await asyncio.sleep(2)
    status = engine.get_execution_status(execution_id)
    print(status)

asyncio.run(main())
```

## Required API Keys

To use this workflow engine, you'll need:

1. **OpenRouter API Key** (for AI nodes with OpenRouter)
   - Get it from: https://openrouter.ai/keys
   - Set in config: `"openrouter": "your-key"` or `OPENROUTER_API_KEY` env var

2. **OpenAI API Key** (optional, if using OpenAI directly)
   - Get it from: https://platform.openai.com/api-keys
   - Set in config: `"openai": "your-key"` or `OPENAI_API_KEY` env var

3. **GitHub Token** (optional, for GitHub API workflows)
   - Get it from: https://github.com/settings/tokens
   - Set in config: `"github": "your-token"` or `GITHUB_TOKEN` env var

4. **Other API Keys** (as needed for your workflows)
   - Add to `workflow_config.json` under `api_keys`

## Example Workflows

See `workflow_engine/examples/` for example workflows:
- `simple_workflow.json` - Basic AI workflow
- `http_to_ai_workflow.json` - HTTP request → AI processing

## Extending the Engine

Add custom node types:

```python
from workflow_engine.nodes.base_node import BaseNode

class MyCustomNode(BaseNode):
    async def execute(self, input_data):
        # Your custom logic here
        return {"result": "custom"}
```

Register it:

```python
engine.register_node_type("custom", MyCustomNode)
```

## License

MIT
