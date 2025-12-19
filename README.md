# Workflow Engine - Free N8N Alternative

A Python-based workflow automation engine that provides N8N-like functionality for free. Perfect for automating tasks, creating AI workflows, and building YouTube automation pipelines.

## 🚀 Features

- ✅ **Free and Open Source** - No licensing fees
- ✅ **Multiple Node Types** - HTTP, AI (OpenRouter/OpenAI), Transform, Conditions, Triggers, YouTube, Database, Image, Voiceover
- ✅ **Async Execution** - Fast, non-blocking workflow execution
- ✅ **Easy Configuration** - Simple JSON-based workflow definitions
- ✅ **API Key Management** - Secure credential handling
- ✅ **Extensible** - Easy to add custom node types
- ✅ **YouTube Automation** - Complete workflows for AI faceless channels

## 📋 Requirements

- Python 3.8+
- `aiohttp` library

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/simplifaisoul/workflow-engine.git
cd workflow-engine
```

### 2. Install Dependencies

```bash
pip install aiohttp
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

## ⚡ Quick Start

### 1. Configure API Keys (Optional for basic tests)

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
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-key-here"

# Linux/Mac
export OPENROUTER_API_KEY="your-key-here"
```

### 2. Run Quick Test (No API Keys Required)

```bash
python workflow_engine/quick_test.py
```

This tests basic workflow execution without needing any API keys!

### 3. Create Your First Workflow

Create a file `my_workflow.json`:

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
        "prompt": "Say hello in one sentence"
      }
    }
  ],
  "connections": {
    "trigger_1": ["ai_1"]
  }
}
```

### 4. Run the Workflow

```bash
# Load workflow
python -m workflow_engine.main load --workflow-id my_workflow --file my_workflow.json

# Run workflow
python -m workflow_engine.main run --workflow-id my_workflow
```

## 📚 Documentation

- **[Full Setup Guide](WORKFLOW_ENGINE_SETUP.md)** - Complete setup instructions
- **[YouTube Automation Guide](YOUTUBE_AUTOMATION_SETUP.md)** - Automate AI faceless YouTube channels
- **[Testing Guide](TESTING_GUIDE.md)** - How to test the engine
- **[Run Tests](RUN_TESTS.md)** - Detailed testing instructions
- **[Workflow Engine README](workflow_engine/README.md)** - Detailed API documentation

## 🎯 Use Cases

### 1. Basic Workflow Automation
- HTTP requests
- Data transformation
- Conditional logic
- Database operations

### 2. AI-Powered Workflows
- Script generation
- Content creation
- Text processing
- Image descriptions

### 3. YouTube Channel Automation
- Find viral videos
- Generate 3-act story scripts
- Create b-roll images
- Generate voiceovers
- Render videos

See `workflow_engine/examples/youtube_automation/` for complete YouTube automation workflows.

## 🔑 Required API Keys

### For Basic Workflows
- **None required!** Basic workflows work without any API keys.

### For AI Features
- **OpenRouter API Key** (Recommended)
  - Get from: https://openrouter.ai/keys
  - Cost: Pay-per-use (~$0.01-0.05 per request)
  - Set as: `OPENROUTER_API_KEY`

### For YouTube Automation
- **OpenRouter API Key** (Required for script generation)
- **YouTube Data API Key** (Optional, for fetching video data)
- **ElevenLabs API Key** (Optional, free TTS available)
- **Image Generation API** (Optional, free options available)

See [YOUTUBE_AUTOMATION_SETUP.md](YOUTUBE_AUTOMATION_SETUP.md) for complete setup.

## 📖 Example Workflows

### Simple AI Workflow

```json
{
  "name": "Simple AI Workflow",
  "nodes": [
    {
      "id": "trigger_1",
      "type": "trigger",
      "parameters": {"trigger_type": "manual"}
    },
    {
      "id": "ai_1",
      "type": "ai",
      "parameters": {
        "provider": "openrouter",
        "model": "openai/gpt-3.5-turbo",
        "prompt": "Summarize: {{$json.text}}"
      }
    }
  ],
  "connections": {
    "trigger_1": ["ai_1"]
  }
}
```

### HTTP to AI Workflow

```json
{
  "name": "HTTP to AI",
  "nodes": [
    {
      "id": "trigger_1",
      "type": "trigger",
      "parameters": {"trigger_type": "manual"}
    },
    {
      "id": "http_1",
      "type": "http",
      "parameters": {
        "method": "GET",
        "url": "https://api.github.com/repos/microsoft/vscode"
      }
    },
    {
      "id": "ai_1",
      "type": "ai",
      "parameters": {
        "provider": "openrouter",
        "model": "openai/gpt-3.5-turbo",
        "prompt": "Analyze this data: {{$json}}"
      }
    }
  ],
  "connections": {
    "trigger_1": ["http_1"],
    "http_1": ["ai_1"]
  }
}
```

More examples in `workflow_engine/examples/`

## 🧪 Testing

### Quick Test (No API Keys)

```bash
python workflow_engine/quick_test.py
```

### Validate Setup

```bash
python workflow_engine/validate_setup.py
```

### Full Test (Requires OpenRouter Key)

```bash
$env:OPENROUTER_API_KEY="your-key"
python workflow_engine/test_workflow.py
```

## 🏗️ Architecture

```
workflow_engine/
├── __init__.py
├── workflow_engine.py    # Core engine
├── config.py             # Configuration management
├── main.py               # CLI interface
├── nodes/                # Node implementations
│   ├── base_node.py
│   ├── http_node.py
│   ├── ai_node.py
│   ├── transform_node.py
│   ├── trigger_node.py
│   ├── condition_node.py
│   ├── youtube_node.py
│   ├── database_node.py
│   ├── image_node.py
│   └── voiceover_node.py
└── examples/             # Example workflows
    ├── simple_workflow.json
    ├── http_to_ai_workflow.json
    └── youtube_automation/
        ├── find_viral_videos.json
        ├── generate_script.json
        ├── generate_images.json
        ├── generate_voiceover.json
        └── main_orchestrator.json
```

## 🔧 Available Node Types

| Node Type | Description | API Key Required? |
|-----------|-------------|-------------------|
| `trigger` | Workflow entry points | ❌ No |
| `http` | Make HTTP requests | ❌ No |
| `ai` | AI API interactions (OpenRouter/OpenAI) | ✅ Yes |
| `transform` | Data manipulation | ❌ No |
| `condition` | Conditional logic | ❌ No |
| `youtube` | YouTube operations | ❌ No |
| `database` | File-based database | ❌ No |
| `image` | Image generation | ✅ Optional |
| `voiceover` | Text-to-speech | ✅ Optional |

## 💻 Python API Usage

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

## 🎨 Extending the Engine

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

## 📊 Cost Breakdown (YouTube Automation)

Per video cost:
- Script Generation: $0.01-0.05 (OpenRouter)
- Images: $0.00 (free APIs)
- Voiceover: $0.00 (free TTS)
- Video Rendering: $0.00 (FFmpeg local)
- **Total: $0.01-0.05 per video**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this project for any purpose.

## 🆘 Support

- Check the [documentation](workflow_engine/README.md)
- Review [example workflows](workflow_engine/examples/)
- See [troubleshooting guide](TESTING_GUIDE.md)

## ⭐ Features Comparison with N8N

| Feature | N8N | This Engine |
|---------|-----|-------------|
| Cost | Paid/Enterprise | Free |
| Open Source | Partial | Yes |
| Self-Hosted | Yes | Yes |
| Python-based | No | Yes |
| Extensible | Yes | Yes |
| API Integration | Yes | Yes |
| AI Integration | Yes | Yes |

## 🎉 Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install aiohttp`
- [ ] Run quick test: `python workflow_engine/quick_test.py`
- [ ] (Optional) Get OpenRouter API key
- [ ] (Optional) Create `workflow_config.json`
- [ ] Load example workflow
- [ ] Run your first workflow!

---

**Ready to automate!** 🚀 Start with the quick test to verify everything works, then build your own workflows!