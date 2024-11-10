from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from collections import Counter
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

class URLRequest(BaseModel):
    url: str
    n: int = 10 

@app.post("/analyze")
async def analyze_url(data: URLRequest):
    try:
        response = requests.get(data.url)
        response.raise_for_status()
        
        response.encoding = response.apparent_encoding
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Error fetching the URL") from e

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    print(text)
    words = re.findall(r'[a-zA-Z]+', text.lower())  
    
    word_counts = Counter(words)
    top_words = word_counts.most_common(data.n)

    return {"top_words": top_words}
