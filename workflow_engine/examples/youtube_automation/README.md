# YouTube Channel Automation Workflows

Complete workflow automation for AI faceless YouTube channels, replicating the N8N workflow from the video.

## Workflows Included

### 1. `find_viral_videos.json`
Finds viral YouTube videos based on view count criteria:
- Checks videos against viral thresholds (10k views in 1 day, 50k in 7 days, 200k in 30 days)
- Filters out duplicates
- Saves eligible videos to database

### 2. `generate_script.json`
Generates 3-act story scripts from YouTube transcripts:
- Takes transcript as input
- Uses AI to convert into compelling 3-act structure
- Includes random character names
- Saves script to database

### 3. `generate_images.json`
Generates b-roll images for videos:
- Creates multiple images (typically 6) based on script scenes
- Can run images in parallel
- Combines all images for video rendering

### 4. `generate_voiceover.json`
Generates voiceovers from script text:
- Converts script to audio using text-to-speech
- Supports ElevenLabs or OpenAI TTS
- Saves audio file for video rendering

### 5. `main_orchestrator.json`
Main workflow that orchestrates the entire process:
- Gets pending videos from database
- Fetches transcript
- Generates script
- Generates images and voiceover in parallel
- Renders final video
- Updates video status

## Required API Keys

### Required:
1. **OpenRouter API Key** ⭐
   - For AI script generation
   - Get from: https://openrouter.ai/keys
   - Set as: `OPENROUTER_API_KEY`

2. **YouTube Data API Key** (Optional but recommended)
   - For fetching video data
   - Get from: https://console.cloud.google.com/apis/credentials
   - Set as: `YOUTUBE_API_KEY` or in workflow config

### Optional (for specific features):
3. **ElevenLabs API Key**
   - For high-quality voiceovers
   - Get from: https://elevenlabs.io/
   - Set as: `ELEVENLABS_API_KEY`
   - **Free alternative:** Use free TTS (gTTS, pyttsx3)

4. **Render API Key** (or alternative video rendering service)
   - For video rendering
   - Options:
     - RenderAPI (paid)
     - NCA Toolkit (free, self-hosted)
     - FFmpeg (free, local)
   - Set as: `RENDER_API_KEY` or configure local rendering

5. **Image Generation API** (Optional)
   - For actual image generation (currently returns descriptions)
   - Free options:
     - Hugging Face Inference API (free tier)
     - Stability AI (free tier available)
     - Replicate API (pay-per-use)
   - Set as: `STABILITY_API_KEY` or `HUGGINGFACE_API_KEY`

## Setup Instructions

### 1. Install Dependencies

```bash
pip install aiohttp gTTS  # gTTS for free TTS
```

### 2. Configure API Keys

Create `workflow_config.json`:

```json
{
  "api_keys": {
    "openrouter": "your-openrouter-key",
    "youtube": "your-youtube-api-key",
    "elevenlabs": "your-elevenlabs-key",
    "render_api": "your-render-api-key"
  }
}
```

### 3. Load Workflows

```bash
# Load main orchestrator
python -m workflow_engine.main load --workflow-id youtube_main --file workflow_engine/examples/youtube_automation/main_orchestrator.json

# Load individual workflows
python -m workflow_engine.main load --workflow-id find_viral --file workflow_engine/examples/youtube_automation/find_viral_videos.json
python -m workflow_engine.main load --workflow-id generate_script --file workflow_engine/examples/youtube_automation/generate_script.json
```

### 4. Run Workflows

```bash
# Run main workflow
python -m workflow_engine.main run --workflow-id youtube_main

# Run individual workflow
python -m workflow_engine.main run --workflow-id find_viral --data '{"api_key": "your-youtube-key"}'
```

## Cost Breakdown (Per Video)

Based on the video, here's the estimated cost:

- **Script Generation (AI):** ~$0.01-0.05 (OpenRouter GPT-4)
- **Image Generation:** Free (if using free APIs) or ~$0.01-0.10
- **Voiceover:** Free (gTTS) or ~$0.01-0.05 (ElevenLabs)
- **Video Rendering:** Free (local FFmpeg) or ~$0.10-0.50 (cloud API)
- **Total:** Under $0.30 per video (as mentioned in video)

## Free Alternatives

### Text-to-Speech:
- **gTTS (Google Text-to-Speech):** Free, unlimited
- **pyttsx3:** Free, offline
- **Edge TTS:** Free, Microsoft

### Image Generation:
- **Hugging Face Inference API:** Free tier available
- **Stability AI:** Free tier available
- **Local models:** Run Stable Diffusion locally (free)

### Video Rendering:
- **FFmpeg:** Free, local rendering
- **NCA Toolkit:** Free, self-hosted
- **MoviePy:** Free Python library

## Database Structure

The workflows use a file-based database (JSON files) stored in `workflows/data/`:

- `videos.json` - Video tracking
- `scripts.json` - Generated scripts
- `voiceovers.json` - Voiceover files
- `images.json` - Generated images

Each record includes:
- `id` - Unique identifier
- `status` - pending, processing, completed, error
- `created_at` - Timestamp
- `updated_at` - Timestamp
- Additional fields specific to each type

## Workflow Flow

```
1. Schedule Trigger (every X hours)
   ↓
2. Get Pending Videos from Database
   ↓
3. Select First Video
   ↓
4. Get YouTube Transcript
   ↓
5. Generate 3-Act Story Script (AI)
   ↓
6. Generate Images (Parallel) + Generate Voiceover (Parallel)
   ↓
7. Render Video (combine images + voiceover)
   ↓
8. Update Video Status in Database
```

## Customization

### Adjust Viral Criteria:
Edit `find_viral_videos.json`:
```json
{
  "min_views_1day": 10000,
  "min_views_7day": 50000,
  "min_views_30day": 200000
}
```

### Change AI Model:
Edit script generation node:
```json
{
  "model": "openai/gpt-3.5-turbo"  // Cheaper option
}
```

### Add More Images:
Edit `generate_images.json` to add more image nodes or increase `num_images`.

## Notes

- The current image generation returns descriptions. For actual images, integrate with Stability AI, Hugging Face, or Replicate.
- Video rendering requires a rendering API or local FFmpeg setup.
- Database is file-based for simplicity. For production, consider SQLite or PostgreSQL.
- All workflows are designed to be cost-effective and use free alternatives where possible.

## Troubleshooting

1. **No API keys:** Set environment variables or add to `workflow_config.json`
2. **Image generation not working:** Integrate actual image API (see notes above)
3. **Video rendering fails:** Set up FFmpeg locally or configure rendering API
4. **Database errors:** Ensure `workflows/data/` directory exists and is writable
