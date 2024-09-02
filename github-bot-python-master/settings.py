import os

from dotenv import load_dotenv

load_dotenv()

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')
