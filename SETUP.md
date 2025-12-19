# Setup Instructions

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd workflow-engine
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install aiohttp
```

### 3. Verify Installation

Run the validation script:

```bash
python workflow_engine/validate_setup.py
```

You should see all imports successful.

### 4. Run Quick Test

Test the engine without API keys:

```bash
python workflow_engine/quick_test.py
```

If this passes, your installation is complete!

## Optional: Configure API Keys

For AI features, create `workflow_config.json`:

```json
{
  "api_keys": {
    "openrouter": "your-key-here"
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

## Next Steps

- Read the [README.md](README.md) for usage examples
- Check [WORKFLOW_ENGINE_SETUP.md](WORKFLOW_ENGINE_SETUP.md) for detailed setup
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for testing instructions

## Troubleshooting

### Python not found
- Install Python from https://www.python.org/downloads/
- Make sure Python is in your PATH

### Module not found errors
- Run: `pip install aiohttp`
- Make sure you're in the project root directory

### Import errors
- Check you're using Python 3.8+
- Verify all files are present
- Run validation script: `python workflow_engine/validate_setup.py`