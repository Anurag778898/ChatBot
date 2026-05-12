# brain.py
import google.generativeai as genai
import json
import config

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

SYSTEM_PROMPT = """
You are JARVIS, a PC assistant. The user gives you a command.
Your job is to convert it into a structured JSON action.

Return ONLY valid JSON — no explanation, no markdown, just JSON.

Action types you can return:
1. Open an app:
   {"action": "open_app", "app": "vs code"}

2. Open a website:
   {"action": "open_website", "url": "https://youtube.com"}

3. Search YouTube:
   {"action": "youtube_search", "query": "lo-fi music"}

4. Search Google:
   {"action": "google_search", "query": "best python tutorials"}

5. Open a folder:
   {"action": "open_folder", "folder": "downloads"}

6. Open a PDF or file:
   {"action": "open_file", "path": "C:/Users/Name/Documents/file.pdf"}

7. Type and open YouTube with specific query in specific browser:
   {"action": "youtube_search", "query": "best podcasts 2024", "browser": "brave"}

8. Play music on YouTube in a specific browser:
   {"action": "youtube_search", "query": "lo-fi chill beats", "browser": "brave"}

9. Just chat/answer (if it's not a PC command):
   {"action": "chat", "reply": "your answer here"}

Examples:
User: "open vs code" → {"action": "open_app", "app": "vs code"}
User: "play lo-fi songs in brave" → {"action": "youtube_search", "query": "lo-fi chill songs", "browser": "brave"}
User: "open best podcast on youtube" → {"action": "youtube_search", "query": "best podcasts 2024"}
User: "open my downloads folder" → {"action": "open_folder", "folder": "downloads"}
User: "what's the capital of France?" → {"action": "chat", "reply": "The capital of France is Paris."}
"""

def understand_command(user_input):
    """Send command to Gemini, get back structured action"""
    try:
        response = model.generate_content(SYSTEM_PROMPT + f"\n\nUser: {user_input}")
        raw = response.text.strip()
        
        # Clean up in case Gemini adds markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        return json.loads(raw.strip())
    except Exception as e:
        return {"action": "chat", "reply": f"Sorry, I had trouble understanding that. Error: {e}"}  