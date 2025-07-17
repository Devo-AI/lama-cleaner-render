import requests

url = "http://127.0.0.1:8000/repurpose"
video_path = "11 seconds.mov"  # Make sure this file is in the same folder
platform = "tiktok"

with open(video_path, "rb") as f:
    files = {
        "file": ("11 seconds.mov", f, "video/quicktime")
    }
    data = {
        "platform": platform  # Changed key from target_platform to platform
    }
    response = requests.post(url, data=data, files=files)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
