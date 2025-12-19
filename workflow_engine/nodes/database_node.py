#!/usr/bin/env python3
"""
Database Node - Simple file-based database operations
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime

from workflow_engine.nodes.base_node import BaseNode

class DatabaseNode(BaseNode):
    """Node for database operations (file-based for simplicity)"""
    
    def __init__(self, node_config: Dict, config_manager=None):
        super().__init__(node_config, config_manager)
        # Get storage path from config
        if config_manager:
            config = config_manager.get_config()
            self.storage_path = config.get("workflows", {}).get("storage_path", "./workflows/data")
        else:
            self.storage_path = "./workflows/data"
        os.makedirs(self.storage_path, exist_ok=True)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database operation"""
        operation = self.get_parameter("operation", "read")
        table_name = self.get_parameter("table", "default")
        file_path = os.path.join(self.storage_path, f"{table_name}.json")
        
        if operation == "read":
            # Read all records
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return {
                    "records": data,
                    "count": len(data)
                }
            return {"records": [], "count": 0}
        
        elif operation == "read_one":
            # Read one record by filter
            filter_key = self.get_parameter("filter_key", "id")
            filter_value = self.get_parameter("filter_value")
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    records = json.load(f)
                
                for record in records:
                    if record.get(filter_key) == filter_value:
                        return {"record": record, "found": True}
            
            return {"record": None, "found": False}
        
        elif operation == "write":
            # Write/update record
            record = input_data.get("record", input_data)
            record_id = record.get("id") or record.get("video_id") or record.get("url")
            
            if not os.path.exists(file_path):
                records = []
            else:
                with open(file_path, 'r') as f:
                    records = json.load(f)
            
            # Update or add
            updated = False
            for i, r in enumerate(records):
                if r.get("id") == record_id or r.get("video_id") == record_id or r.get("url") == record_id:
                    records[i] = {**r, **record, "id": record_id, "updated_at": datetime.now().isoformat()}
                    updated = True
                    break
            
            if not updated:
                record["id"] = record_id
                record["created_at"] = datetime.now().isoformat()
                records.append(record)
            
            with open(file_path, 'w') as f:
                json.dump(records, f, indent=2)
            
            return {"success": True, "record": record, "updated": updated}
        
        elif operation == "check_exists":
            # Check if record exists
            check_key = self.get_parameter("check_key", "url")
            check_value = input_data.get(check_key) or input_data.get("url") or str(input_data)
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    records = json.load(f)
                
                for record in records:
                    if record.get(check_key) == check_value or record.get("url") == check_value:
                        return {"exists": True, "record": record}
            
            return {"exists": False}
        
        elif operation == "filter":
            # Filter records
            filter_key = self.get_parameter("filter_key", "status")
            filter_value = self.get_parameter("filter_value", "pending")
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    records = json.load(f)
                
                filtered = [r for r in records if r.get(filter_key) == filter_value]
                return {"records": filtered, "count": len(filtered)}
            
            return {"records": [], "count": 0}
        
        else:
            return input_data
