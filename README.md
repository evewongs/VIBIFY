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

* HTML, CSS, and JavaScript
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

Examples:

```text
Luxury perfume store
```

```text
Minimal white photography studio
```

```text
Futuristic neon showroom
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

This helps improve visual continuity between generated shots.

---

## Video Regeneration

Users can generate another version while keeping the same product image and selected settings.

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

1. **Upload Product Image**

   * JPG, PNG, or WEBP
   * Maximum file size: 20 MB

2. **Enter Product Information**

   * Enter the product name

3. **Choose Video Settings**

   * Duration
   * Frame size
   * Audio style

4. **Customize Each Clip**

   * Camera Motion
   * Product Movement
   * Lighting
   * Effect
   * Background
   * Background Motion
   * Text on Video
   * Additional Creative Direction

5. **Generate**

   * The frontend sends the product image and settings to FastAPI

6. **Prompt Enhancement**

   * FastAPI passes the settings to `llm.py`
   * Qwen3:8B expands the settings into a detailed AI prompt

7. **Video Generation**

   * MiniMax H3 generates the required clip through ComfyUI

8. **Clip Continuity**

   * For longer videos, the final frame of one clip becomes the input image of the next clip

9. **Video Processing**

   * FFmpeg merges the generated clips

10. **Audio Generation / Processing**

    * ACE Step 1.5 generates background music
    * Or uploaded custom audio is used

11. **Final Output**

    * FFmpeg combines video and audio into the final MP4

12. **Preview / Save / Download**

    * The final result is displayed inside Vibify

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
 │               Ollama
 │                  │
 │                  ▼
 │              Qwen3:8B
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
| Frontend           | HTML, CSS, JavaScript   |
| Backend            | Python, FastAPI, Uvicorn        |
| HTTP Communication | Requests                        |
| Prompt Enhancement | Ollama + Qwen3:8B               |
| Video Generation   | ComfyUI + MiniMax H3            |
| Audio Generation   | ComfyUI + ACE Step 1.5 XL Turbo |
| Media Processing   | FFmpeg 9.0.1 Essentials Build   |
| Output Format      | MP4                             |

---

# Project Structure

The GitHub repository is structured as follows:

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

> **Important:** FFmpeg itself is not included in the GitHub repository.

After downloading and extracting the required FFmpeg package, the local project structure must become:

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
│       ├── bin/
│       │   ├── ffmpeg.exe
│       │   ├── ffplay.exe
│       │   └── ffprobe.exe
│       ├── doc/
│       ├── presets/
│       ├── LICENSE
│       └── README.txt
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

The important FFmpeg executable path is:

```text
Project/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe
```

Do not rename the `ffmpeg-9.0.1-essentials_build` folder.

The backend expects this exact directory structure.

---

# Main Files

## `main.py`

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

---

## `llm.py`

Handles communication with Ollama and Qwen3:8B.

Its purpose is to transform simple user settings into detailed MiniMax H3 video-generation prompts.

---

## `Frontend/`

Contains the Vibify user interface.

```text
Frontend/
├── index.html
├── styles.css
└── app.js
```

---

## `ComfyUI/Workflow/`

Contains the ComfyUI workflow JSON files used by Vibify.

```text
ComfyUI/Workflow/
├── video minimax h3 i2v_low vram.json
└── audio_ace_step1_5_xl_turbo.json
```

---

## `ffmpeg/`

The repository contains the `ffmpeg` directory, but the FFmpeg executable package itself is not included.

Users must manually download and extract:

```text
ffmpeg-9.0.1-essentials_build.zip
```

into this directory.

---

## `uploads/`

Temporary uploaded product images and related input files are stored here during processing.

---

## `outputs/`

Generated videos and final MP4 files are stored here.

---

# Installation & Setup

> **Important:** The Vibify frontend and FastAPI backend can run locally after downloading the repository. Full AI generation also requires Ollama, FFmpeg 9.0.1 Essentials Build, and access to a compatible ComfyUI environment containing the required models and custom nodes.

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

Check:

```bash
python --version
```

---

## Step 3 — Create a Virtual Environment

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

After activation, the terminal should normally display:

```text
(venv)
```

---

## Step 4 — Install Python Dependencies

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

# Step 5 — Install FFmpeg 9.0.1

FFmpeg is **not included in this GitHub repository** because the binary package is too large to include as part of the project repository.

Vibify expects one specific FFmpeg build:

```text
ffmpeg-9.0.1-essentials_build
```

### Required Download

Download the Windows Essentials Build:

```text
ffmpeg-9.0.1-essentials_build.zip
```

Use the **FFmpeg 9.0.1 Essentials Build for Windows by Gyan.dev**.

Do not use:

```text
ffmpeg-release-essentials
ffmpeg-git-essentials
ffmpeg-full_build
ffmpeg-8.x
```

for this project setup.

The expected package is specifically:

```text
ffmpeg-9.0.1-essentials_build.zip
```

---

## Step 5.1 — Extract FFmpeg

After downloading:

```text
ffmpeg-9.0.1-essentials_build.zip
```

extract the ZIP file.

The extracted folder should be named:

```text
ffmpeg-9.0.1-essentials_build
```

Inside it you should see:

```text
ffmpeg-9.0.1-essentials_build/
│
├── bin/
│   ├── ffmpeg.exe
│   ├── ffplay.exe
│   └── ffprobe.exe
│
├── doc/
├── presets/
├── LICENSE
└── README.txt
```

---

## Step 5.2 — Move FFmpeg into the Vibify Project

Move the entire extracted folder into:

```text
Project/ffmpeg/
```

The final structure must be:

```text
Project/
└── ffmpeg/
    └── ffmpeg-9.0.1-essentials_build/
        └── bin/
            └── ffmpeg.exe
```

Therefore, the final executable path must be:

```text
Project/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe
```

### Correct

```text
Project/
└── ffmpeg/
    └── ffmpeg-9.0.1-essentials_build/
        └── bin/
            └── ffmpeg.exe
```

### Incorrect

```text
Project/
└── ffmpeg/
    └── ffmpeg-9.0.1-essentials_build/
        └── ffmpeg-9.0.1-essentials_build/
            └── bin/
                └── ffmpeg.exe
```

### Incorrect

```text
Project/
└── ffmpeg/
    └── bin/
        └── ffmpeg.exe
```

### Incorrect

```text
Project/
└── ffmpeg/
    └── ffmpeg-release-essentials/
        └── bin/
            └── ffmpeg.exe
```

> Do not rename the extracted `ffmpeg-9.0.1-essentials_build` folder.

The backend uses this fixed relative directory structure, so placing FFmpeg in the correct location means no changes to `main.py` are required.

---

## Step 5.3 — Verify FFmpeg

From the `Project` directory, run:

### Windows Command Prompt

```bash
ffmpeg\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe -version
```

### Windows PowerShell

```powershell
.\ffmpeg\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe -version
```

If FFmpeg is installed correctly, the terminal should display FFmpeg version information.

The output should indicate FFmpeg 9.0.1.

---

## Step 6 — Install Ollama

Install Ollama on the computer running the Vibify backend.

Verify:

```bash
ollama --version
```

---

## Step 7 — Install Qwen3:8B

```bash
ollama pull qwen3:8b
```

Check installed models:

```bash
ollama list
```

Test:

```bash
ollama run qwen3:8b
```

---

## Step 8 — Ollama Configuration

`llm.py` uses:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"
```

Ollama must be running on the same computer as the Vibify FastAPI backend unless `OLLAMA_URL` is changed.

The expected default Ollama API address is:

```text
http://localhost:11434
```

---

## Step 9 — Configure ComfyUI

Inside `main.py`:

```python
COMFYUI_HOST = "100.95.194.96"
COMFYUI_PORT = 8188
```

If the ComfyUI server uses another IP address:

```python
COMFYUI_HOST = "YOUR_COMFYUI_IP"
COMFYUI_PORT = 8188
```

The Vibify computer must be able to communicate with this address.

---

## Step 10 — Start ComfyUI

A typical ComfyUI startup command is:

```bash
python main.py --listen 0.0.0.0
```

The exact command depends on the ComfyUI installation.

Confirm ComfyUI is reachable at:

```text
http://COMFYUI_IP:8188
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

These must already be installed in the appropriate ComfyUI model folders.

Large AI model files are not included in the GitHub repository.

---

## Step 14 — Required Video Models

The MiniMax H3 models referenced by the video workflow must also be installed in the appropriate ComfyUI model folders.

Large model files are not included in the GitHub repository.

---

## Step 15 — Start Vibify

Make sure the virtual environment is activated.

Run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Development mode:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Step 16 — Open Vibify

Open:

```text
http://127.0.0.1:8000
```

or:

```text
http://localhost:8000
```

> Do not open `Frontend/index.html` directly.

> Do not use VS Code Live Server for normal Vibify operation.

The frontend should be served through FastAPI.

---

# Running Your First Video

Before generating a video, make sure all required services are ready.

```text
Python / FastAPI  → Ready
Ollama            → Running
Qwen3:8B          → Installed
FFmpeg 9.0.1      → Installed in Project/ffmpeg/
ComfyUI           → Running and reachable
MiniMax H3        → Installed
ACE Step 1.5      → Installed
```

Then:

1. Open `http://127.0.0.1:8000`
2. Click **Start Creating**
3. Sign in or continue as guest
4. Upload a JPG, PNG, or WEBP product image
5. Enter the product name
6. Choose the video duration
7. Choose the frame size
8. Select an audio style or upload custom audio
9. Select Camera Motion
10. Select Product Movement
11. Select Lighting
12. Add optional effects
13. Enter an optional background
14. Enter optional background motion
15. Enter optional text-on-video instructions
16. Enter optional additional creative direction
17. Click **Generate Video**
18. Wait for processing
19. Preview the result
20. Save, download, or regenerate

---

# Video Settings

## Video Duration

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

* Slow pan left
* Slow pan right
* Zoom in
* Zoom out
* Orbit
* Static

---

## Product Movement

* Static
* Slow rotate
* Floating drift
* Gentle bounce
* Pulse zoom

---

## Lighting

* Studio soft
* Golden hour
* Neon rim
* Natural diffuse
* High contrast
* Candlelight

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

This allows users to control the creative direction without learning advanced prompt engineering.

---

# Multi-Clip Generation

Each generated shot is approximately 5 seconds.

## 5 Seconds

```text
Product Image
      ↓
Shot 1
      ↓
Final Video
```

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

Before generating, open:

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

If:

```json
"ffmpeg_exists": false
```

make sure the file exists exactly at:

```text
Project/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe
```

---

# Generation Status

The frontend displays:

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

They are served through:

```text
/generated/<filename>.mp4
```

---

# Troubleshooting

## FFmpeg Not Installed

FFmpeg is not included in the GitHub repository.

Download:

```text
ffmpeg-9.0.1-essentials_build.zip
```

Extract it and place the entire folder inside:

```text
Project/ffmpeg/
```

The final executable must be:

```text
Project/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe
```

---

## `ffmpeg_exists` is `false`

If the health check returns:

```json
"ffmpeg_exists": false
```

check your directory structure.

Correct:

```text
Project/
└── ffmpeg/
    └── ffmpeg-9.0.1-essentials_build/
        └── bin/
            └── ffmpeg.exe
```

A common mistake is accidentally creating an extra folder level:

```text
Project/
└── ffmpeg/
    └── ffmpeg-9.0.1-essentials_build/
        └── ffmpeg-9.0.1-essentials_build/
            └── bin/
                └── ffmpeg.exe
```

If this happens, move the inner folder up one level.

---

## Wrong FFmpeg Version

Vibify is configured for:

```text
ffmpeg-9.0.1-essentials_build
```

Do not rename another version to this folder name.

Use the actual FFmpeg 9.0.1 Essentials Build.

Verify with:

```bash
ffmpeg\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe -version
```

---

## Ollama Error

Run:

```bash
ollama list
```

Make sure:

```text
qwen3:8b
```

is installed.

If missing:

```bash
ollama pull qwen3:8b
```

---

## ComfyUI Connection Error

If:

```json
"comfyui_connected": false
```

check:

1. Confirm ComfyUI is running
2. Check the IP address in `main.py`
3. Confirm port `8188` is reachable
4. Check firewall settings
5. Confirm both computers can communicate

---

## Video Workflow Not Found

Check:

```text
ComfyUI/Workflow/video minimax h3 i2v_low vram.json
```

---

## Audio Workflow Not Found

Check:

```text
ComfyUI/Workflow/audio_ace_step1_5_xl_turbo.json
```

---

## Failed to Fetch

Open Vibify through:

```text
http://127.0.0.1:8000
```

Do not open:

```text
Frontend/index.html
```

directly.

Do not use VS Code Live Server for normal operation.

---

## ComfyUI Workflow Error

Possible causes:

* Missing model
* Missing custom node
* Wrong model filename
* Invalid workflow JSON
* GPU memory error
* Invalid node input
* Network connection issue

Check the ComfyUI terminal for the detailed error.

---

## GPU Memory Error

If generation fails because of VRAM limitations:

* Use the low-VRAM workflow
* Close other GPU-intensive applications
* Reduce unnecessary GPU usage
* Confirm the correct quantized models are loaded
* Check the ComfyUI terminal output

---

# Git Ignore

Because FFmpeg is downloaded separately, the FFmpeg build should not be committed to GitHub.

Use the following `.gitignore`:

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
# Python Cache / Tools
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
# FFmpeg
# ------------------------------------------------------------

ffmpeg/ffmpeg-9.0.1-essentials_build/
ffmpeg/*.zip
ffmpeg/*.7z


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

---

## Keep Required Empty Folders

Git does not track empty folders.

To keep these folders in GitHub:

```text
ffmpeg/
uploads/
outputs/
```

create:

```text
ffmpeg/.gitkeep
uploads/.gitkeep
outputs/.gitkeep
```

Therefore, the GitHub repository should contain:

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
│   └── .gitkeep
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

After a user installs FFmpeg locally:

```text
Project/
│
├── ffmpeg/
│   ├── .gitkeep
│   │
│   └── ffmpeg-9.0.1-essentials_build/
│       └── bin/
│           └── ffmpeg.exe
│
└── ...
```

The FFmpeg build remains local and is ignored by Git.

---

# Quick Start

For Windows:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Project

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

ollama pull qwen3:8b
```

Then manually download:

```text
ffmpeg-9.0.1-essentials_build.zip
```

Extract it into:

```text
Project/ffmpeg/
```

Verify that this file exists:

```text
Project/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe
```

Verify from Command Prompt:

```bash
ffmpeg\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe -version
```

Then start Vibify:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

Check:

```text
http://127.0.0.1:8000/health
```

Before generating, confirm:

```text
Ollama               → Running
Qwen3:8B             → Installed
FFmpeg 9.0.1         → Installed
ComfyUI              → Running and reachable
MiniMax H3           → Installed
ACE Step 1.5         → Installed
Video Workflow       → Found
Audio Workflow       → Found
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

* Video generation can take time
* Video durations are currently limited to 5, 10, and 15 seconds
* Only one product image can be uploaded per generation
* The Library is session-based
* Authentication is not fully completed
* AI results may vary between generations
* Full generation requires a correctly configured ComfyUI environment
* The configured ComfyUI server must be reachable from the Vibify backend
* FFmpeg must be downloaded separately
* Large AI models are not included in the GitHub repository
* Generation speed depends heavily on available GPU hardware

---

# Future Improvements

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
