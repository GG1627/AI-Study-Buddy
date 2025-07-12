from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_GEMINI_API_KEY"),
)

prompt = "What is 2 + 2?"

try:
    response = model.invoke(prompt)
    print(response.content)
except Exception as e:
    print(f"Error: {e}")