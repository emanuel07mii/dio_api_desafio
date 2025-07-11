from dotenv import load_dotenv
import os
load_dotenv()

url = os.getenv("DATABASE_URL")
if not url:
    print("DATABASE_URL not set in .env file. Using default value.\n")

print(url)