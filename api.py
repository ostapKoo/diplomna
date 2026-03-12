from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uuid
from pydantic import BaseModel
from logger_config import logger
app = FastAPI(title="Tom and Jerry API", version="1.0")


class CommandRequest(BaseModel):
    command: str
    target: str


# 75% та 100%)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Генеруємо унікальний ID помилки
    error_id = str(uuid.uuid4())[:8]

    # Логуємо ТЕХНІЧНІ деталі для розробника у файл
    logger.error(f"ErrorID: {error_id} | Path: {request.url.path} | Текст помилки: {str(exc)}", exc_info=True,
                 extra={'context': 'API_Error'})

    # Повертаємо локалізовані відповідь користувачу
    return JSONResponse(
        status_code=500,
        content={
            "error_id": error_id,
            "message": "Ой! Виникла непередбачена помилка системи.",
            "instruction": "Будь ласка, збережіть код помилки та передайте його адміністратору.",
            "technical_details": "Технічні деталі приховані з міркувань безпеки."
        }
    )


@app.post("/execute", summary="Виконати команду")
async def execute_command(req: CommandRequest):
    logger.info(f"Отримано команду: {req.command} для {req.target}", extra={'context': 'UserRequest'})

    if req.command == "зламайся":
        raise ValueError("Штучний збій бази даних!")

    return {"status": "success", "message": f"{req.target.capitalize()} отримав команду: {req.command}"}