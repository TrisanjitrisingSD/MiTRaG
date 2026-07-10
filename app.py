from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from pydantic import BaseModel

from ask_question_to_LLM import ask_llm


app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

templates=Jinja2Templates(directory="templates")


class Question(BaseModel):

    question:str


@app.get("/",response_class=HTMLResponse)

async def home(request:Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",

    )


@app.post("/ask")

async def ask(question:Question):

    return ask_llm(question.question)