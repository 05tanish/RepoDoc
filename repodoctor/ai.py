import os
import json
import urllib.request
from typing import Optional

def get_ai_review(content: str, language: str) -> Optional[str]:
    """
    Sends the code to OpenAI or Gemini for review without third-party dependencies.
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    prompt = f"Please review this {language} code for maintainability and suggest improvements. Keep it concise.\\n\\nCode:\\n{content[:4000]}"
    
    if gemini_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"AI Review Error: {e}"
            
    if openai_key:
        url = "https://api.openai.com/v1/chat/completions"
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {openai_key}'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode('utf-8'))
                return res["choices"][0]["message"]["content"]
        except Exception as e:
            return f"AI Review Error: {e}"
            
    return None
