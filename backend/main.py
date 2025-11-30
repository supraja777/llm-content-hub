from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from latestUpdates.pipeline import generateContentList

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/static"), name = "static")
templates = Jinja2Templates(directory = "../frontend/templates")

@app.get("/flashcards")
def flashcards(request: Request):
   query = "Latest updates on Large Language Models"
   cards = generateContentList(query)
   return templates.TemplateResponse("flashcards.html", {"request": request, "cards": cards})
    
if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port = 8000, reload = True)