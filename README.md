# 🤖 Minimal AI Chatbot API

Welcome to the **Minimal AI Chatbot API**! This project is a simple, end-to-end backend web application designed specifically for students with **zero coding knowledge**.

The goal of this project is to show you how a web server (backend) accepts input data in JSON format, communicates with an Artificial Intelligence (AI) service, and returns the result as a JSON response.

---

## 📂 Project Structure & File Purposes

Here are the files in this project and what they do:

```text
Nobeth-AI-chatbot-demo/
│
├── .env                  # 🔒 Secret file: Stores your private Groq API key.
├── .gitignore            # 🙈 Git controller: Tells Git to ignore .env and virtual environments.
├── requirements.txt      # 📦 Package list: Lists the Python libraries our project needs.
├── app.py                # 🐍 Application core: The main backend code and API logic.
└── README.md             # 📖 This guide: Explains how the project works and how to run it.
```

---

## ⚡ End-to-End Workflow

Here is how the API works under the hood when you send a request:

```mermaid
flowchart TD
    subgraph Browser ["🌐 Interactive Documentation (http://127.0.0.1:8080/docs)"]
        A["👤 Student types prompt under POST /ask"] --> B["📤 Clicks 'Execute' to send JSON request"]
        F["📥 Receives and displays JSON response"]
    end

    subgraph Server ["🐍 Backend Server (FastAPI)"]
        B --> C["📥 FastAPI receives the prompt"]
        C --> D["🤖 FastAPI calls Groq Cloud SDK"]
        E["📤 Packages text reply as JSON"] --> F
    end

    subgraph AI_Cloud ["☁️ AI Service (Groq Cloud)"]
        D -->|API Key + Prompt| Llama["🧠 llama-3.3-70b-versatile Model"]
        Llama -->|Generates text answer| E
    end

    style Browser fill:#1e1e2f,stroke:#6366f1,stroke-width:2px,color:#fff
    style Server fill:#161825,stroke:#a855f7,stroke-width:2px,color:#fff
    style AI_Cloud fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#fff
```

### Step-by-Step Breakdown:
1. **Student Action**: You open the interactive docs page (`/docs`) in your browser, type a prompt (e.g., `"Explain photosynthesis"`), and click **Execute**.
2. **The Request**: Your browser sends a `POST` request containing a JSON body `{ "prompt": "Explain photosynthesis" }` to our backend server.
3. **The Server**: FastAPI receives the prompt, checks that it is not empty, and sends it over to Groq's super-fast AI servers using the **Groq Python SDK**.
4. **The AI**: Groq's AI model (`llama-3.3-70b-versatile`) processes the prompt and generates a text response.
5. **The Response**: FastAPI gets the text response back, packs it into a JSON object `{"response": "..."}`, and sends it back to your browser.

---

## 🚀 Setup Guide from Scratch (For New Users)

Follow these steps to set up and run this project on any new computer:

### Step 1: Download (Pull) the Repository
Open your terminal (PowerShell or Command Prompt) and run:
```bash
git clone https://github.com/sankaran-s2001/Nobeth-AI-chatbot-demo.git
cd Nobeth-AI-chatbot-demo
```

### Step 2: Create a New Virtual Environment
A virtual environment keeps our project libraries separated from other projects on your computer.
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
Activate it based on your operating system:
* **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
* **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### Step 4: Install the Required Packages
Install all libraries listed in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 5: Configure the API Key
1. Create a new file named `.env` in the root of the project directory.
2. Open the `.env` file in your text editor and add the following line, replacing the placeholder with your actual Groq API key:
   ```text
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Step 6: Start the Server
```bash
uvicorn app:app --reload --port 8080
```

### Step 7: Open the Interactive UI
Open your browser and navigate to:
👉 **[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)**

---

## 📜 Code Reference Guide (Functions & Parameters)

Here is a breakdown of the code functions inside `app.py`:

| Route / Endpoint | Function Name | Input Parameters | What it returns (Output) | What it does (Simple Explanation) |
| :--- | :--- | :--- | :--- | :--- |
| **`GET /`** | `welcome_message` | *None* | A JSON object:<br>`{"message": "...", "instructions": "..."}` | **The Welcome Route**: When you visit `http://127.0.0.1:8080/`, it outputs simple instructions on how to test the API. |
| **`POST /ask`** | `ask_ai` | `request_data: AskRequest` <br>*(A JSON object containing the user's prompt)* | A JSON object:<br>`{"response": "AI text answer"}` | **The Chat Handler**: Receives your question, forwards it to Groq's AI, gets the response, and sends it back to the browser. |

---

### 🤖 The Groq AI SDK Call
Inside the `ask_ai` function, we ask Groq to generate a response using this code:
```python
completion = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
    ]
)
```

#### What do these parameters mean?
* **`model="llama-3.3-70b-versatile"`**: The specific AI model we want to run.
* **`messages`**: Instructions for the AI:
  * **`system`**: Sets the AI's behavior/personality.
  * **`user`**: The actual question the student typed.
* **`completion.choices[0].message.content`**: Extracts the generated text response out of the larger API response object.

---

## 📖 Glossary of Terms (With Real-World Analogies)

> [!TIP]
> Use these analogies to understand the concepts if you are completely new to programming!

* **⚙️ Backend**: **The Restaurant Kitchen**. It is hidden behind doors. The chef prepares meals, manages ingredients (data), and handles the heavy lifting.
* **🌉 API (Application Programming Interface)**: **The Waiter**. The waiter takes your order from the table, carries it to the kitchen (backend), and returns with your food (response).
* **📥 Endpoint (`/ask`)**: **A Specific Item on the Menu**. It is a specific web address that accepts inputs to perform a specific action (like getting an AI response).
* **📦 JSON**: **The Serving Tray**. A standardized format used to carry structured data back and forth over the internet.
* **🛠️ SDK (Software Development Kit)**: **A Pre-packaged Recipe Box**. It provides pre-made ingredients and tools so developers don't have to write complex connection code from scratch.
* **🧠 LLM (Large Language Model)**: **The Smart Chef**. A computer model trained on millions of pages of text to understand human prompts and write human-like replies.
* **🔒 Environment Variables (`.env`)**: **The Restaurant Safe**. A secure place to lock away secret API keys so they aren't left lying around in the open.
