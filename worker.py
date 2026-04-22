import asyncio
import requests
from cache import get_cache_path

queue = asyncio.Queue()

async def worker():
    while True:
        job = await queue.get()

        video_url, file_path = job

        try:
            r = requests.get(video_url, stream=True, timeout=10)

            with open(file_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

        except Exception as e:
            print("Download error:", e)

        queue.task_done()
