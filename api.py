from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Tom and Jerry Assistant API",
    description="Інтерактивна OpenAPI документація для керування голосовим асистентом.",
    version="1.0.0"
)


class CommandRequest(BaseModel):
    command_text: str
    target: str  # "tom" або "jerry"


class CommandResponse(BaseModel):
    status: str
    response_message: str


@app.post("/execute", response_model=CommandResponse, summary="Виконати команду")
async def execute_command(request: CommandRequest):
    """
    Виконує системну команду (Том) або запит до ШІ (Джері).

    - **command_text**: Текст команди (наприклад, "відкрий браузер" або "напиши вірш").
    - **target**: Вказує, кому адресована команда ("tom" або "jerry").
    """

    if request.target.lower() == "tom":
        return {"status": "success", "response_message": f"Том виконав системну команду: {request.command_text}"}
    return {"status": "success", "response_message": f"Джері згенерував відповідь на: {request.command_text}"}
