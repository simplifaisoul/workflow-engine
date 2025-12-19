# Contributing to Workflow Engine

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes: `python workflow_engine/quick_test.py`
6. Commit: `git commit -m "Add feature: description"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Style

- Follow PEP 8 Python style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

## Adding New Node Types

1. Create a new file in `workflow_engine/nodes/`
2. Inherit from `BaseNode`
3. Implement the `execute` method
4. Register in `workflow_engine/workflow_engine.py`
5. Add to `workflow_engine/nodes/__init__.py`
6. Add example workflow if applicable

Example:

```python
from workflow_engine.nodes.base_node import BaseNode

class MyNode(BaseNode):
    async def execute(self, input_data):
        # Your logic here
        return {"result": "data"}
```

## Testing

- Run quick test: `python workflow_engine/quick_test.py`
- Run validation: `python workflow_engine/validate_setup.py`
- Test your new node type in isolation

## Documentation

- Update README.md if adding features
- Add examples in `workflow_engine/examples/`
- Document new node types

## Questions?

Open an issue for discussion before making large changes.

Thank you for contributing! 🎉