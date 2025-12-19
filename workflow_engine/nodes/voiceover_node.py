#!/usr/bin/env python3
"""
Voiceover Node - Generate voiceovers using text-to-speech
"""

import aiohttp
from typing import Dict, Any
import json

from workflow_engine.nodes.base_node import BaseNode

class VoiceoverNode(BaseNode):
    """Node for text-to-speech/voiceover generation"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute voiceover generation"""
        provider = self.get_parameter("provider", "elevenlabs")
        text = self.get_parameter("text", "")
        voice_id = self.get_parameter("voice_id", "21m00Tcm4TlvDq8ikWAM")  # Default ElevenLabs voice
        model = self.get_parameter("model", "eleven_multilingual_v2")
        
        # Get text from input if not provided
        if not text:
            if isinstance(input_data, dict):
                text = input_data.get("text") or input_data.get("script") or input_data.get("content") or str(input_data)
            else:
                text = str(input_data)
        
        # Get API key
        api_key = None
        if provider == "elevenlabs":
            api_key = self.get_config_value("elevenlabs_api_key") or self.get_parameter("api_key")
        elif provider == "openai":
            api_key = self.get_config_value("openai_api_key") or self.get_parameter("api_key")
        
        if not api_key:
            # For free alternative, we can use browser TTS or local TTS
            # Return a placeholder that indicates free TTS should be used
            return {
                "voiceover_url": "placeholder_audio.mp3",
                "text": text,
                "provider": "free_tts",
                "note": "For free TTS, use: gTTS (Google Text-to-Speech), pyttsx3, or browser-based TTS",
                "audio_file": "voiceover.mp3"
            }
        
        # Use ElevenLabs API
        if provider == "elevenlabs":
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            payload = {
                "text": text,
                "model_id": model,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"ElevenLabs API error: {response.status} - {error_text}")
                    
                    # Save audio to file
                    audio_data = await response.read()
                    audio_file = f"voiceover_{hash(text) % 10000}.mp3"
                    
                    import os
                    os.makedirs("workflows/audio", exist_ok=True)
                    file_path = f"workflows/audio/{audio_file}"
                    
                    with open(file_path, 'wb') as f:
                        f.write(audio_data)
                    
                    return {
                        "voiceover_url": file_path,
                        "audio_file": audio_file,
                        "text": text,
                        "provider": "elevenlabs",
                        "size_bytes": len(audio_data)
                    }
        
        # Use OpenAI TTS
        elif provider == "openai":
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "tts-1",
                "input": text,
                "voice": self.get_parameter("voice", "alloy")
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"OpenAI TTS error: {response.status} - {error_text}")
                    
                    audio_data = await response.read()
                    audio_file = f"voiceover_{hash(text) % 10000}.mp3"
                    
                    import os
                    os.makedirs("workflows/audio", exist_ok=True)
                    file_path = f"workflows/audio/{audio_file}"
                    
                    with open(file_path, 'wb') as f:
                        f.write(audio_data)
                    
                    return {
                        "voiceover_url": file_path,
                        "audio_file": audio_file,
                        "text": text,
                        "provider": "openai",
                        "size_bytes": len(audio_data)
                    }
        
        return {"error": "Voiceover generation failed"}
