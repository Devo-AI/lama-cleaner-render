from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from utils import (
    download_tiktok_video,
    process_uploaded_video,
    strip_metadata,
    generate_unique_filename,
)

app = FastAPI()

# Setup folders
os.makedirs("static/input", exist_ok=True)
os.makedirs("static/output", exist_ok=True)

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/repurpose")
async def repurpose_video(
    request: Request,
    target_platform: str = Form(...),
    tiktok_url: str = Form(""),
    file: UploadFile = File(None),
):
    input_path = None
    base_filename = generate_unique_filename()

    try:
        if tiktok_url.strip():
            input_path = await download_tiktok_video(tiktok_url, base_filename)
            if not input_path:
                return templates.TemplateResponse(
                    "index.html",
                    {"request": request, "error": "Failed to download from TikTok URL"},
                )

        elif file:
            input_path = await process_uploaded_video(file, base_filename)
        else:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Please upload a file or enter a TikTok URL"},
            )

        output_path = f"static/output/{base_filename}_final.mp4"
        strip_metadata(input_path, output_path)

        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=os.path.basename(output_path),
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Unexpected error: {str(e)}"},
        )
