import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
from config import API_ID, API_HASH, SESSION_STRING, OWNER_ID

userbot = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(userbot)

queues = {}

async def download_audio(url):
    options = {"format": "bestaudio/best", "outtmpl": "song.mp3"}
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return "song.mp3"

@userbot.on_message(filters.command("play", prefixes="/") & filters.me)
async def play(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Please provide a song name.")
        return

    query = " ".join(message.command[1:])
    ydl_opts = {"quiet": True, "format": "bestaudio/best"}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
    
    url = info["url"]
    song_path = await download_audio(url)

    chat_id = message.chat.id
    if chat_id in queues:
        queues[chat_id].append(song_path)
    else:
        queues[chat_id] = [song_path]
    
    if not call_py.active_calls:
        await call_py.join_group_call(chat_id, AudioPiped(song_path, StreamType().local_stream))
        await message.reply(f"🎵 Playing **{info['title']}** in voice chat.")

@userbot.on_message(filters.command("skip", prefixes="/") & filters.me)
async def skip(client, message):
    chat_id = message.chat.id
    if chat_id in queues and len(queues[chat_id]) > 1:
        queues[chat_id].pop(0)
        next_song = queues[chat_id][0]
        await call_py.change_stream(chat_id, AudioPiped(next_song, StreamType().local_stream))
        await message.reply("⏭ Skipping to the next song.")
    else:
        await message.reply("❌ No more songs in queue.")

@userbot.on_message(filters.command("end", prefixes="/") & filters.me)
async def end(client, message):
    chat_id = message.chat.id
    await call_py.leave_group_call(chat_id)
    queues.pop(chat_id, None)
    await message.reply("🔇 Stopped playing.")

@userbot.on_message(filters.command("krish", prefixes="/") & filters.me)
async def krish(client, message):
    await message.reply(f"👑 Owner: [Krish](tg://user?id={OWNER_ID})")

@userbot.on_message(filters.command("start", prefixes="/") & filters.me)
async def start(client, message):
    await message.reply("🎵 I'm a Userbot Music Player. Use /play <song> to play music.")

userbot.start()
call_py.run()
