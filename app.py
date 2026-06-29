import os
# The "os" module is part of Python's standard library. We use it to read environment variables (like our API key).
from dotenv import load_dotenv
# "dotenv" allows us to read key-value pairs from a file named ".env" and set them as environment variables.
# This is a secure way to store API keys without uploading them to GitHub.
from fastapi import FastAPI, Request, HTTPException
# "FastAPI" is the main framework class.
# "Request" is used to represent incoming HTTP requests.
# "HTTPException" allows us to return HTTP errors (like 400 or 500) with custom messages.
from fastapi.templating import Jinja2Templates
# "Jinja2Templates" helps FastAPI search for and render HTML files in our project.
from pydantic import BaseModel
# "BaseModel" is used to define and validate the structure of JSON data sent to our API.
from groq import Groq
# "Groq" is the official SDK provided by Groq to interact with their high-speed AI models.

# ==========================================
# 1. LOAD CONFIGURATION & ENVIRONMENT FILES
# ==========================================
# Look for a file named ".env" in the same directory and load its key-value pairs.
load_dotenv()

# Retrieve the Groq API key from the environment.
groq_api_key = os.getenv("GROQ_API_KEY")

# Check if the API key exists. If not, print a warning to help the student debug.
if not groq_api_key:
    print("\n[WARNING] GROQ_API_KEY is not set in your .env file!")
    print("Please make sure you have a .env file with: GROQ_API_KEY=your_key_here\n")

# ==========================================
# 2. INITIALIZE SERVICES (FastAPI & Groq)
# ==========================================
# Create our FastAPI application instance. This instance handles our routes and starts the server.
app = FastAPI(
    title="Nobeth Demo AI Chatbot",
    description="A beginner-friendly AI Chatbot built using FastAPI and Groq Cloud.",
    version="1.0.0"
)

# Set up the folder where our HTML templates reside.
# Here we specify the folder "templates" which we will create next.
templates = Jinja2Templates(directory="templates")

# Initialize the Groq client with the API key we loaded from .env.
# If the API key is empty, we set groq_client to None so we can handle it later without crashing immediately.
try:
    groq_client = Groq(api_key=groq_api_key)
except Exception as e:
    print(f"[ERROR] Failed to initialize Groq client: {e}")
    groq_client = None

# ==========================================
# 3. DEFINE DATA MODELS (Pydantic)
# ==========================================
# When the frontend sends a POST request to '/ask', it sends data in JSON format: {"prompt": "user prompt here"}
# We define a Pydantic model so FastAPI knows exactly what keys and data types to expect and validate.
class AskRequest(BaseModel):
    prompt: str  # We expect a key named "prompt" containing a string (text)

# ==========================================
# 4. DEFINE WEB SERVER ROUTES
# ==========================================

# --- GET ROUTE (Renders the Chat Room UI) ---
# When a user visits the root URL (http://127.0.0.1:8000/), this function runs.
# It uses Jinja2 to render the "index.html" file inside the "templates" folder.
@app.get("/")
def get_home_page(request: Request):
    # "templates.TemplateResponse" renders our HTML file and passes the "request" context, 
    # which is required by FastAPI to manage the client connection.
    # Note: Modern FastAPI/Starlette uses the keyword argument signature: TemplateResponse(request=request, name="index.html")
    return templates.TemplateResponse(request=request, name="index.html")


# --- POST ROUTE (Sends user prompt to Groq AI) ---
# When the browser submits the user's message, it sends a POST request to "/ask" with a JSON body.
# FastAPI automatically validates this body against our "AskRequest" model above.
@app.post("/ask")
def ask_ai(request_data: AskRequest):
    # 1. Check if the Groq API key is set
    if not groq_api_key or not groq_client:
        raise HTTPException(
            status_code=500,
            detail="Groq API Key is missing or invalid. Please check your .env file."
        )

    # 2. Extract and clean the prompt sent by the user
    user_prompt = request_data.prompt.strip()

    # 3. Check if the user prompt is empty or just spaces
    if not user_prompt:
        raise HTTPException(
            status_code=400,
            detail="The prompt cannot be empty. Please enter a valid message."
        )

    try:
        # 4. Request a text completion from Groq
        # We call the completion API synchronously (which means we wait for the response to finish before continuing).
        # We are using the requested "llama-3.3-70b-versatile" model.
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                # System role: Sets the behavior, tone, or instructions for the AI.
                {
                    "role": "system",
                    "content": "You are a helpful, friendly, and concise AI chat assistant. Format your replies clearly."
                },
                # User role: Represents the actual question or input from the student/user.
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        # 5. Extract the text message generated by the AI
        ai_response = completion.choices[0].message.content

        # 6. Return the response as a JSON dictionary: {"response": "AI's text answer"}
        # FastAPI automatically converts Python dictionaries into JSON formatting.
        return {"response": ai_response}

    except Exception as e:
        # If anything goes wrong (e.g. network failure, invalid key, rate limits),
        # return a server error (HTTP 500) explaining what happened.
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating a response: {str(e)}"
        )
