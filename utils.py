import asyncio

async def download_song(song_name):
    await asyncio.sleep(2)
    return f"{song_name}.mp3"
