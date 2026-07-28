from dotenv import load_dotenv
import os
from google import genai

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Say hello in one sentence."
)

print(response.text)