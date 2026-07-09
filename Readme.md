# 🎬 AMD Captivate AI - Intelligent Video Captioning System

An AI-powered video analysis and captioning platform that automatically generates multiple caption styles for videos using advanced computer vision. Built for the **AMD Developer Hackathon 2026**.

**Features:**
- 🤖 AI-generated captions in 4 distinct styles (Formal, Sarcastic, Humorous-Tech, Humorous-NonTech)
- 🎯 Intelligent keyframe extraction with duplicate removal
- 📝 Overall video summaries
- 🎬 SRT subtitle export
- 🐳 Docker batch processing support
- ⚡ Powered by Fireworks AI Qwen 3.7 Plus Vision model



## 🚀 Quick Start

### Option 1: Docker Batch Processing (Recommended for Submission)

```bash
# Pull and run the container
docker run -v /path/to/input:/input -v /path/to/output:/output anadi555/amd_hackathon:latest
```

**Input Format** (`/input/tasks.json`):
```json
[
  {
    "task_id": "video-001",
    "video_url": "https://example.com/video.mp4",
    "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
  }
]
```

**Output Format** (`/output/results.json`):
```json
[
  {
    "task_id": "video-001",
    "captions": {
      "formal": "A detailed professional description...",
      "sarcastic": "A witty, ironic take on the content...",
      "humorous_tech": "Tech-savvy humor with coding references...",
      "humorous_non_tech": "Everyday funny without technical jargon..."
    }
  }
]
```

### Option 2: Web Interface (Development)

```bash
# Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` in your browser.

---

## 📊 System Architecture

```
User/Hackathon → Docker Container
                      ↓
              1. Read /input/tasks.json
                      ↓
              2. Download video from URL
                      ↓
              3. Extract intelligent keyframes
                      ↓
              4. Remove duplicate frames (grayscale diff)
                      ↓
              5. Caption each frame via Fireworks Vision API
                      ↓
              6. Generate overall video summary
                      ↓
              7. Create 4 caption style variations
                      ↓
              8. Write /output/results.json
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **Vision AI** | Fireworks AI (Qwen 3.7 Plus Vision) |
| **Video Processing** | OpenCV, FFmpeg |
| **Frontend** | React 19, Vite, Vanilla CSS |
| **Containerization** | Docker, Docker Hub |
| **API** | REST (FastAPI), JSON |

---

## 📁 Project Structure

```
AMD_Deveoper_Hakathon/
├── backend/
│   ├── main.py              # FastAPI server & endpoints
│   ├── batch_processor.py   # Docker batch processing entry point
│   ├── pipeline.py          # Video processing pipeline
│   ├── video.py             # Frame extraction & duplicate detection
│   ├── caption.py           # Frame captioning
│   ├── summarizer.py        # Video summary generation
│   ├── styles.py            # Multi-style caption generation
│   ├── fireworks.py         # Fireworks Vision API integration
│   ├── config.py            # Configuration & env variables
│   └── prompts.py           # AI prompt engineering
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # React main app
│   │   ├── App.css          # Cyberpunk UI styling
│   │   └── main.jsx         # Entry point
│   └── vite.config.js
│
├── Dockerfile               # Container definition
├── batch_processor.py       # Batch job processor
├── requirements.txt         # Python dependencies
├── example_input.json       # Sample input
├── example_output.json      # Sample output
├── DOCKER_SUBMISSION.md     # Docker deployment guide
└── README.md               # This file
```

---

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10+
- Docker Desktop
- Fireworks AI API Key (free at https://fireworks.ai)
- Node.js 18+ (for frontend development only)

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd AMD_Deveoper_Hakathon

# Create .env file with your credentials
echo "FIREWORKS_API_KEY=your_api_key_here" > .env
echo "MODEL_NAME=accounts/fireworks/models/qwen3p7-plus" >> .env
```

### 2. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Build Docker Image

```bash
docker build -t amd_hackathon:latest .
```

### 4. Test Locally

```bash
# Create test directories
mkdir test-input test-output

# Add test tasks
cat > test-input/tasks.json << 'EOF'
[
  {
    "task_id": "test-001",
    "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
  }
]
EOF

# Run container
docker run -v $(pwd)/test-input:/input -v $(pwd)/test-output:/output anadi555/amd_hackathon:latest

# Check results
cat test-output/results.json
```

---

## 📖 Usage Examples

### Example 1: Single Video Processing

```bash
mkdir my-batch
cat > my-batch/tasks.json << 'EOF'
[
  {
    "task_id": "spiderman-clip",
    "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    "styles": ["formal", "sarcastic"]
  }
]
EOF

docker run -v $(pwd)/my-batch:/input -v $(pwd)/my-batch:/output anadi555/amd_hackathon:latest
cat my-batch/results.json
```

### Example 2: Batch Processing Multiple Videos

```json
[
  {
    "task_id": "video-1",
    "video_url": "https://example.com/video1.mp4",
    "styles": ["formal", "humorous_non_tech"]
  },
  {
    "task_id": "video-2",
    "video_url": "https://example.com/video2.mp4",
    "styles": ["sarcastic", "humorous_tech"]
  },
  {
    "task_id": "video-3",
    "video_url": "https://example.com/video3.mp4",
    "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
  }
]
```

---

## 🎨 Caption Styles Explained

| Style | Purpose | Example |
|-------|---------|---------|
| **Formal** | Professional, structured language for business/news | "An individual crosses an urban intersection during daylight hours." |
| **Sarcastic** | Witty, ironic tone for entertainment | "Oh look, someone's brave enough to cross mid-traffic. How thrilling." |
| **Humorous-Tech** | Tech humor with coding/dev references | `while(crossing) { dodge++; look_both_ways(); }` |
| **Humorous-NonTech** | Everyday funny with no jargon | "Either very brave or very late for pizza." |

---

## 🔑 Key Features

### 1. **Adaptive Keyframe Extraction**
- Intelligently samples 8-30 frames based on video duration
- Not uniform—captures scene changes automatically

### 2. **Duplicate Frame Detection**
- Grayscale pixel difference analysis using OpenCV
- Removes redundant static frames
- Saves bandwidth and API costs

### 3. **Multi-Style Captions**
- Same content, 4 different writing styles
- Perfect for different audiences & platforms
- Powered by Fireworks AI Qwen 3.7 Plus Vision

### 4. **Batch Processing**
- Process multiple videos in one container run
- JSON input/output for easy automation
- Docker containerized for scalability

### 5. **Export Options**
- JSON: Full structured data
- TXT: Human-readable report
- SRT: Standard subtitle format for video players

---

## 📊 Performance Metrics

- **Frame Extraction**: ~2-5 seconds per video
- **Captioning**: ~30-60 seconds (depends on frame count & API)
- **Summary Generation**: ~10 seconds
- **Style Variation**: ~15 seconds
- **Total**: 1-2 minutes per video on average

---

## 🐳 Docker Container Specs

```
Image: anadi555/amd_hackathon:latest
Size: ~1.2GB (Python runtime + dependencies)
Input: /input/tasks.json
Output: /output/results.json
Memory: 2GB minimum, 4GB recommended
CPU: 2 cores minimum
```

---

## 🚨 Troubleshooting

### Container Error: "Input file not found"
```bash
# Verify tasks.json exists in input directory
ls -la test-input/tasks.json

# Ensure correct path in docker run command
docker run -v C:\full\path\to\input:/input ...
```

### API Error: "Model is required but not provided"
```bash
# Check .env file exists and is readable
cat .env
# Should show: FIREWORKS_API_KEY=...
# Should show: MODEL_NAME=accounts/fireworks/models/qwen3p7-plus
```

### JSON Parse Error in Container
```bash
# Validate JSON format
python -m json.tool test-input/tasks.json

# Ensure it's an array, not a single object
# Should start with [ and end with ]
```

### 404 Error for Video URL
```bash
# Test URL is accessible
curl -I https://example.com/video.mp4

# Use public, downloadable URLs only
# Avoid:
#   - Private/auth-required URLs
#   - Expired links
#   - Redirect URLs without final destination
```

---

## 📝 API Endpoints (Web Interface)

```
POST /upload              # Upload video file
POST /caption             # Trigger caption pipeline
POST /extract             # Extract frames
GET  /outputs/{path}      # Serve keyframe images
GET  /video-info          # Get video metadata
```

---

## 📦 Dependencies

### Python Packages
- fastapi >= 0.100.0
- uvicorn >= 0.22.0
- opencv-python-headless >= 4.8.0
- requests >= 2.31.0
- python-dotenv >= 1.0.0
- python-multipart >= 0.0.6

### System Dependencies
- Python 3.11+
- Docker (for containerization)

---

## 🔐 Security & API Keys

⚠️ **Important:**
- Never commit `.env` file with API keys
- Use `.env.template` for configuration reference
- Rotate API keys regularly
- Use IAM roles/secrets in production

```bash
# .env.template (safe to commit)
FIREWORKS_API_KEY=your_key_here
MODEL_NAME=accounts/fireworks/models/qwen3p7-plus
```

---

## 📤 Deployment & Submission

### Docker Hub
```bash
docker tag amd-captivate-ai:latest anadi555/amd_hackathon:latest
docker push anadi555/amd_hackathon:latest
```

**Public Image:** `anadi555/amd_hackathon:latest`

### GitHub Repository
Push all code including:
- ✅ Dockerfile
- ✅ All Python backend files
- ✅ batch_processor.py
- ✅ requirements.txt
- ✅ .env.template (NO secrets)
- ✅ This README

---

## 🎯 Hackathon Submission Checklist

- [x] Docker image built and tested
- [x] Container pushed to Docker Hub (public)
- [x] Reads `/input/tasks.json` on startup
- [x] Writes `/output/results.json` before exit
- [x] All 4 caption styles implemented
- [x] Error handling for API failures
- [x] Batch processing for multiple videos
- [x] Comprehensive documentation
- [x] Example input/output files
- [x] GitHub repository ready

---

## 💡 Future Enhancements

- [ ] Support for multiple video formats (MKV, WebM, etc.)
- [ ] GPU acceleration for faster processing
- [ ] Database for batch job tracking
- [ ] Web dashboard for monitoring
- [ ] Custom caption style templates
- [ ] Subtitle synchronization refinement
- [ ] Multi-language caption generation
- [ ] Real-time streaming support

---

## 📞 Support & Questions

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review example files: `example_input.json`, `example_output.json`
3. Check Docker logs: `docker logs <container-id>`
4. Review `DOCKER_SUBMISSION.md` for deployment details

---

## 📄 License

This project is built for the AMD Developer Hackathon 2026.

---

## 🙏 Acknowledgments

- **Fireworks AI** for the Qwen 3.7 Plus Vision model
- **AMD** for hosting the Developer Hackathon
- **FastAPI** for the backend framework
- **React & Vite** for the frontend stack

---

**Ready to submit? Start with the Docker image:** `anadi555/amd_hackathon:latest`
Open `.env` and insert your API key:
```env
FIREWORKS_API_KEY=your_actual_fireworks_api_key
MODEL_NAME=accounts/fireworks/models/qwen3p7-plus
```

### 3. Start Backend API
Create a Python virtual environment and install packages:
```bash
# Create and activate virtual environment
python -m venv .venv
# On Windows Powershell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the Uvicorn local server
python -m uvicorn backend.main:app --reload --port 8000
```
* Swagger API docs are accessible at: `http://localhost:8000/docs`
* Uploaded videos will sit in `uploads/`, and frames will serve from `outputs/`.

### 4. Start React Frontend
In a new terminal shell:
```bash
cd frontend

# Install package dependencies
npm install

# Start Vite hot-reloading dev server
npm run dev
```
Open `http://localhost:5173` in your browser to view the application.

---

## 🎨 Visual Assets & Design Aesthetic
The application implements premium glassmorphic styling, employing a responsive slate-navy layout highlighted by neon cyan (`#00f2fe`) and neon purple (`#9d4edd`) glowing elements. Actions trigger micro-animations, loading steps visually pulse to illustrate pipeline progress, and keyframes expand into full-scale modal cards when selected.
