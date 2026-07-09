# Docker Batch Processing Submission

This guide explains how to build and submit your Docker container for the batch processing track.

## Overview

Instead of running as a web server, your container processes videos in **batch mode**:
1. Reads a JSON file with video URLs and requested caption styles
2. Downloads and processes each video
3. Outputs results in a structured JSON format

## Requirements

- **Docker** installed
- **Public container registry account** (Docker Hub, GitHub Container Registry, Azure Container Registry, etc.)
- Your **Fireworks API Key** in `.env`

## File Structure

```
Dockerfile              # Container definition
batch_processor.py      # Batch processing entry point
example_input.json      # Sample input format
example_output.json     # Sample output format
build_and_push.sh       # Linux/Mac build script
build_and_push.bat      # Windows build script
```

## Input Format (`/input/tasks.json`)

```json
[
  {
    "task_id": "v1",
    "video_url": "https://storage.example.com/clips/clip1.mp4",
    "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
  }
]
```

**Fields:**
- `task_id`: Unique identifier for this task
- `video_url`: URL to download the video from
- `styles`: Array of caption styles to generate (subset of the 4 available)

## Output Format (`/output/results.json`)

```json
[
  {
    "task_id": "v1",
    "captions": {
      "formal": "...",
      "sarcastic": "...",
      "humorous_tech": "...",
      "humorous_non_tech": "..."
    }
  }
]
```

**Fields:**
- `task_id`: Matches the input task_id
- `captions`: Generated captions for each requested style

## Style Descriptions

- **formal**: Professional, structured language
- **sarcastic**: Witty, ironic, sarcastic tone
- **humorous_tech**: Technical humor with coding/tech references (for tech-savvy audience)
- **humorous_non_tech**: Everyday funny with no technical jargon

## Build & Deploy

### Step 1: Build the Docker Image

**On Windows:**
```bash
.\build_and_push.bat amd-captivate-ai docker.io your-username
```

**On Linux/Mac:**
```bash
./build_and_push.sh amd-captivate-ai docker.io your-username
```

Or manually:
```bash
docker build -t amd-captivate-ai:latest .
```

### Step 2: Tag for Your Registry

```bash
# Docker Hub
docker tag amd-captivate-ai:latest your-username/amd-captivate-ai:latest

# GitHub Container Registry
docker tag amd-captivate-ai:latest ghcr.io/your-username/amd-captivate-ai:latest

# Azure Container Registry
docker tag amd-captivate-ai:latest myregistry.azurecr.io/amd-captivate-ai:latest
```

### Step 3: Login to Registry

```bash
# Docker Hub
docker login

# GitHub Container Registry
docker login ghcr.io

# Azure Container Registry
az acr login --name myregistry
```

### Step 4: Push to Registry

```bash
# Docker Hub
docker push your-username/amd-captivate-ai:latest

# GitHub Container Registry
docker push ghcr.io/your-username/amd-captivate-ai:latest

# Azure Container Registry
docker push myregistry.azurecr.io/amd-captivate-ai:latest
```

## Testing Locally

Before submitting, test your container locally:

### Create input directory with tasks.json
```bash
mkdir -p ./test-input
# Add your tasks.json to ./test-input/
```

### Run the container
```bash
docker run \
  -v ./test-input:/input \
  -v ./test-output:/output \
  your-username/amd-captivate-ai:latest
```

### Check results
```bash
cat ./test-output/results.json
```

## Example Usage

```bash
# Build
docker build -t my-caption-ai:latest .

# Run batch processing
docker run \
  -v /path/to/input:/input \
  -v /path/to/output:/output \
  my-caption-ai:latest

# Results appear in /path/to/output/results.json
```

## Troubleshooting

**Container exits immediately:**
- Check that `/input/tasks.json` exists
- Verify JSON format is correct
- Check Docker logs: `docker logs <container-id>`

**API errors:**
- Verify `.env` has valid `FIREWORKS_API_KEY` and `MODEL_NAME`
- Check Fireworks API key has sufficient credits

**Memory issues:**
- Limit memory: `docker run -m 4g ...`
- Process fewer videos per batch

## Submission Checklist

- [ ] Dockerfile is created and tested
- [ ] Container builds without errors
- [ ] Container is pushed to a **public registry**
- [ ] Container reads `/input/tasks.json`
- [ ] Container writes `/output/results.json`
- [ ] Output format matches specification
- [ ] All 4 caption styles work correctly
- [ ] API errors are handled gracefully
- [ ] Container exits cleanly after processing

## Public Registries

Choose one to push your image:

1. **Docker Hub** (Free, easiest)
   - URL: `docker.io/username/image:tag`

2. **GitHub Container Registry** (Free with GitHub account)
   - URL: `ghcr.io/username/image:tag`

3. **Azure Container Registry** (Free tier available)
   - URL: `registry.azurecr.io/image:tag`

4. **Google Container Registry**
   - URL: `gcr.io/project-id/image:tag`

## Support

For issues, check:
- Example files: `example_input.json`, `example_output.json`
- Backend logs during processing
- Container image logs
