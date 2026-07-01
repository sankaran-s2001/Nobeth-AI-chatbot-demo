import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(
    title="Minimal AI Chatbot API",
    description="### 🌟 Welcome Student!\n1. Expand the green **POST /ask** bar.\n2. Click the **Try it out** button.\n3. Type your question in the text box under **prompt**.\n4. Click the blue **Execute** button to see the AI response!"
)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def welcome():
    return RedirectResponse(url="/docs")

@app.post("/ask")
def ask_ai(prompt: str):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"response": completion.choices[0].message.content}
