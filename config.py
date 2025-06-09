import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    ADMIN_ID = int(os.getenv('ADMIN_ID'))
    FILES_DIR = os.getenv('FILES_DIR', 'static/files')

config = Config()

