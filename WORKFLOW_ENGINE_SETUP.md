# Workflow Engine Setup Guide

## 🎯 What You Need

I've created a **free N8N alternative** workflow automation engine for you! Here's what you need to get started:

## 📋 Required API Keys

**Note:** You mentioned you have an "OpenRouter key" but provided an SSH key. Here's what you actually need:

### 1. **OpenRouter API Key** ⭐ (Required for AI workflows)
   - **Get it from:** https://openrouter.ai/keys
   - **What it's for:** AI node operations (GPT-3.5, GPT-4, Claude, etc.)
   - **Cost:** Pay-per-use, very affordable
   - **Set it as:** `OPENROUTER_API_KEY` environment variable or in `workflow_config.json`

### 2. **OpenAI API Key** (Optional - if you want to use OpenAI directly)
   - **Get it from:** https://platform.openai.com/api-keys
   - **What it's for:** Direct OpenAI API access (alternative to OpenRouter)
   - **Set it as:** `OPENAI_API_KEY` environment variable

### 3. **GitHub Token** (Optional - for GitHub API workflows)
   - **Get it from:** https://github.com/settings/tokens
   - **What it's for:** GitHub API operations in workflows
   - **Set it as:** `GITHUB_TOKEN` environment variable

### 4. **Other API Keys** (As needed)
   - Any other APIs you want to use in your workflows
   - Add them to `workflow_config.json` under `api_keys`

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install aiohttp
```

Or if you have requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys

**Option A: Environment Variables (Recommended)**
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-openrouter-key-here"
$env:OPENAI_API_KEY="your-openai-key-here"  # Optional
$env:GITHUB_TOKEN="your-github-token-here"  # Optional
```

**Option B: Config File**
1. Copy `workflow_config.json.example` to `workflow_config.json`
2. Edit and add your keys:
```json
{
  "api_keys": {
    "openrouter": "your-actual-openrouter-api-key-here",
    "openai": "your-openai-key-here",
    "github": "your-github-token-here"
  }
}
```

### Step 3: Test the Workflow Engine

```bash
# Load an example workflow
python -m workflow_engine.main load --workflow-id test --file workflow_engine/examples/simple_workflow.json

# Run it
python -m workflow_engine.main run --workflow-id test --data '{"text": "Hello world"}'
```

## 📝 Creating Your First Workflow

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
        "prompt": "Summarize: {{$json.text}}"
      }
    }
  ],
  "connections": {
    "trigger_1": ["ai_1"]
  }
}
```

Then run:
```bash
python -m workflow_engine.main load --workflow-id my_workflow --file my_workflow.json
python -m workflow_engine.main run --workflow-id my_workflow --data '{"text": "Your text here"}'
```

## 🔑 Getting Your OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Go to https://openrouter.ai/keys
4. Create a new API key
5. Copy it and add to your config

**Important:** The SSH key you provided is for SSH access, not for OpenRouter. You need to get an actual API key from OpenRouter's website.

## 📚 Available Node Types

- **Trigger** - Workflow entry points
- **HTTP** - Make HTTP requests
- **AI** - Use OpenRouter/OpenAI for AI operations
- **Transform** - Data manipulation
- **Condition** - Conditional logic

See `workflow_engine/README.md` for full documentation.

## 🆘 Need Help?

- Check `workflow_engine/README.md` for detailed docs
- See `workflow_engine/examples/` for example workflows
- All node types are documented in the README

## ✨ What Makes This Free?

- ✅ No licensing fees
- ✅ No subscription required
- ✅ Open source
- ✅ Run locally or on your server
- ✅ Only pay for API usage (OpenRouter charges per request, very affordable)

You only pay for what you use with OpenRouter (typically $0.0001-$0.01 per request depending on the model).
