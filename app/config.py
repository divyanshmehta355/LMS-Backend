import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.account import Account

# Load environment variables
load_dotenv()

# Initialize Appwrite Client
client = Client()
client.set_endpoint(os.getenv("APPWRITE_ENDPOINT"))
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
client.set_key(os.getenv("APPWRITE_API_KEY"))

# Initialize Appwrite Account service
account = Account(client)
