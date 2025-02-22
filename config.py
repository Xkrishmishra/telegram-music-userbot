import os

# Telegram API details
API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))  # Replace with your API ID
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")  # Replace with your API Hash

# Pyrogram Session (Stored in the session folder)
SESSION = os.getenv("SESSION", "session/your_session.session")  # Replace with correct session filename

# Owner Details
OWNER_NAME = "Krish Mishra"  # Change if needed
OWNER_ID = os.getenv("OWNER_ID", "YOUR_TELEGRAM_USER_ID")  # Replace with your Telegram ID
