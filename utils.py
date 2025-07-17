import os
import uuid
import aiofiles
import subprocess
from TikTokApi import TikTokApi

async def process_uploaded_video(file, base_filename):
    input_path = f"static/input/{base_filename}.mp4"
    async with aiofiles.open(input_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    return input_path


async def download_tiktok_video(url: str, base_filename: str) -> str:
    try:
        api = TikTokApi()
        video = api.video(url=url)
        video_data = video.bytes()
        output_path = f"static/input/{base_filename}.mp4"
        with open(output_path, "wb") as f:
            f.write(video_data)
        return output_path
    except Exception as e:
        print("❌ TikTok download error:", e)
        return None


def strip_metadata(input_path: str, output_path: str):
    try:
        command = [
            "ffmpeg",
            "-i", input_path,
            "-map_metadata", "-1",
            "-c:v", "copy",
            "-c:a", "copy",
            output_path,
            "-y"
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("❌ Metadata stripping failed:", e)
        raise


def generate_unique_filename() -> str:
    return str(uuid.uuid4())[:8]
