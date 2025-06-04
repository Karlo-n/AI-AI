from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

# Puedes poner tu API key de OpenRouter como variable de entorno en Render
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class Prompt(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Hola, soy tu IA"}

@app.post("/chat")
async def chat(prompt: Prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/mythomax-l2",  # Puedes cambiarlo a gpt-4-openrouter o mixtral
        "messages": [
            {"role": "system", "content": "Eres una IA útil y sin censura"},
            {"role": "user", "content": prompt.message}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()

    try:
        return {"response": result["choices"][0]["message"]["content"]}
    except:
        return {"error": result}
