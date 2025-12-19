# Testing Guide for Workflow Engine

## Quick Tests (No API Keys Required)

### 1. Validate Setup

```bash
python workflow_engine/validate_setup.py
```

This checks:
- ✅ All imports work correctly
- ✅ All required files exist
- ✅ Directory structure is correct

### 2. Run Basic Workflow Test

```bash
python workflow_engine/quick_test.py
```

This tests:
- ✅ Workflow loading
- ✅ Node execution (trigger, transform, condition)
- ✅ Data flow between nodes
- ✅ No API keys needed!

## Full Tests (Requires API Keys)

### 3. Test with OpenRouter API

```bash
# Set your OpenRouter key
$env:OPENROUTER_API_KEY="your-key-here"

# Run test
python workflow_engine/test_workflow.py
```

This tests:
- ✅ AI node with OpenRouter
- ✅ Full workflow execution
- ✅ API integration

### 4. Test YouTube Automation Workflows

```bash
# Load and test individual workflows
python -m workflow_engine.main load --workflow-id find_viral --file workflow_engine/examples/youtube_automation/find_viral_videos.json

python -m workflow_engine.main run --workflow-id find_viral --data '{"api_key": "your-youtube-key"}'
```

## Expected Output

### Quick Test Output:
```
============================================================
Quick Workflow Test (No API Keys Required)
============================================================

📋 Loading workflow...
✅ Workflow loaded successfully

🚀 Running workflow...
✅ Execution started: basic_test_20240101_120000

📊 Execution Status: completed

📝 Node Results:

  Node: trigger_1
    ✅ Success
    Data keys: ['triggered_at']

  Node: transform_1
    ✅ Success
    Data keys: ['test', 'status', 'input']

  Node: condition_1
    ✅ Success
    Data keys: ['condition_result', 'field', 'field_value', 'expected_value']
    Condition result: True

============================================================
✅ Test completed successfully!
============================================================
```

## Troubleshooting

### Import Errors
```bash
# Install missing dependencies
pip install aiohttp
```

### Module Not Found
```bash
# Make sure you're in the project root
cd c:\Users\mrads\.cursor\extensions\anysphere.remote-ssh-1.0.34
python workflow_engine/quick_test.py
```

### API Key Errors
- Quick test doesn't need API keys
- Full test requires OpenRouter key
- Set environment variable: `$env:OPENROUTER_API_KEY="your-key"`

## What Each Test Validates

| Test | Validates | Requires API Key? |
|------|-----------|-------------------|
| `validate_setup.py` | Code structure, imports | ❌ No |
| `quick_test.py` | Basic workflow execution | ❌ No |
| `test_workflow.py` | AI integration | ✅ Yes (OpenRouter) |
| Individual workflows | Specific functionality | ✅ Depends on workflow |

## Next Steps After Testing

1. ✅ If quick test passes → Basic engine works!
2. ✅ If validation passes → Setup is correct!
3. ✅ If full test passes → Ready for production!
4. ✅ Load your workflows and start automating!
