#!/usr/bin/env python3
"""
YouTube Node - Extract video data and check viral criteria
"""

import re
from typing import Dict, Any
from datetime import datetime, timedelta

from workflow_engine.nodes.base_node import BaseNode

class YouTubeNode(BaseNode):
    """Node for YouTube operations"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute YouTube operation"""
        operation = self.get_parameter("operation", "extract_id")
        
        if operation == "extract_id":
            # Extract YouTube video ID from URL
            url = input_data.get("url", "") or str(input_data)
            
            # Pattern to match YouTube URLs
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
                r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})'
            ]
            
            video_id = None
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    video_id = match.group(1)
                    break
            
            return {
                "video_id": video_id,
                "url": url,
                "video_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else None
            }
        
        elif operation == "check_viral":
            # Check if video meets viral criteria
            views = int(input_data.get("views", 0) or 0)
            published_at = input_data.get("published_at", "")
            min_views_1day = self.get_parameter("min_views_1day", 10000)
            min_views_7day = self.get_parameter("min_views_7day", 50000)
            min_views_30day = self.get_parameter("min_views_30day", 200000)
            
            # Parse published date
            try:
                if isinstance(published_at, str):
                    # Try ISO format
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                else:
                    pub_date = datetime.now()
            except:
                pub_date = datetime.now()
            
            # Calculate days since publication
            days_ago = (datetime.now() - pub_date.replace(tzinfo=None)).days
            
            # Check viral criteria
            is_viral = False
            if days_ago <= 1 and views >= min_views_1day:
                is_viral = True
            elif days_ago <= 7 and views >= min_views_7day:
                is_viral = True
            elif days_ago <= 30 and views >= min_views_30day:
                is_viral = True
            
            return {
                "is_viral": is_viral,
                "views": views,
                "days_ago": days_ago,
                "criteria_met": is_viral,
                **input_data
            }
        
        else:
            return input_data
