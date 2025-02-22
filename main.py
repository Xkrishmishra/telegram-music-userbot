from pyrogram import Client, filters
from player import MusicPlayer
from config import API_ID, API_HASH, SESSION_STRING, OWNER_NAME, OWNER_ID

app = Client("music_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
player = MusicPlayer(app)

@app.on_message(filters.command("play", prefixes="/") & filters.me)
async def play_song(client, message):
    song_name = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if song_name:
        await player.play(song_name, message.chat.id)
    else:
        await message.reply("Please provide a song name. Example: `/play Faded`")

@app.on_message(filters.command("skip", prefixes="/") & filters.me)
async def skip_song(client, message):
    await player.skip(message.chat.id)

@app.on_message(filters.command("end", prefixes="/") & filters.me)
async def stop_song(client, message):
    await player.stop(message.chat.id)

@app.on_message(filters.command("krish", prefixes="/"))
async def show_owner(client, message):
    await message.reply(f"👑 **Owner:** {OWNER_NAME}\n🆔 **User ID:** `{OWNER_ID}`")

print("Bot is running...")
app.run()
