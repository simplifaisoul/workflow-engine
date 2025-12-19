# YouTube Channel Automation - Complete Setup Guide

## 🎯 What This Replicates

This replicates the N8N workflow from the video "How I Automate AI Faceless Channels with N8N" that:
- Finds viral YouTube videos automatically
- Generates 3-act story scripts using AI
- Creates b-roll images
- Generates voiceovers
- Renders complete videos
- Tracks everything in a database

**Cost per video: Under $0.30** (as shown in the video)

## 📋 Required API Keys & Services

### ⭐ Required:

1. **OpenRouter API Key** (REQUIRED)
   - **Purpose:** AI script generation (3-act stories)
   - **Get it:** https://openrouter.ai/keys
   - **Cost:** ~$0.01-0.05 per script
   - **Set as:** `OPENROUTER_API_KEY`

### 🔧 Recommended:

2. **YouTube Data API Key** (Recommended)
   - **Purpose:** Fetch video data, transcripts
   - **Get it:** https://console.cloud.google.com/apis/credentials
   - **Cost:** Free (10,000 units/day)
   - **Set as:** `YOUTUBE_API_KEY`

### 💡 Optional (Free Alternatives Available):

3. **ElevenLabs API Key** (Optional - Free TTS available)
   - **Purpose:** High-quality voiceovers
   - **Get it:** https://elevenlabs.io/
   - **Cost:** Free tier available, then ~$0.01-0.05 per voiceover
   - **Free Alternative:** Use gTTS (Google Text-to-Speech) - completely free
   - **Set as:** `ELEVENLABS_API_KEY`

4. **Image Generation API** (Optional - Free options available)
   - **Options:**
     - **Hugging Face Inference API** (Free tier)
     - **Stability AI** (Free tier available)
     - **Replicate API** (Pay-per-use)
   - **Cost:** Free tier or ~$0.01-0.10 per image
   - **Set as:** `STABILITY_API_KEY` or `HUGGINGFACE_API_KEY`

5. **Video Rendering** (Free options available)
   - **Options:**
     - **FFmpeg** (Free, local) ⭐ Recommended
     - **NCA Toolkit** (Free, self-hosted)
     - **RenderAPI** (Paid, cloud)
   - **Cost:** Free if using FFmpeg locally
   - **Set as:** `RENDER_API_KEY` (only if using cloud rendering)

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install aiohttp gTTS
```

For video rendering (FFmpeg):
- **Windows:** Download from https://ffmpeg.org/download.html
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### Step 2: Configure API Keys

**Option A: Environment Variables (Recommended)**

```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-openrouter-key"
$env:YOUTUBE_API_KEY="your-youtube-key"  # Optional
$env:ELEVENLABS_API_KEY="your-elevenlabs-key"  # Optional
```

**Option B: Config File**

Create `workflow_config.json`:

```json
{
  "api_keys": {
    "openrouter": "your-openrouter-key-here",
    "youtube": "your-youtube-api-key",
    "elevenlabs": "your-elevenlabs-key",
    "stability": "your-stability-key",
    "render_api": "your-render-api-key"
  },
  "workflows": {
    "storage_path": "./workflows/data"
  }
}
```

### Step 3: Load Workflows

```bash
# Load main orchestrator
python -m workflow_engine.main load --workflow-id youtube_main --file workflow_engine/examples/youtube_automation/main_orchestrator.json

# Load individual workflows
python -m workflow_engine.main load --workflow-id find_viral --file workflow_engine/examples/youtube_automation/find_viral_videos.json
python -m workflow_engine.main load --workflow-id generate_script --file workflow_engine/examples/youtube_automation/generate_script.json
python -m workflow_engine.main load --workflow-id generate_images --file workflow_engine/examples/youtube_automation/generate_images.json
python -m workflow_engine.main load --workflow-id generate_voiceover --file workflow_engine/examples/youtube_automation/generate_voiceover.json
```

### Step 4: Run Workflows

```bash
# Run main workflow (orchestrates everything)
python -m workflow_engine.main run --workflow-id youtube_main

# Or run individual workflows
python -m workflow_engine.main run --workflow-id find_viral --data '{"api_key": "your-youtube-key"}'
```

## 📊 Cost Breakdown (Per Video)

Based on the video's analysis:

| Component | Service | Cost |
|-----------|---------|------|
| Script Generation | OpenRouter (GPT-4) | $0.01-0.05 |
| Images (6 images) | Free APIs | $0.00 |
| Voiceover | gTTS (free) | $0.00 |
| Video Rendering | FFmpeg (local) | $0.00 |
| **Total** | | **$0.01-0.05** |

With paid services:
- ElevenLabs voiceover: +$0.01-0.05
- Cloud rendering: +$0.10-0.50
- **Total with paid:** Still under $0.30 per video

## 🎬 Workflow Process

1. **Find Viral Videos**
   - Searches YouTube for trending videos
   - Filters by view count criteria (10k/1day, 50k/7days, 200k/30days)
   - Checks for duplicates
   - Saves to database

2. **Generate Script**
   - Fetches video transcript
   - Uses AI to create 3-act story structure
   - Adds random character names
   - Saves script

3. **Generate Assets**
   - **Images:** Creates 6 b-roll images (can run in parallel)
   - **Voiceover:** Converts script to audio
   - Both run simultaneously for speed

4. **Render Video**
   - Combines images + voiceover
   - Creates final MP4 video
   - Updates status in database

## 🔧 Free Alternatives Setup

### Free Text-to-Speech (gTTS)

The workflow supports free TTS automatically. No API key needed!

```python
# Already integrated - just don't set ELEVENLABS_API_KEY
# The workflow will use free TTS automatically
```

### Free Image Generation

**Option 1: Hugging Face (Free)**
1. Get API key: https://huggingface.co/settings/tokens
2. Set: `HUGGINGFACE_API_KEY`
3. Update image node to use Hugging Face API

**Option 2: Local Stable Diffusion**
- Run Stable Diffusion locally (free)
- Update image node to call local API

### Free Video Rendering (FFmpeg)

**Setup FFmpeg:**
1. Install FFmpeg (see Step 1)
2. Create a simple rendering script
3. Update workflow to call FFmpeg instead of cloud API

**Example FFmpeg command:**
```bash
ffmpeg -loop 1 -i image1.jpg -i voiceover.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output.mp4
```

## 📁 Database Structure

All data is stored in `workflows/data/` as JSON files:

- `videos.json` - Video tracking with status
- `scripts.json` - Generated scripts
- `voiceovers.json` - Voiceover metadata
- `images.json` - Image metadata

Example video record:
```json
{
  "id": "video_123",
  "video_id": "dQw4w9WgXcQ",
  "url": "https://youtube.com/watch?v=...",
  "status": "pending",
  "views": 150000,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:05:00"
}
```

## 🎨 Customization

### Adjust Viral Criteria

Edit `find_viral_videos.json`:
```json
{
  "min_views_1day": 5000,    // Lower threshold
  "min_views_7day": 25000,
  "min_views_30day": 100000
}
```

### Change AI Model

Use cheaper model in `generate_script.json`:
```json
{
  "model": "openai/gpt-3.5-turbo"  // Cheaper than GPT-4
}
```

### Add More Images

Edit `generate_images.json` to add more image nodes or increase count.

## ⚠️ Important Notes

1. **Image Generation:** Currently returns descriptions. For actual images, integrate with:
   - Stability AI API
   - Hugging Face Inference API
   - Replicate API
   - Or run Stable Diffusion locally

2. **Video Rendering:** Requires:
   - FFmpeg installed locally, OR
   - Cloud rendering API configured

3. **Database:** Uses file-based JSON storage. For production, consider:
   - SQLite (simple)
   - PostgreSQL (scalable)
   - NoCoDB (as mentioned in video)

4. **YouTube Transcripts:** May require:
   - YouTube Data API for some videos
   - Or use `youtube-transcript-api` Python library (free)

## 🆘 Troubleshooting

**No API keys found:**
- Set environment variables or add to `workflow_config.json`
- Check key names match exactly

**Image generation not working:**
- Integrate actual image API (see notes above)
- Or use local Stable Diffusion

**Video rendering fails:**
- Install FFmpeg
- Or configure cloud rendering API
- Check file paths are correct

**Database errors:**
- Ensure `workflows/data/` directory exists
- Check write permissions

## 📚 Additional Resources

- **Workflow Examples:** `workflow_engine/examples/youtube_automation/`
- **Full Documentation:** `workflow_engine/README.md`
- **Main Setup Guide:** `WORKFLOW_ENGINE_SETUP.md`

## 🎉 You're Ready!

With just an **OpenRouter API key**, you can start automating your YouTube channel! All other services have free alternatives.

**Minimum setup:**
1. Get OpenRouter key
2. Install dependencies
3. Load workflows
4. Run!

The system will use free alternatives for everything else automatically.
