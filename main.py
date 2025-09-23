from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Regex pattern for YouTube video URL
youtube_url_pattern = r'^https?://(www\.)?youtube\.com/watch\?v=([\w-]{11})(&.*)?$'

def get_youtube_video_id(url: str):
    match = re.match(youtube_url_pattern, url)
    if match:
        video_id = match.group(2)  # captured video ID
        return video_id
    return None

def is_youtube_video_url(url: str):
    return bool(re.match(youtube_url_pattern, url))


app = FastAPI()

@app.get("/send_youtube_video_url/")
async def video_url(url: str):
    if not is_youtube_video_url(url):
        raise HTTPException(status_code = 400, detail = "Not a YouTube video URL")

    curr_video_id = get_youtube_video_id(url)
    if not curr_video_id:
        raise HTTPException(status_code = 400, detail = "Could not extract video ID")

    try:
        # Fetch transcript (English by default, can add fallback)
        transcript = YouTubeTranscriptApi().fetch(video_id = curr_video_id, languages = ['en'])
        return {"video_id": curr_video_id, "transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Failed to fetch transcript: {str(e)}")

