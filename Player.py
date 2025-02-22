from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

class MusicPlayer:
    def __init__(self, app):
        self.app = app
        self.call = PyTgCalls(self.app)
        self.call.start()
        self.queue = {}

    async def play(self, song_name, chat_id):
        ydl_opts = {"format": "bestaudio", "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            url = info["entries"][0]["url"]

        self.queue[chat_id] = url
        await self.call.join_group_call(chat_id, AudioPiped(url))
        await self.app.send_message(chat_id, f"🎶 **Now Playing:** {song_name}")

    async def skip(self, chat_id):
        if chat_id in self.queue:
            del self.queue[chat_id]
        await self.call.leave_group_call(chat_id)
        await self.app.send_message(chat_id, "⏭ **Skipped!**")

    async def stop(self, chat_id):
        if chat_id in self.queue:
            del self.queue[chat_id]
        await self.call.leave_group_call(chat_id)
        await self.app.send_message(chat_id, "⏹ **Stopped!**")
