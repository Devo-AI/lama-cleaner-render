import ffmpeg

def process_video(input_path: str, output_path: str) -> str:
    print(f"🎬 [video_processor] Processing video from {input_path} to {output_path}")
    (
        ffmpeg
        .input(input_path)
        .output(output_path, vf="scale=720:-1", acodec='aac', vcodec='libx264')
        .run(overwrite_output=True)
    )
    return output_path
