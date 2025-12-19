#!/usr/bin/env python3
"""
Configuration Manager for Workflow Engine
"""

import os
import json
from typing import Dict, Optional

class WorkflowConfigManager:
    """Manages API keys and configuration for workflows"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            base_dir = os.path.dirname(__file__)
            config_path = os.path.join(base_dir, "..", "workflow_config.json")
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file or environment"""
        config = {
            "api_keys": {
                "openrouter": os.getenv("OPENROUTER_API_KEY"),
                "openai": os.getenv("OPENAI_API_KEY"),
                "github": os.getenv("GITHUB_TOKEN"),
            },
            "http": {
                "default_headers": {},
                "timeout": 30
            },
            "workflows": {
                "storage_path": "./workflows"
            }
        }
        
        # Load from file if exists
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    # Merge with defaults
                    if "api_keys" in file_config:
                        config["api_keys"].update(file_config["api_keys"])
                    if "http" in file_config:
                        config["http"].update(file_config["http"])
                    if "workflows" in file_config:
                        config["workflows"].update(file_config["workflows"])
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return config
    
    def get_credential(self, key: str) -> Optional[str]:
        """Get an API key or credential"""
        # Check api_keys first
        if key in self.config.get("api_keys", {}):
            return self.config["api_keys"][key]
        
        # Check environment variables
        env_key = key.upper().replace("-", "_")
        return os.getenv(env_key)
    
    def set_credential(self, key: str, value: str):
        """Set an API key or credential"""
        if "api_keys" not in self.config:
            self.config["api_keys"] = {}
        self.config["api_keys"][key] = value
        self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get_config(self) -> Dict:
        """Get full configuration"""
        return self.config.copy()
