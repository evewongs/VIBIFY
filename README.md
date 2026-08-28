# Vibify

> **AI-powered product marketing video generation made simple.**

Vibify transforms a single product image into a short promotional video using AI. Users can choose guided creative settings such as video duration, aspect ratio, camera motion, product movement, lighting, background, effects, and music without needing advanced video-editing or prompt-engineering knowledge.

---

## Table of Contents

* [Overview](#overview)
* [Problem & Motivation](#problem--motivation)
* [Key Features](#key-features)
* [How Vibify Works](#how-vibify-works)
* [System Architecture](#system-architecture)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Installation & Setup](#installation--setup)
* [Running Your First Video](#running-your-first-video)
* [Video Settings](#video-settings)
* [AI Prompt Enhancement](#ai-prompt-enhancement)
* [Multi-Clip Generation](#multi-clip-generation)
* [AI Audio Generation](#ai-audio-generation)
* [Health Check](#health-check)
* [Generation Status](#generation-status)
* [Cancel Generation](#cancel-generation)
* [Generated Files](#generated-files)
* [Troubleshooting](#troubleshooting)
* [Git Ignore](#git-ignore)
* [Quick Start](#quick-start)
* [Target Users](#target-users)
* [Use Cases](#use-cases)
* [Current Limitations](#current-limitations)
* [Future Improvements](#future-improvements)
* [Design Philosophy](#design-philosophy)
* [Project Status](#project-status)

---

# Overview

Vibify is an AI-powered application designed to make product marketing video creation faster, simpler, and more accessible.

Instead of requiring users to have professional video-editing skills or detailed knowledge of AI prompting, Vibify provides a guided interface where users can:

* Upload a product image
* Enter a product name
* Select video duration and aspect ratio
* Select camera motion, product movement, and lighting
* Describe backgrounds, effects, and background motion
* Add text-on-video instructions
* Provide additional creative direction
* Select AI-generated music or upload custom audio
* Generate, preview, save, and download the final MP4 video

Vibify combines:

* HTML, CSS, and Vanilla JavaScript
* Python and FastAPI
* Ollama + Qwen3:8B
* ComfyUI
* MiniMax H3
* ACE Step 1.5 XL Turbo
* FFmpeg

---

# Problem & Motivation

Creating professional marketing videos can be expensive and time-consuming.

Traditional video production may require:

* Professional video-editing software
* Video-editing experience
* Professional production skills
* Powerful hardware
* Knowledge of AI prompt engineering
* Significant production time

Vibify simplifies this process by providing guided creative selections and automatic AI prompt enhancement.

## Main Goals

* Reduce video-production cost
* Reduce production time
* Make AI video generation accessible to non-experts
* Reduce the need for professional video-editing skills
* Simplify AI prompting
* Provide guided creative controls
* Support lower-VRAM generation workflows

---

# Key Features

## Product Image to Marketing Video

Users upload a single product image, which becomes the main visual reference for the generated promotional video.

Supported image formats:

* JPG
* PNG
* WEBP

Maximum upload size:

```text
20 MB
```

---

## Guided Video Customization

Vibify provides predefined settings together with optional custom creative inputs.

### Predefined Settings

* Video Duration
* Frame Size
* Camera Motion
* Product Movement
* Lighting
* Audio Style

### Custom Creative Inputs

* Effects
* Background
* Background Motion
* Text on Video
* Additional Creative Direction

---

## AI Prompt Enhancement

User selections are sent to Ollama running Qwen3:8B.

Qwen3:8B expands the simple settings selected by the user into a more detailed prompt suitable for the MiniMax H3 ComfyUI video-generation workflow.

```text
User Settings
      ↓
FastAPI
      ↓
llm.py
      ↓
Ollama
      ↓
Qwen3:8B
      ↓
Detailed Video Prompt
      ↓
ComfyUI
      ↓
MiniMax H3
```

This allows users to control the creative direction without having to manually write complicated AI video prompts.

---

## Product Identity Preservation

Vibify instructs the AI workflow to preserve visible product characteristics such as:

* Shape
* Proportions
* Colours
* Materials
* Texture
* Stitching
* Logos
* Structure
* Other visible product details

The uploaded product remains the primary subject while the surrounding environment and background can be customized.

> Vibify currently uses AI prompt and workflow control for product preservation rather than a separate traditional segmentation model.

---

## AI Background Customization

Users can describe the desired environment using the **Background** field.

Examples include:

```text
Luxury perfume store
```

```text
Minimal white photography studio
```

```text
Futuristic neon showroom
```

```text
Outdoor tropical environment
```

The **Background Motion** field allows the user to specify environmental movement separately from product movement.

---

## AI Background Music

Available music styles include:

* Cinematic
* Upbeat
* Energetic
* Premium
* Modern
* Corporate
* Ambient
* Playful
* Inspirational
* Futuristic

Users may also upload their own audio.

---

## Multi-Clip Video Generation

Vibify generates approximately 5-second clips.

Longer videos are created by generating multiple clips and combining them.

| Video Duration | Number of Clips |
| -------------- | --------------: |
| 5 seconds      |               1 |
| 10 seconds     |               2 |
| 15 seconds     |               3 |

Each clip can have its own creative direction.

---

## Clip Continuity

For multi-clip videos, Vibify extracts the final frame of the previous clip and uses it as the input image for the next clip.

This helps maintain visual continuity between generated shots.

```text
Clip 1
  ↓
Last Frame
  ↓
Clip 2
  ↓
Last Frame
  ↓
Clip 3
```

---

## Video Regeneration

Users can generate another version while keeping the same product image and selected settings.

This allows multiple creative results to be produced from the same configuration.

---

## Video Library

The current Vibify Library is session-based.

It allows users to:

* Preview generated videos
* View selected generation settings
* Access generated results during the current application session

Persistent Library storage is planned as a future improvement.

---

## Video Download

Final videos are exported as:

```text
MP4
```

---

# How Vibify Works

## 1. Upload Product Image

The user uploads a product image.

Supported formats:

```text
JPG
PNG
WEBP
```

Maximum size:

```text
20 MB
```

## 2. Enter Product Information

The user enters the product name.

## 3. Choose Video Settings

The user selects:

* Duration
* Frame size
* Audio style

## 4. Customize Each Clip

For every clip, the user can configure:

* Camera Motion
* Product Movement
* Lighting
* Effect
* Background
* Background Motion
* Text on Video
* Additional Creative Direction

## 5. Generate

The frontend sends the uploaded product image and generation settings to the FastAPI backend.

## 6. Prompt Enhancement

FastAPI passes the selected settings to `llm.py`.

`llm.py` communicates with Ollama and Qwen3:8B to produce a detailed video-generation prompt.

## 7. Video Generation

The generated prompt and product image are sent to the MiniMax H3 workflow through ComfyUI.

## 8. Clip Continuity

For videos longer than 5 seconds, the final frame of each generated clip is extracted and used as the starting image of the next clip.

## 9. Video Processing

FFmpeg combines multiple clips into a single continuous video.

## 10. Audio Generation / Processing

If an AI music style is selected, ACE Step 1.5 generates background music.

If custom audio is uploaded, the uploaded audio is used instead.

## 11. Final Output

FFmpeg combines the generated video and audio into the final MP4 file.

## 12. Preview / Save / Download

The final result is displayed inside Vibify, where the user can preview, save, download, or regenerate the video.

---

# System Architecture

```text
User
 │
 ├── Product Image
 ├── Product Name
 ├── Duration / Frame Size
 ├── Camera Motion
 ├── Product Movement
 ├── Lighting
 ├── Background / Effects
 ├── Creative Direction
 └── Audio
 │
 ▼
Frontend
HTML / CSS / JavaScript
 │
 ▼
FastAPI Backend
main.py
 │
 ├──────────────► llm.py
 │                  │
 │                  ▼
 │             Ollama
 │                  │
 │                  ▼
 │             Qwen3:8B
 │                  │
 │                  ▼
 │          Detailed AI Prompt
 │
 ▼
ComfyUI
 │
 ├── MiniMax H3 Video Workflow
 │
 └── ACE Step 1.5 Audio Workflow
 │
 ▼
FFmpeg
 │
 ├── Extract Last Frames
 ├── Merge Video Clips
 ├── Process Audio
 └── Create Final MP4
 │
 ▼
outputs/
 │
 ▼
Preview / Save / Download
```

---

# Technology Stack

| Area               | Technology                      |
| ------------------ | ------------------------------- |
| Frontend           | HTML, CSS, Vanilla JavaScript   |
| Backend            | Python, FastAPI, Uvicorn        |
| HTTP Communication | Requests                        |
| Prompt Enhancement | Ollama + Qwen3:8B               |
| Video Generation   | ComfyUI + MiniMax H3            |
| Audio Generation   | ComfyUI + ACE Step 1.5 XL Turbo |
| Media Processing   | FFmpeg                          |
| Output Format      | MP4                             |

---

# Project Structure

The current Vibify project structure is:

```text
Project/
│
├── main.py
├── llm.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── Frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── ffmpeg/
│   └── ffmpeg-9.0.1-essentials_build/
│       └── bin/
│           └── ffmpeg.exe
│
├── ComfyUI/
│   └── Workflow/
│       ├── video minimax h3 i2v_low vram.json
│       └── audio_ace_step1_5_xl_turbo.json
│
├── uploads/
│
└── outputs/
```

## Main Files

### `main.py`

The main FastAPI backend.

Responsibilities include:

* Serving the frontend
* Receiving uploaded product images
* Receiving generation settings
* Calling the prompt-enhancement module
* Communicating with ComfyUI
* Monitoring workflow completion
* Managing multi-clip generation
* Extracting final frames
* Merging generated clips
* Processing audio
* Creating the final MP4
* Serving generated videos
* Handling generation interruption

### `llm.py`

Handles communication with Ollama and Qwen3:8B.

Its purpose is to transform simple user settings into detailed MiniMax H3 video-generation prompts.

### `Frontend/`

Contains the Vibify user interface.

```text
Frontend/
├── index.html
├── styles.css
└── app.js
```

### `ComfyUI/Workflow/`

Contains the ComfyUI workflow JSON files used by Vibify.

```text
ComfyUI/Workflow/
├── video minimax h3 i2v_low vram.json
└── audio_ace_step1_5_xl_turbo.json
```

### `ffmpeg/`

Contains the FFmpeg executable used by the backend.

### `uploads/`

Temporary uploaded product images and related input files are stored here during processing.

### `outputs/`

Generated videos and final MP4 files are stored here.

---

# Installation & Setup

> **Important:** The Vibify frontend and FastAPI backend can run locally after downloading the repository. Full AI generation also requires Ollama and access to a compatible ComfyUI environment containing the required models and custom nodes.

---

## Step 1 — Download the Project

### Option A — Download ZIP

1. Open the GitHub repository
2. Click **Code**
3. Click **Download ZIP**
4. Extract the ZIP
5. Open the `Project` folder

### Option B — Clone with Git

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Project
```

---

## Step 2 — Install Python

Install Python 3.10 or newer.

Check the installed version:

```bash
python --version
```

---

## Step 3 — Create a Virtual Environment

From inside the project folder:

```bash
python -m venv venv
```

### Windows Command Prompt

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should normally show:

```text
(venv)
```

---

## Step 4 — Install Python Dependencies

Install the dependencies:

```bash
pip install -r requirements.txt
```

Recommended `requirements.txt`:

```text
fastapi
uvicorn[standard]
python-multipart
requests
```

---

## Step 5 — Check FFmpeg

FFmpeg is included inside the project:

```text
ffmpeg/
└── ffmpeg-9.0.1-essentials_build/
    └── bin/
        └── ffmpeg.exe
```

The backend should use the FFmpeg executable through a relative project path.

This means the project can be moved to another Windows computer without depending on a personal absolute path such as:

```text
C:\Users\Username\...
```

---

## Step 6 — Install Ollama

Install Ollama on the computer running the Vibify backend.

Verify the installation:

```bash
ollama --version
```

---

## Step 7 — Install Qwen3:8B

Pull the required model:

```bash
ollama pull qwen3:8b
```

Check installed models:

```bash
ollama list
```

Test the model:

```bash
ollama run qwen3:8b
```

Exit the interactive model when testing is complete.

---

## Step 8 — Ollama Configuration

`llm.py` uses:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"
```

Ollama must therefore be running on the same computer as the Vibify FastAPI backend unless `OLLAMA_URL` is changed.

The expected default Ollama API address is:

```text
http://localhost:11434
```

---

## Step 9 — Configure ComfyUI

Inside `main.py`, configure the ComfyUI server:

```python
COMFYUI_HOST = "100.95.194.96"
COMFYUI_PORT = 8188
```

If the ComfyUI server uses another IP address, change the configuration:

```python
COMFYUI_HOST = "YOUR_COMFYUI_IP"
COMFYUI_PORT = 8188
```

The computer running Vibify must be able to connect to this address.

---

## Step 10 — Start ComfyUI

A typical ComfyUI startup command is:

```bash
python main.py --listen 0.0.0.0
```

The exact command may vary depending on the ComfyUI installation.

Confirm that ComfyUI is reachable at:

```text
http://COMFYUI_IP:8188
```

For example:

```text
http://100.95.194.96:8188
```

---

## Step 11 — Required Video Workflow

The required MiniMax H3 workflow must exist at:

```text
ComfyUI/Workflow/video minimax h3 i2v_low vram.json
```

---

## Step 12 — Required Audio Workflow

The required ACE Step workflow must exist at:

```text
ComfyUI/Workflow/audio_ace_step1_5_xl_turbo.json
```

---

## Step 13 — Required ACE Step Models

The audio workflow references models such as:

```text
acestep_v1.5_xl_turbo_bf16.safetensors
qwen_0.6b_ace15.safetensors
qwen_4b_ace15.safetensors
ace_1.5_vae.safetensors
```

These model files must already be installed in the appropriate ComfyUI model directories.

Large AI model files should not be committed to the Vibify GitHub repository.

---

## Step 14 — Required Video Models

The MiniMax H3 models referenced by the video workflow must also be installed in the appropriate ComfyUI model folders.

The exact model files depend on the configured workflow.

Large model files are not included in the GitHub repository.

---

## Step 15 — Start Vibify

Make sure the virtual environment is activated.

Then run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

For development mode with automatic reload:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Step 16 — Open Vibify

Open a browser and go to:

```text
http://127.0.0.1:8000
```

or:

```text
http://localhost:8000
```

> **Important:** Do not open `Frontend/index.html` directly.

> **Important:** Do not use VS Code Live Server for normal Vibify operation.

The frontend should be served through the FastAPI backend.

---

# Running Your First Video

1. Start Ollama
2. Start the required ComfyUI server
3. Start the Vibify FastAPI backend
4. Open `http://127.0.0.1:8000`
5. Click **Start Creating**
6. Sign in or continue as guest
7. Upload a JPG, PNG, or WEBP product image
8. Enter the product name
9. Choose the video duration
10. Choose the frame size
11. Select an audio style or upload custom audio
12. Select Camera Motion
13. Select Product Movement
14. Select Lighting
15. Add optional effects
16. Enter an optional background
17. Enter optional background motion
18. Enter optional text-on-video instructions
19. Enter optional additional creative direction
20. Click **Generate Video**
21. Wait for processing
22. Preview the result
23. Save, download, or regenerate

---

# Video Settings

## Video Duration

Available durations:

* 5 seconds
* 10 seconds
* 15 seconds

---

## Frame Sizes

| Format    | Aspect Ratio | Typical Use              |
| --------- | ------------ | ------------------------ |
| Square    | 1:1          | Instagram posts          |
| Landscape | 16:9         | YouTube / Desktop        |
| Portrait  | 9:16         | TikTok / Instagram Reels |

---

## Camera Motion

Available camera motion options include:

* Slow pan left
* Slow pan right
* Zoom in
* Zoom out
* Orbit
* Static

---

## Product Movement

Available product movement options include:

* Static
* Slow rotate
* Floating drift
* Gentle bounce
* Pulse zoom

---

## Lighting

Available lighting options include:

* Studio soft
* Golden hour
* Neon rim
* Natural diffuse
* High contrast
* Candlelight

---

## Creative Inputs

Users can additionally provide:

### Effect

Optional visual effects for the generated clip.

### Background

Describes the desired environment surrounding the product.

### Background Motion

Describes how the environment should move during the shot.

### Text on Video

Provides instructions for text that should appear in the generated video.

### Additional Creative Direction

Allows the user to provide extra instructions not covered by the predefined settings.

---

# AI Prompt Enhancement

Example user settings:

```text
Camera Motion: Zoom in
Product Movement: Slow rotate
Lighting: Golden hour
Background: Luxury perfume store
```

The frontend sends these settings to FastAPI.

FastAPI passes the settings to `llm.py`.

`llm.py` sends them to Ollama running Qwen3:8B.

```text
Simple User Settings
        ↓
FastAPI
        ↓
llm.py
        ↓
Ollama
        ↓
Qwen3:8B
        ↓
Detailed MiniMax H3 Prompt
```

The prompt-enhancement system also instructs the model to preserve the identity of the uploaded product.

This allows users to control the creative direction without learning advanced prompt engineering.

---

# Multi-Clip Generation

Each generated shot is approximately 5 seconds.

The number of clips depends on the selected duration.

## 5 Seconds

```text
Product Image
      ↓
Shot 1
      ↓
Final Video
```

---

## 10 Seconds

```text
Product Image
      ↓
Shot 1
      ↓
Extract Exact Last Frame
      ↓
Shot 2
      ↓
FFmpeg Merge
      ↓
Final Video
```

---

## 15 Seconds

```text
Product Image
      ↓
Shot 1
      ↓
Extract Exact Last Frame
      ↓
Shot 2
      ↓
Extract Exact Last Frame
      ↓
Shot 3
      ↓
FFmpeg Merge
      ↓
Final Video
```

The final frame from one shot is reused as the input image for the next shot to improve visual continuity.

---

# AI Audio Generation

If the user selects an AI audio preset:

```text
Selected Music Style
        ↓
FastAPI
        ↓
ACE Step Prompt
        ↓
ComfyUI
        ↓
ACE Step 1.5 XL Turbo
        ↓
Generated Audio
        ↓
FFmpeg
        ↓
Final MP4
```

The generated audio duration follows the selected video duration.

---

## Custom Audio

If a user uploads custom audio:

```text
Generated Video
      +
Uploaded Audio
      ↓
FFmpeg
      ↓
Final MP4
```

Custom uploaded audio takes priority over the AI audio preset.

---

# Health Check

Before generating a video, open:

```text
http://127.0.0.1:8000/health
```

A correctly configured system should return something similar to:

```json
{
  "success": true,
  "comfyui_connected": true,
  "ffmpeg_exists": true,
  "video_workflow_exists": true,
  "audio_workflow_exists": true
}
```

The important values should normally be:

```text
true
```

If one of these values is `false`, check the relevant configuration before generating a video.

---

# Generation Status

The Vibify frontend displays the current generation status.

Possible states include:

```text
Waiting
Processing
Done
Failed
```

The progress percentage shown in the frontend is an estimate.

The FastAPI backend separately monitors ComfyUI for actual workflow completion.

---

# Cancel Generation

During processing, users can click:

```text
Cancel Generation
```

The frontend sends:

```text
POST /interrupt
```

FastAPI then forwards the interrupt request to ComfyUI.

---

# Generated Files

Generated videos are stored inside:

```text
outputs/
```

The backend serves generated videos through:

```text
/generated/<filename>.mp4
```

These URLs are used by the frontend to preview and download generated results.

---

# Troubleshooting

## FFmpeg Not Found

Check that the FFmpeg executable exists at:

```text
ffmpeg/
└── ffmpeg-9.0.1-essentials_build/
    └── bin/
        └── ffmpeg.exe
```

If the `/health` endpoint reports:

```json
"ffmpeg_exists": false
```

check the FFmpeg path configured in the backend.

---

## Ollama Error

Check that Ollama is installed:

```bash
ollama --version
```

Check installed models:

```bash
ollama list
```

Make sure this model exists:

```text
qwen3:8b
```

If it is missing:

```bash
ollama pull qwen3:8b
```

Test it manually:

```bash
ollama run qwen3:8b
```

---

## ComfyUI Connection Error

If:

```json
"comfyui_connected": false
```

check the following:

1. Confirm ComfyUI is running
2. Check the ComfyUI IP address in `main.py`
3. Confirm port `8188` is reachable
4. Check Windows Firewall or network firewall settings
5. Confirm both computers can communicate
6. Confirm ComfyUI was started with network access enabled

---

## Video Workflow Not Found

Check:

```text
ComfyUI/Workflow/video minimax h3 i2v_low vram.json
```

The filename must match the path expected by `main.py`.

---

## Audio Workflow Not Found

Check:

```text
ComfyUI/Workflow/audio_ace_step1_5_xl_turbo.json
```

The filename must match the path expected by `main.py`.

---

## Failed to Fetch

Make sure Vibify is opened through FastAPI:

```text
http://127.0.0.1:8000
```

Do not open:

```text
Frontend/index.html
```

directly in the browser.

Do not use VS Code Live Server for normal operation.

---

## ComfyUI Workflow Error

Possible causes include:

* Missing model
* Missing custom node
* Wrong model filename
* Invalid workflow JSON
* GPU memory error
* Invalid node input
* Network connection issue
* Incorrect ComfyUI IP address
* Workflow configuration mismatch

Check the ComfyUI terminal for the detailed error message.

---

## GPU Memory Error

MiniMax H3 video generation can require significant GPU memory.

If generation fails because of VRAM limitations:

* Use the low-VRAM workflow
* Close other GPU-intensive applications
* Reduce unnecessary GPU usage
* Confirm that the correct quantized models are loaded
* Check ComfyUI terminal output for memory-related errors

---

# Git Ignore

The project should contain a `.gitignore` file in the root directory:

```text
Project/
├── .gitignore
├── main.py
├── llm.py
└── ...
```

Recommended `.gitignore`:

```gitignore
# ============================================================
# Vibify .gitignore
# ============================================================


# ------------------------------------------------------------
# Python
# ------------------------------------------------------------

__pycache__/
*.py[cod]
*$py.class
*.pyd
*.so


# ------------------------------------------------------------
# Virtual Environments
# ------------------------------------------------------------

venv/
.venv/
env/
ENV/


# ------------------------------------------------------------
# Environment Variables / Secrets
# ------------------------------------------------------------

.env
.env.*
!.env.example

*.pem
*.key


# ------------------------------------------------------------
# Python Tools / Cache
# ------------------------------------------------------------

.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/


# ------------------------------------------------------------
# IDE / Editor
# ------------------------------------------------------------

.vscode/
.idea/
*.code-workspace


# ------------------------------------------------------------
# Operating System Files
# ------------------------------------------------------------

.DS_Store
Thumbs.db
desktop.ini


# ------------------------------------------------------------
# Vibify Temporary Uploads
# ------------------------------------------------------------

uploads/*
!uploads/.gitkeep


# ------------------------------------------------------------
# Vibify Generated Outputs
# ------------------------------------------------------------

outputs/*
!outputs/.gitkeep


# ------------------------------------------------------------
# Temporary Media Files
# ------------------------------------------------------------

*.tmp
*.temp

temp/
tmp/


# ------------------------------------------------------------
# Logs
# ------------------------------------------------------------

*.log
logs/


# ------------------------------------------------------------
# AI Model Files
# ------------------------------------------------------------

*.safetensors
*.ckpt
*.pt
*.pth
*.bin
*.gguf
*.onnx


# ------------------------------------------------------------
# ComfyUI Generated Files
# ------------------------------------------------------------

ComfyUI/output/
ComfyUI/input/
ComfyUI/temp/


# ------------------------------------------------------------
# Node / Frontend Dependencies
# ------------------------------------------------------------

node_modules/


# ------------------------------------------------------------
# Build / Distribution
# ------------------------------------------------------------

build/
dist/
*.egg-info/


# ------------------------------------------------------------
# Backup Files
# ------------------------------------------------------------

*.bak
*.backup
*~
```

## Keep Empty Upload and Output Folders

Git does not track empty folders.

If you want the following folders to appear after someone clones the repository:

```text
uploads/
outputs/
```

create:

```text
uploads/.gitkeep
outputs/.gitkeep
```

The project structure then becomes:

```text
Project/
│
├── main.py
├── llm.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── Frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── ffmpeg/
│   └── ffmpeg-9.0.1-essentials_build/
│       └── bin/
│           └── ffmpeg.exe
│
├── ComfyUI/
│   └── Workflow/
│       ├── video minimax h3 i2v_low vram.json
│       └── audio_ace_step1_5_xl_turbo.json
│
├── uploads/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
```

---

# Quick Start

For a Windows computer that already has access to the required ComfyUI environment:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Project

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

ollama pull qwen3:8b

uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

Check system status:

```text
http://127.0.0.1:8000/health
```

For full generation, make sure:

```text
Ollama        → Running
Qwen3:8B      → Installed
ComfyUI       → Running and reachable
MiniMax H3    → Installed
ACE Step 1.5  → Installed
FFmpeg        → Available
```

---

# Target Users

Vibify is designed for:

* Marketing teams
* Small businesses
* Online sellers
* Companies and brands
* Product owners
* E-commerce users
* Content creators
* Users without professional video-editing experience

---

# Use Cases

Vibify can be used for:

* Product advertisements
* E-commerce promotional videos
* Social media marketing
* Product launches
* Brand promotions
* Online-store content
* Marketing campaigns
* Short-form advertisements
* Product showcase videos

---

# Current Limitations

The current version of Vibify has several limitations:

* Video generation can take time
* Video durations are currently limited to 5, 10, and 15 seconds
* Only one product image can be uploaded per generation
* The Library is session-based
* Authentication is not fully completed
* AI results may vary between generations
* Full generation requires a correctly configured ComfyUI environment
* The configured ComfyUI server must be reachable from the Vibify backend
* Large AI models are not included in the GitHub repository
* Generation speed depends heavily on available GPU hardware

---

# Future Improvements

Planned improvements include:

* Multiple product-image support
* More duration options
* Persistent Library storage
* Video deletion
* Completed authentication
* User accounts
* Generation history
* More camera motion options
* More product movement options
* More lighting options
* More video styles
* More visual effects
* More music options
* Additional export formats
* Faster generation
* Additional AI video models
* Advanced video-editing controls
* Brand-specific templates
* Cloud storage support
* Improved product consistency
* Generation queue management
* Better progress tracking

---

# Design Philosophy

> **Simple inputs, powerful AI, professional-looking results.**

Vibify is designed to hide the technical complexity of AI video generation while still allowing users to control the creative direction.

The user should not need to understand:

* Complex prompt engineering
* ComfyUI workflow design
* Video model configuration
* FFmpeg commands
* AI audio-generation workflows

Instead, Vibify translates simple creative choices into the technical instructions required by the underlying AI systems.

---

# Project Status

The main Vibify generation workflow is implemented, including:

* Product image upload
* Product name input
* Guided video settings
* Per-clip customization
* Prompt enhancement
* Ollama + Qwen3:8B integration
* AI video generation
* MiniMax H3 integration
* Multi-clip continuity
* Last-frame extraction
* AI audio generation
* ACE Step 1.5 integration
* Custom audio support
* FFmpeg video processing
* Video preview
* Video download
* Generation interruption
* Basic session Library

Some features are still under development, including:

* Full authentication
* Persistent Library storage
* User accounts
* Persistent generation history

---

# Vibify

**AI Product Marketing Video Generation Application**

```text
One Product Image
        ↓
Guided Creative Controls
        ↓
AI Prompt Enhancement
        ↓
AI Video + Audio Generation
        ↓
Professional Marketing Video
```