from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from latestUpdates.pipeline import generateContentList
from mock_interview.pipeline import generate_questions_and_answers

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/static"), name = "static")
templates = Jinja2Templates(directory = "../frontend/templates")

#----------------- FLASHCARDS --------------------- 
@app.get("/flashcards")
def flashcards(request: Request):
   query = "Latest updates on Large Language Models"
   cards = generateContentList(query)
   return templates.TemplateResponse("flashcards.html", {"request": request, "cards": cards})

#----------------- MOCK INTERVIEW --------------------- 
generated_questions_and_answers = generate_questions_and_answers("RAG")
questions_and_answers = generated_questions_and_answers

@app.get("/interview")
def interview(request: Request):
   return templates.TemplateResponse(
      "interview.html",
      {
         "request": request,
         "questions_and_answers": questions_and_answers,
      }
   )

user_answers = []

@app.post("/interview")
async def submit_answers(
   request: Request,
):
   form_data = await request.form()  
   user_answers = [form_data[f"answer{{i}}"] for i in range(len(questions_and_answers))]
   feedback = "Thanks! Your answers have been submitted!"

   return templates.TemplateResponse(
      "interview.html",
      {
         "request": request,
         "user_answers": user_answers,
         "feedback": feedback
      }
   )
    
if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port = 8000, reload = True)