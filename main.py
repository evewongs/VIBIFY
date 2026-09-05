from pathlib import Path
import json
import uuid
import time
import subprocess
import shutil
from typing import Any

import requests

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    HTTPException,
)

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from llm import generate_prompt


# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_DIR = BASE_DIR / "Frontend"
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

LIBRARY_FILE = BASE_DIR / "library.json"

WORKFLOW_DIR = (
    BASE_DIR /
    "ComfyUI" /
    "Workflow"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

WORKFLOW_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

if not LIBRARY_FILE.exists():
    LIBRARY_FILE.write_text(
        json.dumps({"videos": []}, indent=2),
        encoding="utf-8",
    )

# =============================================================================
# LIBRARY
# =============================================================================

def load_library() -> dict:

    try:

        with open(
            LIBRARY_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(
                file
            )

    except Exception:

        data = {
            "videos": []
        }

    if not isinstance(
        data,
        dict,
    ):

        data = {
            "videos": []
        }

    if not isinstance(
        data.get("videos"),
        list,
    ):

        data["videos"] = []

    return data


def save_library(
    data: dict,
):

    with open(
        LIBRARY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

# =============================================================================
# WORKFLOW FILES
# =============================================================================

VIDEO_WORKFLOW_FILE = (
    WORKFLOW_DIR /
    "video minimax h3 i2v_low vram.json"
)

AUDIO_WORKFLOW_FILE = (
    WORKFLOW_DIR /
    "audio_ace_step1_5_xl_turbo.json"
)


# =============================================================================
# COMFYUI
# =============================================================================

COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8188

COMFYUI_URL = (
    f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"
)

COMFYUI_POLL_INTERVAL = 2.0
COMFYUI_TIMEOUT = 60 * 60


# =============================================================================
# FFMPEG
# =============================================================================

FFMPEG_PATH = (
    BASE_DIR /
    "ffmpeg" /
    "ffmpeg-9.0.1-essentials_build" /
    "bin" /
    "ffmpeg.exe"
)


# =============================================================================
# VIDEO SETTINGS
# =============================================================================

SHOT_DURATION = 5


# =============================================================================
# TERMINAL COLORS
# =============================================================================

RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"
GRAY = "\033[90m"


# =============================================================================
# TERMINAL HELPERS
# =============================================================================

def terminal_title(
    title: str,
    color: str = CYAN,
):

    print()
    print(
        color +
        "=" * 80 +
        RESET
    )

    print(
        color +
        BOLD +
        title +
        RESET
    )

    print(
        color +
        "=" * 80 +
        RESET
    )

    print()


def terminal_value(
    label: str,
    value: Any,
    color: str = WHITE,
):

    print(
        f"{BOLD}{label}:{RESET}"
    )

    print(
        f"{color}{value}{RESET}"
    )

    print()


def terminal_prompt(
    title: str,
    prompt: str,
    color: str = WHITE,
):

    print()
    print(
        color +
        "=" * 80 +
        RESET
    )

    print(
        color +
        BOLD +
        title +
        RESET
    )

    print(
        color +
        "-" * 80 +
        RESET
    )

    print(prompt)

    print(
        color +
        "-" * 80 +
        RESET
    )

    print()


# =============================================================================
# FASTAPI
# =============================================================================

app = FastAPI(
    title="Vibify AI Product Video"
)


# =============================================================================
# FRONTEND ROUTES
# =============================================================================

@app.get("/")
def home():

    index_file = (
        FRONTEND_DIR /
        "index.html"
    )

    if not index_file.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                f"index.html not found: "
                f"{index_file}"
            ),
        )

    return FileResponse(
        index_file
    )


@app.get("/app.js")
def frontend_javascript():

    file_path = (
        FRONTEND_DIR /
        "app.js"
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                f"app.js not found: "
                f"{file_path}"
            ),
        )

    return FileResponse(
        file_path,
        media_type="application/javascript",
    )


@app.get("/styles.css")
def frontend_styles():

    file_path = (
        FRONTEND_DIR /
        "styles.css"
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                f"styles.css not found: "
                f"{file_path}"
            ),
        )

    return FileResponse(
        file_path,
        media_type="text/css",
    )


# =============================================================================
# HEALTH
# =============================================================================

@app.get("/health")
def health():

    comfy_ok = False

    try:

        response = requests.get(
            f"{COMFYUI_URL}/system_stats",
            timeout=5,
        )

        comfy_ok = (
            response.ok
        )

    except Exception:

        comfy_ok = False

    return {

        "success":
            True,

        "server":
            "A",

        "comfyui":
            COMFYUI_URL,

        "comfyui_connected":
            comfy_ok,

        "ffmpeg_path":
            str(FFMPEG_PATH),

        "ffmpeg_exists":
            FFMPEG_PATH.exists(),

        "video_workflow":
            str(
                VIDEO_WORKFLOW_FILE
            ),

        "video_workflow_exists":
            VIDEO_WORKFLOW_FILE.exists(),

        "audio_workflow":
            str(
                AUDIO_WORKFLOW_FILE
            ),

        "audio_workflow_exists":
            AUDIO_WORKFLOW_FILE.exists(),
    }


# =============================================================================
# DEBUG PATHS
# =============================================================================

@app.get("/debug/paths")
def debug_paths():

    return {

        "base_dir":
            str(BASE_DIR),

        "frontend_dir":
            str(FRONTEND_DIR),

        "frontend_exists":
            FRONTEND_DIR.exists(),

        "upload_dir":
            str(UPLOAD_DIR),

        "upload_exists":
            UPLOAD_DIR.exists(),

        "output_dir":
            str(OUTPUT_DIR),

        "output_exists":
            OUTPUT_DIR.exists(),

        "workflow_dir":
            str(WORKFLOW_DIR),

        "workflow_exists":
            WORKFLOW_DIR.exists(),

        "video_workflow_file":
            str(
                VIDEO_WORKFLOW_FILE
            ),

        "video_workflow_exists":
            VIDEO_WORKFLOW_FILE.exists(),

        "audio_workflow_file":
            str(
                AUDIO_WORKFLOW_FILE
            ),

        "audio_workflow_exists":
            AUDIO_WORKFLOW_FILE.exists(),

        "comfyui_url":
            COMFYUI_URL,

        "ffmpeg_path":
            str(FFMPEG_PATH),

        "ffmpeg_exists":
            FFMPEG_PATH.exists(),

        "shot_duration":
            SHOT_DURATION,
    }


# =============================================================================
# DEBUG OUTPUTS
# =============================================================================

@app.get("/debug/outputs")
def debug_outputs():

    files = []

    for file in (
        OUTPUT_DIR.iterdir()
    ):

        if file.is_file():

            files.append({

                "name":
                    file.name,

                "size":
                    file.stat().st_size,

                "path":
                    str(file),

                "url":
                    f"/generated/{file.name}",
            })

    return {

        "success":
            True,

        "output_dir":
            str(OUTPUT_DIR),

        "files":
            files,
    }


# =============================================================================
# INTERRUPT
# =============================================================================

@app.post("/interrupt")
def interrupt_generation():

    terminal_title(
        "INTERRUPT GENERATION",
        RED,
    )

    try:

        response = requests.post(
            f"{COMFYUI_URL}/interrupt",
            timeout=10,
        )

        return {

            "success":
                response.ok,

            "status_code":
                response.status_code,
        }

    except requests.RequestException as e:

        return {

            "success":
                False,

            "error":
                str(e),
        }


# =============================================================================
# CHECK COMFYUI
# =============================================================================

def check_comfyui():

    try:

        response = requests.get(
            f"{COMFYUI_URL}/system_stats",
            timeout=10,
        )

        response.raise_for_status()

        return True

    except requests.RequestException as e:

        raise HTTPException(
            status_code=503,
            detail=(
                "Cannot connect to ComfyUI "
                f"({COMFYUI_URL}). "
                f"Error: {str(e)}"
            ),
        )


# =============================================================================
# CHECK FFMPEG
# =============================================================================

def check_ffmpeg():

    terminal_title(
        "CHECK FFMPEG",
        CYAN,
    )

    terminal_value(
        "FFmpeg path",
        FFMPEG_PATH,
    )

    if not FFMPEG_PATH.exists():

        raise HTTPException(
            status_code=500,
            detail=(
                "FFmpeg executable not found.\n"
                f"Expected path: {FFMPEG_PATH}"
            ),
        )

    try:

        result = subprocess.run(
            [
                str(FFMPEG_PATH),
                "-version",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not execute FFmpeg.\n"
                f"{str(e)}"
            ),
        )

    if result.returncode != 0:

        raise HTTPException(
            status_code=500,
            detail=(
                "FFmpeg returned an error.\n"
                f"{result.stderr[-3000:]}"
            ),
        )

    print(
        GREEN +
        "FFmpeg connection: OK" +
        RESET
    )

    print()

    return True


# =============================================================================
# LOAD WORKFLOW
# =============================================================================

def load_workflow(
    workflow_path: Path,
) -> dict:

    terminal_title(
        "LOAD WORKFLOW",
        CYAN,
    )

    terminal_value(
        "Workflow",
        workflow_path,
    )

    if not workflow_path.exists():

        raise HTTPException(
            status_code=500,
            detail=(
                "Workflow file not found: "
                f"{workflow_path}"
            ),
        )

    try:

        with open(
            workflow_path,
            "r",
            encoding="utf-8",
        ) as file:

            workflow = json.load(
                file
            )

    except json.JSONDecodeError as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Invalid workflow JSON: "
                f"{str(e)}"
            ),
        )

    return workflow


# =============================================================================
# SAVE UPLOAD
# =============================================================================

def save_upload_file(
    upload_file: UploadFile,
    prefix: str,
) -> Path:

    original_filename = (
        upload_file.filename
        or f"{prefix}.bin"
    )

    extension = (
        Path(
            original_filename
        )
        .suffix
        .lower()
    )

    if not extension:

        extension = ".bin"

    destination = (
        UPLOAD_DIR /
        f"{prefix}_"
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    try:

        upload_file.file.seek(0)

        data = (
            upload_file.file.read()
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not read uploaded file: "
                f"{str(e)}"
            ),
        )

    if not data:

        raise HTTPException(
            status_code=400,
            detail=(
                "Uploaded file is empty."
            ),
        )

    try:

        destination.write_bytes(
            data
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not save uploaded file: "
                f"{str(e)}"
            ),
        )

    return destination


# =============================================================================
# UPLOAD IMAGE TO COMFYUI
# =============================================================================

def upload_image_to_comfyui(
    image_path: Path,
    upload_name: str,
) -> str:

    terminal_title(
        "UPLOAD IMAGE TO COMFYUI",
        BLUE,
    )

    check_comfyui()

    try:

        with open(
            image_path,
            "rb",
        ) as image_file:

            response = requests.post(

                f"{COMFYUI_URL}/upload/image",

                files={
                    "image": (
                        upload_name,
                        image_file,
                        "application/octet-stream",
                    )
                },

                data={
                    "overwrite":
                        "true"
                },

                timeout=120,
            )

        response.raise_for_status()

        result = (
            response.json()
        )

    except requests.RequestException as e:

        raise HTTPException(
            status_code=502,
            detail=(
                "Failed to upload image to ComfyUI: "
                f"{str(e)}"
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=502,
            detail=(
                "ComfyUI returned invalid JSON "
                "while uploading image."
            ),
        )

    image_name = (
        result.get(
            "name"
        )
    )

    if not image_name:

        raise HTTPException(
            status_code=502,
            detail=(
                "ComfyUI image upload succeeded "
                "but no image name was returned."
            ),
        )

    terminal_value(
        "ComfyUI image",
        image_name,
        GREEN,
    )

    return image_name


# =============================================================================
# VIDEO RESOLUTION
# =============================================================================

def get_resolution_settings(
    frame_size: str,
) -> tuple[str, float]:

    frame_size = (
        frame_size.strip()
    )

    if frame_size == "1:1":

        return (
            "1:1 (Square)",
            1,
        )

    if frame_size == "16:9":

        return (
            "16:9 (Widescreen)",
            1,
        )

    if frame_size == "9:16":

        return (
            "9:16 (Portrait Widescreen)",
            1,
        )

    return (
        "1:1 (Square)",
        1,
    )


# =============================================================================
# SHOT TIMING
# =============================================================================

def get_shot_times(
    shot_index: int,
) -> tuple[float, float]:

    start_time = (
        shot_index *
        SHOT_DURATION
    )

    end_time = (
        start_time +
        SHOT_DURATION
    )

    return (
        start_time,
        end_time,
    )


# =============================================================================
# H3 FRAME COUNT
# =============================================================================

def get_h3_frame_count(
    seconds: float,
) -> int:

    base_frames = max(
        5,
        round(
            seconds * 24
        ),
    )

    frame_count = (
        base_frames +
        (
            5 -
            (
                base_frames %
                17
            )
        ) %
        17
    )

    return frame_count


# =============================================================================
# BUILD LLM INPUT
# =============================================================================

def build_llm_input(
    product_name: str,
    frame_size: str,
    duration: int,
    shot: dict,
    shot_index: int,
    shot_count: int,
) -> str:

    start_time, end_time = (
        get_shot_times(
            shot_index
        )
    )

    return f"""
Product Name:
{product_name}

Frame Size:
{frame_size}

Final Video Duration:
{duration} seconds

Individual Shot Duration:
{SHOT_DURATION} seconds

Shot:
{shot_index + 1} of {shot_count}

Shot Time:
{start_time:.2f} - {end_time:.2f} seconds

Camera Motion:
{shot.get("cameraMotion", "")}

Lighting:
{shot.get("lighting", "")}

Product Motion:
{shot.get("productMotion", "")}

Effects:
{shot.get("effect", "")}

Background Motion:
{shot.get("backgroundMotion", "")}

Background / Environment:
{shot.get("background", "")}

Text On Video:
{shot.get("textOnVideo", "")}

Additional Creative Direction:
{shot.get("additionalPrompt", "")}
""".strip()


# =============================================================================
# BUILD MINIMAX PROMPT
# =============================================================================

def build_minimax_prompt(
    product_name: str,
    shot: dict,
    generated_prompt: str,
) -> str:

    background = (
        str(
            shot.get(
                "background",
                "",
            )
        ).strip()
        or
        "a premium studio environment"
    )

    background_motion = (
        str(
            shot.get(
                "backgroundMotion",
                "",
            )
        ).strip()
        or
        "subtle natural environmental movement"
    )

    camera_motion = (
        str(
            shot.get(
                "cameraMotion",
                "",
            )
        ).strip()
        or
        "slow controlled cinematic camera movement"
    )

    lighting = (
        str(
            shot.get(
                "lighting",
                "",
            )
        ).strip()
        or
        "premium studio soft lighting"
    )

    product_motion = (
        str(
            shot.get(
                "productMotion",
                "",
            )
        ).strip()
        or
        "static product presentation"
    )

    effects = (
        str(
            shot.get(
                "effect",
                "",
            )
        ).strip()
        or
        "none"
    )

    text_on_video = (
        str(
            shot.get(
                "textOnVideo",
                "",
            )
        ).strip()
    )

    additional_prompt = (
        str(
            shot.get(
                "additionalPrompt",
                "",
            )
        ).strip()
        or
        generated_prompt
    )

    text_instruction = ""

    if text_on_video:

        text_instruction = f"""
TEXT ON VIDEO:

Display the following text clearly and professionally:

"{text_on_video}"

The text should be readable, correctly spelled,
visually clean and naturally integrated into
the advertisement.
"""

    return f"""
Create a premium cinematic product advertisement using the uploaded
product image as the exact visual reference.

PRODUCT:

The product being advertised is:

{product_name}

PRODUCT REFERENCE:

Use the uploaded product image as the authoritative visual reference
for the product.

Maintain the exact visual identity of the product throughout the
entire shot.

Preserve its original:

- shape
- geometry
- proportions
- colors
- materials
- textures
- surface details
- construction
- branding
- logos
- stitching
- visible product characteristics

Do not redesign the product.

Do not change its shape.

Do not add or remove product components.

Keep the product sharp, stable, recognizable, and visually consistent
across all frames.

SCENE:

Place the product in:

{background}

Create a sophisticated realistic commercial environment with:

- realistic surfaces
- spatial depth
- atmospheric detail
- cinematic composition
- realistic reflections
- physically plausible lighting

BACKGROUND MOTION:

{background_motion}

Create smooth, subtle and physically realistic environmental movement
that complements the product without distracting from it.

CAMERA:

{camera_motion}

Use smooth controlled cinematic camera movement.

Keep the product as the primary subject.

Maintain stable framing and clear visual focus.

LIGHTING:

{lighting}

Create premium cinematic lighting with realistic:

- highlights
- shadows
- reflections
- rim lighting

The lighting should reveal the product's materials, textures,
construction and fine details.

PRODUCT MOTION:

{product_motion}

Apply subtle, elegant and physically plausible product movement while
maintaining the product's original identity, geometry, proportions,
materials and surface details.

EFFECTS:

{effects}

Create subtle realistic cinematic effects that enhance the atmosphere.

{text_instruction}

ADDITIONAL CREATIVE DIRECTION:

{additional_prompt}

Maintain a clean premium advertising composition.

The product must remain visually dominant.

DEPTH OF FIELD:

Use realistic cinematic depth of field.

Keep the product highly detailed and sharply focused while creating
natural depth and controlled separation from the background.

MOTION:

Smooth, elegant, controlled commercial motion with strong temporal
consistency and natural physical movement.

Avoid:

- product deformation
- identity changes
- geometry changes
- texture changes
- logo changes
- flickering
- unstable camera motion
- unnatural object movement
- excessive effects

AUDIO:

Silent visual generation.

Audio will be added separately after video generation.
""".strip()


# =============================================================================
# PREPARE VIDEO WORKFLOW
# =============================================================================

def prepare_video_workflow(
    base_workflow: dict,
    product_name: str,
    frame_size: str,
    image_name: str,
    shot: dict,
    generated_prompt: str,
    shot_index: int,
) -> dict:

    workflow = json.loads(
        json.dumps(
            base_workflow
        )
    )

    # NODE 6 - input image

    if "6" in workflow:

        workflow[
            "6"
        ][
            "inputs"
        ][
            "image"
        ] = image_name


    # NODE 7 - resolution

    if "7" in workflow:

        aspect_ratio, megapixels = (
            get_resolution_settings(
                frame_size
            )
        )

        workflow[
            "7"
        ][
            "inputs"
        ][
            "aspect_ratio"
        ] = aspect_ratio

        workflow[
            "7"
        ][
            "inputs"
        ][
            "megapixels"
        ] = megapixels


    # NODE 8 - duration

    if "8" in workflow:

        workflow[
            "8"
        ][
            "inputs"
        ][
            "value"
        ] = SHOT_DURATION


    # NODE 10 - prompt

    if "10" in workflow:

        final_prompt = (
            build_minimax_prompt(
                product_name,
                shot,
                generated_prompt,
            )
        )

        workflow[
            "10"
        ][
            "inputs"
        ][
            "prompt"
        ] = final_prompt


    # NODE 11 - random seed

    if "11" in workflow:

        workflow[
            "11"
        ][
            "inputs"
        ][
            "noise_seed"
        ] = (
            uuid.uuid4().int %
            900000000000000
        )


    # NODE 19 - output video filename

    if "19" in workflow:

        workflow[
            "19"
        ][
            "inputs"
        ][
            "filename_prefix"
        ] = (
            "video/"
            f"vibify_shot_"
            f"{shot_index + 1}_"
            f"{uuid.uuid4().hex}"
        )


    # NODE 24 - final frame index

    if "24" in workflow:

        frame_count = (
            get_h3_frame_count(
                SHOT_DURATION
            )
        )

        workflow[
            "24"
        ][
            "inputs"
        ][
            "batch_index"
        ] = (
            frame_count - 1
        )

        workflow[
            "24"
        ][
            "inputs"
        ][
            "length"
        ] = 1


    # NODE 26 - save final frame

    if "26" in workflow:

        workflow[
            "26"
        ][
            "inputs"
        ][
            "filename_prefix"
        ] = (
            "last_frame/"
            f"vibify_shot_"
            f"{shot_index + 1}_last_"
            f"{uuid.uuid4().hex}"
        )

    return workflow


# =============================================================================
# QUEUE WORKFLOW
# =============================================================================

def queue_workflow(
    workflow: dict,
) -> str:

    check_comfyui()

    client_id = str(
        uuid.uuid4()
    )

    payload = {

        "prompt":
            workflow,

        "client_id":
            client_id,
    }

    terminal_title(
        "QUEUE WORKFLOW TO COMFYUI",
        BLUE,
    )

    try:

        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json=payload,
            timeout=30,
        )

    except requests.RequestException as e:

        raise HTTPException(
            status_code=502,
            detail={
                "message":
                    "Failed to connect to ComfyUI.",

                "error":
                    str(e),
            },
        )

    if not response.ok:

        try:

            response_data = (
                response.json()
            )

        except ValueError:

            response_data = (
                response.text
            )

        raise HTTPException(
            status_code=502,
            detail={
                "message":
                    "ComfyUI rejected workflow.",

                "status_code":
                    response.status_code,

                "response":
                    response_data,
            },
        )

    try:

        result = (
            response.json()
        )

    except ValueError:

        raise HTTPException(
            status_code=502,
            detail=(
                "ComfyUI returned invalid JSON."
            ),
        )

    if result.get("error"):

        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "ComfyUI workflow error.",

                "error":
                    result.get(
                        "error"
                    ),

                "node_errors":
                    result.get(
                        "node_errors",
                        {},
                    ),
            },
        )

    prompt_id = (
        result.get(
            "prompt_id"
        )
    )

    if not prompt_id:

        raise HTTPException(
            status_code=502,
            detail=(
                "ComfyUI did not return prompt_id."
            ),
        )

    terminal_value(
        "Prompt ID",
        prompt_id,
        GREEN,
    )

    return prompt_id


# =============================================================================
# WAIT FOR COMPLETION
# =============================================================================

def wait_for_completion(
    prompt_id: str,
) -> dict:

    start_time = (
        time.time()
    )

    terminal_title(
        "WAITING FOR COMFYUI",
        YELLOW,
    )

    while True:

        elapsed = (
            time.time() -
            start_time
        )

        if (
            elapsed >
            COMFYUI_TIMEOUT
        ):

            raise HTTPException(
                status_code=504,
                detail=(
                    "ComfyUI generation timed out."
                ),
            )

        try:

            response = requests.get(
                f"{COMFYUI_URL}/history/{prompt_id}",
                timeout=20,
            )

            response.raise_for_status()

            history = (
                response.json()
            )

        except requests.RequestException:

            time.sleep(
                COMFYUI_POLL_INTERVAL
            )

            continue

        if (
            prompt_id
            not in history
        ):

            print(
                f"{YELLOW}"
                f"Waiting... "
                f"{int(elapsed)}s"
                f"{RESET}",
                end="\r",
                flush=True,
            )

            time.sleep(
                COMFYUI_POLL_INTERVAL
            )

            continue

        result = (
            history[
                prompt_id
            ]
        )

        status = (
            result.get(
                "status",
                {},
            )
        )

        status_string = (
            status.get(
                "status_str"
            )
        )

        if status_string == "error":

            raise HTTPException(
                status_code=500,
                detail={
                    "message":
                        "ComfyUI workflow failed.",

                    "prompt_id":
                        prompt_id,

                    "messages":
                        status.get(
                            "messages",
                            [],
                        ),
                },
            )

        if (
            status.get(
                "completed"
            )
            is True
        ):

            print()

            print(
                GREEN +
                "ComfyUI generation completed." +
                RESET
            )

            print()

            return result

        time.sleep(
            COMFYUI_POLL_INTERVAL
        )


# =============================================================================
# FIND VIDEO
# =============================================================================

def find_video_in_history(
    history: dict,
) -> dict | None:

    outputs = (
        history.get(
            "outputs",
            {},
        )
    )

    node_order = []

    if "19" in outputs:

        node_order.append(
            (
                "19",
                outputs["19"],
            )
        )

    for node_id, output in (
        outputs.items()
    ):

        if node_id != "19":

            node_order.append(
                (
                    node_id,
                    output,
                )
            )

    for _, node_output in (
        node_order
    ):

        if not isinstance(
            node_output,
            dict,
        ):

            continue

        for key in (
            "gifs",
            "videos",
            "files",
            "images",
        ):

            items = (
                node_output.get(
                    key,
                    [],
                )
            )

            if not isinstance(
                items,
                list,
            ):

                continue

            for item in items:

                if not isinstance(
                    item,
                    dict,
                ):

                    continue

                filename = (
                    item.get(
                        "filename",
                        "",
                    )
                )

                if filename.lower().endswith(
                    (
                        ".mp4",
                        ".webm",
                        ".mov",
                        ".mkv",
                        ".gif",
                    )
                ):

                    return item

    return None


# =============================================================================
# FIND LAST FRAME
# =============================================================================

def find_last_frame_in_history(
    history: dict,
) -> dict | None:

    outputs = (
        history.get(
            "outputs",
            {},
        )
    )

    node_output = (
        outputs.get(
            "26",
            {},
        )
    )

    if not isinstance(
        node_output,
        dict,
    ):

        return None

    images = (
        node_output.get(
            "images",
            [],
        )
    )

    if not isinstance(
        images,
        list,
    ):

        return None

    for item in images:

        if not isinstance(
            item,
            dict,
        ):

            continue

        filename = (
            item.get(
                "filename",
                "",
            )
        )

        if filename.lower().endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
            )
        ):

            return item

    return None


# =============================================================================
# FIND AUDIO
# =============================================================================

def find_audio_in_history(
    history: dict,
) -> dict | None:

    outputs = (
        history.get(
            "outputs",
            {},
        )
    )

    ordered_nodes = []

    if "107" in outputs:

        ordered_nodes.append(
            (
                "107",
                outputs["107"],
            )
        )

    for node_id, node_output in (
        outputs.items()
    ):

        if node_id != "107":

            ordered_nodes.append(
                (
                    node_id,
                    node_output,
                )
            )

    audio_extensions = (
        ".mp3",
        ".wav",
        ".flac",
        ".ogg",
        ".m4a",
        ".aac",
    )

    for _, node_output in (
        ordered_nodes
    ):

        if not isinstance(
            node_output,
            dict,
        ):

            continue

        for key in (
            "audio",
            "audios",
            "files",
        ):

            items = (
                node_output.get(
                    key,
                    [],
                )
            )

            if isinstance(
                items,
                dict,
            ):

                items = [items]

            if not isinstance(
                items,
                list,
            ):

                continue

            for item in items:

                if not isinstance(
                    item,
                    dict,
                ):

                    continue

                filename = (
                    item.get(
                        "filename",
                        "",
                    )
                )

                if filename.lower().endswith(
                    audio_extensions
                ):

                    return item

        # fallback for custom node format

        for value in (
            node_output.values()
        ):

            if not isinstance(
                value,
                list,
            ):

                continue

            for item in value:

                if not isinstance(
                    item,
                    dict,
                ):

                    continue

                filename = (
                    item.get(
                        "filename",
                        "",
                    )
                )

                if filename.lower().endswith(
                    audio_extensions
                ):

                    return item

    return None


# =============================================================================
# DOWNLOAD COMFYUI FILE
# =============================================================================

def download_comfy_file(
    file_info: dict,
    destination: Path,
):

    filename = (
        file_info.get(
            "filename"
        )
    )

    subfolder = (
        file_info.get(
            "subfolder",
            "",
        )
    )

    file_type = (
        file_info.get(
            "type",
            "output",
        )
    )

    if not filename:

        raise HTTPException(
            status_code=500,
            detail=(
                "ComfyUI output does not contain filename."
            ),
        )

    params = {

        "filename":
            filename,

        "subfolder":
            subfolder,

        "type":
            file_type,
    }

    try:

        response = requests.get(
            f"{COMFYUI_URL}/view",
            params=params,
            stream=True,
            timeout=180,
        )

        response.raise_for_status()

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            destination,
            "wb",
        ) as output_file:

            for chunk in (
                response.iter_content(
                    chunk_size=1024 * 1024
                )
            ):

                if chunk:

                    output_file.write(
                        chunk
                    )

    except requests.RequestException as e:

        raise HTTPException(
            status_code=502,
            detail=(
                "Failed to download file "
                "from ComfyUI: "
                f"{str(e)}"
            ),
        )

    if (
        not destination.exists()
        or
        destination.stat().st_size == 0
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "Downloaded ComfyUI file is empty."
            ),
        )


# =============================================================================
# MERGE VIDEO SHOTS
# =============================================================================

def merge_videos(
    video_paths: list[Path],
    destination: Path,
):

    if not video_paths:

        raise HTTPException(
            status_code=500,
            detail=(
                "No video shots available."
            ),
        )

    check_ffmpeg()


    # -------------------------------------------------------------------------
    # ONE VIDEO
    # -------------------------------------------------------------------------

    if len(video_paths) == 1:

        command = [

            str(FFMPEG_PATH),

            "-y",

            "-i",
            str(
                video_paths[0]
            ),

            "-map",
            "0:v:0",

            "-c:v",
            "copy",

            "-an",

            "-movflags",
            "+faststart",

            str(destination),
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:

            fallback = [

                str(FFMPEG_PATH),

                "-y",

                "-i",
                str(
                    video_paths[0]
                ),

                "-map",
                "0:v:0",

                "-c:v",
                "libx264",

                "-preset",
                "medium",

                "-crf",
                "18",

                "-pix_fmt",
                "yuv420p",

                "-an",

                "-movflags",
                "+faststart",

                str(destination),
            ]

            result = (
                subprocess.run(
                    fallback,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            )

        if result.returncode != 0:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to finalize generated video.\n"
                    f"{result.stderr[-4000:]}"
                ),
            )

        return


    # -------------------------------------------------------------------------
    # MULTIPLE VIDEOS
    # -------------------------------------------------------------------------

    concat_file = (
        OUTPUT_DIR /
        f".concat_"
        f"{uuid.uuid4().hex}.txt"
    )

    try:

        with open(
            concat_file,
            "w",
            encoding="utf-8",
        ) as file:

            for video_path in (
                video_paths
            ):

                safe_path = (
                    str(
                        video_path.resolve()
                    )
                    .replace(
                        "\\",
                        "/",
                    )
                    .replace(
                        "'",
                        r"\'",
                    )
                )

                file.write(
                    f"file '{safe_path}'\n"
                )


        # first try copy

        command = [

            str(FFMPEG_PATH),

            "-y",

            "-f",
            "concat",

            "-safe",
            "0",

            "-i",
            str(concat_file),

            "-map",
            "0:v:0",

            "-c:v",
            "copy",

            "-an",

            "-movflags",
            "+faststart",

            str(destination),
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if (
            result.returncode == 0
            and
            destination.exists()
            and
            destination.stat().st_size > 0
        ):

            return

        if destination.exists():

            try:

                destination.unlink()

            except Exception:

                pass


        # fallback re-encode

        fallback = [

            str(FFMPEG_PATH),

            "-y",

            "-f",
            "concat",

            "-safe",
            "0",

            "-i",
            str(concat_file),

            "-c:v",
            "libx264",

            "-preset",
            "medium",

            "-crf",
            "18",

            "-pix_fmt",
            "yuv420p",

            "-an",

            "-movflags",
            "+faststart",

            str(destination),
        ]

        fallback_result = (
            subprocess.run(
                fallback,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        )

        if (
            fallback_result.returncode
            != 0
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Failed to merge video shots.\n"
                    f"{fallback_result.stderr[-4000:]}"
                ),
            )

    finally:

        if concat_file.exists():

            try:

                concat_file.unlink()

            except Exception:

                pass


# =============================================================================
# AUDIO PRESETS
# =============================================================================

AUDIO_PRESETS = {

    "Cinematic 🎬": {

        "style": (
            "cinematic commercial music with polished modern production, "
            "premium atmosphere, subtle dramatic energy and elegant "
            "advertising feel"
        ),

        "bpm":
            95,

        "key":
            "E minor",
    },


    "Upbeat 🎵": {

        "style": (
            "upbeat modern commercial music with a catchy melody, "
            "bright rhythm, positive energy and clean advertising production"
        ),

        "bpm":
            118,

        "key":
            "C major",
    },


    "Energetic ⚡": {

        "style": (
            "energetic modern advertising music with punchy rhythm, "
            "fast momentum, exciting production and strong promotional energy"
        ),

        "bpm":
            128,

        "key":
            "D minor",
    },


    "Premium ✨": {

        "style": (
            "premium luxury commercial music with sophisticated modern textures, "
            "elegant rhythm and high-end brand advertising feel"
        ),

        "bpm":
            92,

        "key":
            "A minor",
    },


    "Modern 🔷": {

        "style": (
            "modern commercial background music with contemporary electronic "
            "textures, clean rhythm, stylish production and catchy "
            "advertising energy"
        ),

        "bpm":
            110,

        "key":
            "F minor",
    },


    "Corporate 💼": {

        "style": (
            "professional corporate commercial music with clean modern "
            "instrumentation, confident rhythm and polished business "
            "advertising feel"
        ),

        "bpm":
            105,

        "key":
            "C major",
    },


    "Ambient 🌿": {

        "style": (
            "soft ambient commercial background music with calm modern textures, "
            "gentle rhythm, clean production and relaxed brand-friendly atmosphere"
        ),

        "bpm":
            75,

        "key":
            "D major",
    },


    "Playful 😊": {

        "style": (
            "playful cheerful commercial music with a fun catchy melody, "
            "bright rhythm and friendly modern advertising energy"
        ),

        "bpm":
            120,

        "key":
            "G major",
    },


    "Inspirational 🌟": {

        "style": (
            "uplifting inspirational commercial music with a memorable melody, "
            "positive progression and polished motivational advertising feel"
        ),

        "bpm":
            100,

        "key":
            "D major",
    },


    "Futuristic 🚀": {

        "style": (
            "futuristic modern commercial music with sleek electronic textures, "
            "digital rhythm, innovative energy and polished technology "
            "advertising feel"
        ),

        "bpm":
            115,

        "key":
            "F minor",
    },
}


# =============================================================================
# PREPARE ACE STEP AUDIO WORKFLOW
# =============================================================================

def prepare_audio_workflow(
    base_workflow: dict,
    audio_style: str,
    product_name: str,
    duration: int,
) -> dict:

    workflow = json.loads(
        json.dumps(
            base_workflow
        )
    )

    preset = (
        AUDIO_PRESETS.get(
            audio_style,
            AUDIO_PRESETS[
                "Modern 🔷"
            ],
        )
    )

    style_description = (
        preset[
            "style"
        ]
    )

    bpm = (
        preset[
            "bpm"
        ]
    )

    keyscale = (
        preset[
            "key"
        ]
    )


    # -------------------------------------------------------------------------
    # NEW AUDIO PROMPT
    # -------------------------------------------------------------------------

    audio_prompt = f"""
Create modern commercial background music for a marketing video.

Make it catchy, polished, engaging, and suitable for advertising a
product or service.

Use a clean contemporary sound with a memorable melody and rhythm
that matches the selected music style.

Keep the energy suitable for a short promotional video and make the
music feel professional, exciting, and brand-friendly.

Music Description:
[ {style_description} ]

duration:
[ {duration} ]

Product/service:
[ {product_name} ]

Avoid cinematic movie-score, orchestral, dramatic, dark, or overly
emotional soundtrack styles unless specifically requested by the
selected music style.

Keep the music instrumental with no vocals and no spoken words.

Structure the music specifically for a short {duration}-second
commercial advertisement.

Create an immediate musical hook at the beginning.

Avoid long introductions or slow build-ups.

Maintain a clear and engaging rhythm throughout the full duration.

End the music naturally with a smooth, gradual fade-out.

Do not abruptly cut or stop the music.

Make the ending feel complete and polished for a professional
advertisement.
""".strip()


    # -------------------------------------------------------------------------
    # NODE 94
    # TextEncodeAceStepAudio1.5
    # -------------------------------------------------------------------------

    if "94" not in workflow:

        raise HTTPException(
            status_code=500,
            detail=(
                "Audio workflow Node 94 "
                "was not found."
            ),
        )


    workflow[
        "94"
    ][
        "inputs"
    ][
        "tags"
    ] = audio_prompt


    workflow[
        "94"
    ][
        "inputs"
    ][
        "lyrics"
    ] = ""


    workflow[
        "94"
    ][
        "inputs"
    ][
        "duration"
    ] = duration


    workflow[
        "94"
    ][
        "inputs"
    ][
        "bpm"
    ] = bpm


    workflow[
        "94"
    ][
        "inputs"
    ][
        "keyscale"
    ] = keyscale


    # -------------------------------------------------------------------------
    # NODE 98
    # Exact audio seconds
    # -------------------------------------------------------------------------

    if "98" not in workflow:

        raise HTTPException(
            status_code=500,
            detail=(
                "Audio workflow Node 98 "
                "was not found."
            ),
        )


    workflow[
        "98"
    ][
        "inputs"
    ][
        "seconds"
    ] = duration


    # -------------------------------------------------------------------------
    # NODE 109
    # Random seed
    # -------------------------------------------------------------------------

    if "109" in workflow:

        workflow[
            "109"
        ][
            "inputs"
        ][
            "value"
        ] = (
            uuid.uuid4().int %
            2147483647
        )


    # -------------------------------------------------------------------------
    # NODE 107
    # MP3 output filename
    # -------------------------------------------------------------------------

    if "107" not in workflow:

        raise HTTPException(
            status_code=500,
            detail=(
                "Audio workflow Node 107 "
                "was not found."
            ),
        )


    workflow[
        "107"
    ][
        "inputs"
    ][
        "filename_prefix"
    ] = (
        "audio/"
        f"vibify_audio_"
        f"{uuid.uuid4().hex}"
    )


    terminal_title(
        "ACE STEP AUDIO SETTINGS",
        MAGENTA,
    )

    terminal_value(
        "Audio style",
        audio_style,
    )

    terminal_value(
        "Product",
        product_name,
    )

    terminal_value(
        "BPM",
        bpm,
    )

    terminal_value(
        "Key",
        keyscale,
    )

    terminal_value(
        "Duration",
        f"{duration} seconds",
    )

    terminal_prompt(
        "ACE STEP MUSIC PROMPT",
        audio_prompt,
        GREEN,
    )

    return workflow


# =============================================================================
# GENERATE ACE STEP AUDIO
# =============================================================================

def generate_ace_audio(
    audio_style: str,
    product_name: str,
    duration: int,
) -> Path:

    terminal_title(
        "GENERATE ACE STEP AUDIO",
        MAGENTA,
    )

    base_workflow = (
        load_workflow(
            AUDIO_WORKFLOW_FILE
        )
    )

    workflow = (
        prepare_audio_workflow(
            base_workflow,
            audio_style,
            product_name,
            duration,
        )
    )

    prompt_id = (
        queue_workflow(
            workflow
        )
    )

    history = (
        wait_for_completion(
            prompt_id
        )
    )

    audio_info = (
        find_audio_in_history(
            history
        )
    )

    if not audio_info:

        terminal_title(
            "AUDIO OUTPUT DEBUG",
            RED,
        )

        print(
            json.dumps(
                history.get(
                    "outputs",
                    {},
                ),
                indent=2,
            )
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "ACE Step completed but no "
                "generated audio file was found."
            ),
        )

    comfy_filename = (
        audio_info.get(
            "filename",
            "audio.mp3",
        )
    )

    extension = (
        Path(
            comfy_filename
        )
        .suffix
        .lower()
    )

    if not extension:

        extension = ".mp3"

    destination = (
        OUTPUT_DIR /
        f"generated_audio_"
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    download_comfy_file(
        audio_info,
        destination,
    )

    terminal_value(
        "Generated audio",
        destination,
        GREEN,
    )

    return destination


# =============================================================================
# ADD AUDIO TO VIDEO
# =============================================================================

def mux_video_audio(
    video_path: Path,
    audio_path: Path,
    destination: Path,
):

    check_ffmpeg()

    terminal_title(
        "FFMPEG ADD AUDIO",
        MAGENTA,
    )

    command = [

        str(FFMPEG_PATH),

        "-y",

        "-i",
        str(video_path),

        "-stream_loop",
        "-1",

        "-i",
        str(audio_path),

        "-map",
        "0:v:0",

        "-map",
        "1:a:0",

        "-c:v",
        "copy",

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        "-shortest",

        "-movflags",
        "+faststart",

        str(destination),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if (
        result.returncode == 0
        and
        destination.exists()
        and
        destination.stat().st_size > 0
    ):

        return


    # -------------------------------------------------------------------------
    # FALLBACK
    # -------------------------------------------------------------------------

    if destination.exists():

        try:

            destination.unlink()

        except Exception:

            pass


    fallback = [

        str(FFMPEG_PATH),

        "-y",

        "-i",
        str(video_path),

        "-stream_loop",
        "-1",

        "-i",
        str(audio_path),

        "-map",
        "0:v:0",

        "-map",
        "1:a:0",

        "-c:v",
        "libx264",

        "-preset",
        "medium",

        "-crf",
        "18",

        "-pix_fmt",
        "yuv420p",

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        "-shortest",

        "-movflags",
        "+faststart",

        str(destination),
    ]

    fallback_result = (
        subprocess.run(
            fallback,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    )

    if (
        fallback_result.returncode
        != 0
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to add audio to video.\n"
                f"{fallback_result.stderr[-5000:]}"
            ),
        )

    if (
        not destination.exists()
        or
        destination.stat().st_size == 0
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "FFmpeg reported success but "
                "final video with audio is missing."
            ),
        )


# =============================================================================
# GENERATE
# =============================================================================

@app.post("/generate")
def generate(

    product_name: str = Form(...),

    frame_size: str = Form(...),

    duration: int = Form(...),

    shots: str = Form(...),

    product_image: UploadFile = File(...),

    audio: str = Form(""),

    audio_file: UploadFile | None = File(None),

):

    terminal_title(
        "NEW VIBIFY GENERATION",
        MAGENTA,
    )


    # =========================================================================
    # VALIDATION
    # =========================================================================

    if duration not in (
        5,
        10,
        15,
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Duration must be 5, 10 or 15 seconds."
            ),
        )


    if frame_size not in (
        "1:1",
        "16:9",
        "9:16",
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid frame size."
            ),
        )


    product_name = (
        product_name.strip()
    )

    if not product_name:

        raise HTTPException(
            status_code=400,
            detail=(
                "Product name is required."
            ),
        )


    try:

        shot_data = (
            json.loads(
                shots
            )
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid shots JSON."
            ),
        )


    if not isinstance(
        shot_data,
        list,
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "shots must be a JSON array."
            ),
        )


    expected_shot_count = (
        duration //
        SHOT_DURATION
    )


    if (
        len(shot_data) !=
        expected_shot_count
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid shot count for "
                f"{duration} seconds. "
                f"Expected "
                f"{expected_shot_count}, "
                f"received "
                f"{len(shot_data)}."
            ),
        )


    # =========================================================================
    # REQUEST INFO
    # =========================================================================

    terminal_value(
        "Product",
        product_name,
    )

    terminal_value(
        "Frame size",
        frame_size,
    )

    terminal_value(
        "Duration",
        duration,
    )

    terminal_value(
        "Shot count",
        len(
            shot_data
        ),
    )

    terminal_value(
        "Audio preset",
        audio or "None",
    )

    terminal_value(
        "Custom audio uploaded",
        bool(
            audio_file
            and
            audio_file.filename
        ),
    )


    # =========================================================================
    # SAVE PRODUCT IMAGE
    # =========================================================================

    image_path = (
        save_upload_file(
            product_image,
            "product",
        )
    )

    original_filename = (
        product_image.filename
        or "product.png"
    )


    # =========================================================================
    # UPLOAD PRODUCT IMAGE TO COMFYUI
    # =========================================================================

    current_image_name = (
        upload_image_to_comfyui(
            image_path,
            original_filename,
        )
    )


    # =========================================================================
    # LOAD VIDEO WORKFLOW
    # =========================================================================

    base_video_workflow = (
        load_workflow(
            VIDEO_WORKFLOW_FILE
        )
    )


    # =========================================================================
    # GENERATE VIDEO SHOTS
    # =========================================================================

    local_shot_videos = []

    generated_shots = []

    shot_chain = []

    temporary_last_frames = []

    shot_count = (
        len(
            shot_data
        )
    )


    for shot_index, shot in (
        enumerate(
            shot_data
        )
    ):

        if not isinstance(
            shot,
            dict,
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Shot "
                    f"{shot_index + 1} "
                    f"is invalid."
                ),
            )


        terminal_title(
            f"VIDEO SHOT "
            f"{shot_index + 1} / "
            f"{shot_count}",
            MAGENTA,
        )


        shot_input_image = (
            current_image_name
        )


        # ---------------------------------------------------------------------
        # LLM INPUT
        # ---------------------------------------------------------------------

        llm_input = (
            build_llm_input(

                product_name=
                    product_name,

                frame_size=
                    frame_size,

                duration=
                    duration,

                shot=
                    shot,

                shot_index=
                    shot_index,

                shot_count=
                    shot_count,
            )
        )


        terminal_prompt(
            "LLM INPUT",
            llm_input,
            BLUE,
        )


        # ---------------------------------------------------------------------
        # LLM PROMPT
        # ---------------------------------------------------------------------

        try:

            generated_prompt = (
                generate_prompt(
                    llm_input
                )
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "LLM prompt generation failed: "
                    f"{str(e)}"
                ),
            )


        terminal_prompt(
            "LLM GENERATED PROMPT",
            generated_prompt,
            GREEN,
        )


        final_prompt = (
            build_minimax_prompt(
                product_name,
                shot,
                generated_prompt,
            )
        )


        terminal_prompt(
            "FINAL MINIMAX PROMPT",
            final_prompt,
            MAGENTA,
        )


        # ---------------------------------------------------------------------
        # VIDEO WORKFLOW
        # ---------------------------------------------------------------------

        workflow = (
            prepare_video_workflow(

                base_workflow=
                    base_video_workflow,

                product_name=
                    product_name,

                frame_size=
                    frame_size,

                image_name=
                    shot_input_image,

                shot=
                    shot,

                generated_prompt=
                    generated_prompt,

                shot_index=
                    shot_index,
            )
        )


        # ---------------------------------------------------------------------
        # QUEUE
        # ---------------------------------------------------------------------

        prompt_id = (
            queue_workflow(
                workflow
            )
        )


        # ---------------------------------------------------------------------
        # WAIT
        # ---------------------------------------------------------------------

        history = (
            wait_for_completion(
                prompt_id
            )
        )


        # ---------------------------------------------------------------------
        # VIDEO OUTPUT
        # ---------------------------------------------------------------------

        video_info = (
            find_video_in_history(
                history
            )
        )


        if not video_info:

            raise HTTPException(
                status_code=500,
                detail={
                    "message":
                        "ComfyUI finished but no "
                        "video was found.",

                    "prompt_id":
                        prompt_id,
                },
            )


        comfy_video_filename = (
            video_info.get(
                "filename",
                f"shot_"
                f"{shot_index + 1}.mp4",
            )
        )


        video_extension = (
            Path(
                comfy_video_filename
            )
            .suffix
            .lower()
        )


        if not video_extension:

            video_extension = ".mp4"


        local_video_path = (
            OUTPUT_DIR /
            f"shot_"
            f"{shot_index + 1}_"
            f"{uuid.uuid4().hex}"
            f"{video_extension}"
        )


        download_comfy_file(
            video_info,
            local_video_path,
        )


        local_shot_videos.append(
            local_video_path
        )


        start_time, end_time = (
            get_shot_times(
                shot_index
            )
        )


        # ---------------------------------------------------------------------
        # LAST FRAME FOR NEXT SHOT
        # ---------------------------------------------------------------------

        last_frame_url = None
        next_input_image = None


        if (
            shot_index <
            shot_count - 1
        ):

            last_frame_info = (
                find_last_frame_in_history(
                    history
                )
            )


            if not last_frame_info:

                raise HTTPException(
                    status_code=500,
                    detail={
                        "message": (
                            "ComfyUI finished shot "
                            f"{shot_index + 1}, "
                            "but Node 26 did not "
                            "return the last frame."
                        ),

                        "prompt_id":
                            prompt_id,
                    },
                )


            comfy_last_filename = (
                last_frame_info.get(
                    "filename",
                    "last_frame.png",
                )
            )


            last_extension = (
                Path(
                    comfy_last_filename
                )
                .suffix
                .lower()
            )


            if not last_extension:

                last_extension = ".png"


            last_frame_path = (
                OUTPUT_DIR /
                f"last_frame_"
                f"{shot_index + 1}_"
                f"{uuid.uuid4().hex}"
                f"{last_extension}"
            )


            download_comfy_file(
                last_frame_info,
                last_frame_path,
            )


            temporary_last_frames.append(
                last_frame_path
            )


            current_image_name = (
                upload_image_to_comfyui(

                    last_frame_path,

                    (
                        f"vibify_shot_"
                        f"{shot_index + 1}_"
                        f"last_input"
                        f"{last_extension}"
                    ),
                )
            )


            next_input_image = (
                current_image_name
            )


            last_frame_url = (
                f"/generated/"
                f"{last_frame_path.name}"
            )


        # ---------------------------------------------------------------------
        # SHOT RETURN DATA
        # ---------------------------------------------------------------------

        generated_shots.append({

            "shot":
                shot_index + 1,

            "start_time":
                start_time,

            "end_time":
                end_time,

            "duration":
                SHOT_DURATION,

            "video":
                (
                    f"/generated/"
                    f"{local_video_path.name}"
                ),

            "filename":
                local_video_path.name,

            "input_image":
                shot_input_image,

            "last_frame":
                last_frame_url,

            "next_input_image":
                next_input_image,

            "generated_prompt":
                generated_prompt,

            "final_minimax_prompt":
                final_prompt,

            "comfy_prompt_id":
                prompt_id,
        })


        shot_chain.append({

            "shot":
                shot_index + 1,

            "input_image":
                shot_input_image,

            "output_video":
                str(
                    local_video_path
                ),

            "next_input_image":
                next_input_image,

            "last_frame":
                last_frame_url,
        })


    # =========================================================================
    # MERGE SHOTS
    # =========================================================================

    terminal_title(
        "MERGE VIDEO SHOTS",
        MAGENTA,
    )


    silent_video_path = (
        OUTPUT_DIR /
        f"vibify_silent_"
        f"{uuid.uuid4().hex}.mp4"
    )


    merge_videos(
        local_shot_videos,
        silent_video_path,
    )


    if (
        not silent_video_path.exists()
        or
        silent_video_path.stat().st_size == 0
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "Silent video was not created."
            ),
        )


    # =========================================================================
    # AUDIO SELECTION
    # =========================================================================

    selected_audio_path = None

    audio_source = None

    audio_applied = False

    audio_warning = None

    generated_audio_path = None

    uploaded_audio_path = None


    # -------------------------------------------------------------------------
    # CUSTOM AUDIO HAS PRIORITY
    # -------------------------------------------------------------------------

    if (
        audio_file is not None
        and
        audio_file.filename
    ):

        terminal_title(
            "USE UPLOADED AUDIO",
            GREEN,
        )

        uploaded_audio_path = (
            save_upload_file(
                audio_file,
                "user_audio",
            )
        )

        selected_audio_path = (
            uploaded_audio_path
        )

        audio_source = (
            "uploaded"
        )


    # -------------------------------------------------------------------------
    # OTHERWISE ACE STEP
    # -------------------------------------------------------------------------

    elif audio:

        terminal_title(
            "GENERATE AI AUDIO",
            MAGENTA,
        )

        try:

            generated_audio_path = (
                generate_ace_audio(

                    audio_style=
                        audio,

                    product_name=
                        product_name,

                    duration=
                        duration,
                )
            )

            selected_audio_path = (
                generated_audio_path
            )

            audio_source = (
                "ace_step"
            )

        except HTTPException as e:

            print(
                RED +
                "ACE Step audio generation failed." +
                RESET
            )

            print(
                e.detail
            )

            print()

            audio_warning = (
                "Video generated successfully, "
                "but AI music generation failed. "
                f"{e.detail}"
            )


    # =========================================================================
    # FINAL VIDEO
    # =========================================================================

    final_video_path = (
        OUTPUT_DIR /
        f"vibify_"
        f"{uuid.uuid4().hex}.mp4"
    )


    if selected_audio_path:

        mux_video_audio(
            silent_video_path,
            selected_audio_path,
            final_video_path,
        )

        audio_applied = True

    else:

        try:

            shutil.move(
                str(
                    silent_video_path
                ),
                str(
                    final_video_path
                ),
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Could not create final video: "
                    f"{str(e)}"
                ),
            )


    # =========================================================================
    # FINAL CHECK
    # =========================================================================

    if (
        not final_video_path.exists()
        or
        final_video_path.stat().st_size == 0
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "Final video was not created."
            ),
        )


    # =========================================================================
    # CLEANUP
    # =========================================================================

    for shot_video in (
        local_shot_videos
    ):

        try:

            if shot_video.exists():

                shot_video.unlink()

        except Exception:

            pass


    for frame in (
        temporary_last_frames
    ):

        try:

            if frame.exists():

                frame.unlink()

        except Exception:

            pass


    if (
        silent_video_path.exists()
        and
        silent_video_path !=
        final_video_path
    ):

        try:

            silent_video_path.unlink()

        except Exception:

            pass


    if generated_audio_path:

        try:

            if (
                generated_audio_path.exists()
            ):

                generated_audio_path.unlink()

        except Exception:

            pass


    if uploaded_audio_path:

        try:

            if (
                uploaded_audio_path.exists()
            ):

                uploaded_audio_path.unlink()

        except Exception:

            pass


    try:

        if image_path.exists():

            image_path.unlink()

    except Exception:

        pass


    # =========================================================================
    # RETURN
    # =========================================================================

    video_url = (
        f"/generated/"
        f"{final_video_path.name}"
    )


    terminal_title(
        "GENERATION COMPLETE",
        GREEN,
    )


    terminal_value(
        "Final video",
        final_video_path,
    )


    terminal_value(
        "Browser URL",
        video_url,
    )


    terminal_value(
        "Final size",
        final_video_path.stat().st_size,
    )


    terminal_value(
        "Duration",
        f"{duration} seconds",
    )


    terminal_value(
        "Audio applied",
        audio_applied,
    )


    terminal_value(
        "Audio source",
        audio_source,
    )


    return {

        "success":
            True,

        "id":
            uuid.uuid4().hex,

        "product_name":
            product_name,

        "frame_size":
            frame_size,

        "duration":
            duration,

        "shot_duration":
            SHOT_DURATION,

        "shot_count":
            shot_count,

        "video_url":
            video_url,

        "filename":
            final_video_path.name,

        "audio":
            audio,

        "audio_applied":
            audio_applied,

        "audio_source":
            audio_source,

        "audio_warning":
            audio_warning,

        "shots":
            generated_shots,

        "shot_chain":
            shot_chain,
    }

# =============================================================================
# SAVE VIDEO TO LIBRARY
# =============================================================================

@app.post("/api/library/save")
def save_video_to_library(
    video_url: str = Form(...),
    filename: str = Form(...),
    product_name: str = Form(""),
    frame_size: str = Form(""),
    duration: int = Form(0),
    audio: str = Form(""),
    shots: str = Form("[]"),
):

    library = load_library()

    # Prevent the same video from being saved twice
    for video in library["videos"]:

        if video.get("filename") == filename:

            return {
                "success": True,
                "already_saved": True,
                "video": video,
            }

    # Remember the prompts/shots used to create the video
    try:
        shot_data = json.loads(shots)

    except json.JSONDecodeError:
        shot_data = []

    library_video = {

        "id":
            uuid.uuid4().hex,

        "video_url":
            video_url,

        "filename":
            filename,

        "product_name":
            product_name,

        "frame_size":
            frame_size,

        "duration":
            duration,

        "audio":
            audio,

        "shots":
            shot_data,

        "saved_at":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
    }

    library["videos"].insert(
        0,
        library_video,
    )

    save_library(library)

    return {

        "success":
            True,

        "already_saved":
            False,

        "video":
            library_video,
    }

# =============================================================================
# GET SAVED LIBRARY VIDEOS
# =============================================================================

@app.get("/api/library")
def get_library():

    library = load_library()

    return {

        "success":
            True,

        "videos":
            library["videos"],
    }

# =============================================================================
# DELETE GENERATED VIDEO
# =============================================================================

@app.delete(
    "/api/generated/{filename}"
)
def delete_generated_video(
    filename: str,
):

    safe_filename = (
        Path(
            filename
        ).name
    )

    file_path = (
        OUTPUT_DIR /
        safe_filename
    )

    try:

        resolved = (
            file_path.resolve()
        )

        output_root = (
            OUTPUT_DIR.resolve()
        )

        if (
            output_root
            not in resolved.parents
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid filename."
                ),
            )

    except HTTPException:

        raise

    except Exception:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid filename."
            ),
        )


    if not resolved.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                "File not found."
            ),
        )


    try:

        resolved.unlink()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


    return {

        "success":
            True,
    }


# =============================================================================
# STATIC FILES
# =============================================================================

app.mount(
    "/generated",
    StaticFiles(
        directory=OUTPUT_DIR
    ),
    name="generated",
)


app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="static",
)
