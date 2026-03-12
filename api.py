from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import uuid
import time
from pydantic import BaseModel
from logger_config import logger, trace_id_var

app = FastAPI(title="Tom and Jerry API", version="1.0")


class CommandRequest(BaseModel):
    command: str
    target: str



@app.middleware("http")
async def log_requests_and_trace(request: Request, call_next):

    trace_id = str(uuid.uuid4())[:8]
    trace_id_var.set(trace_id)


    start_time = time.time()


    response = await call_next(request)


    process_time = (time.time() - start_time) * 1000


    logger.info(
        f"HTTP {request.method} {request.url.path} | Status: {response.status_code} | Time: {process_time:.2f}ms",
        extra={'context': 'HTTP_Traffic'}
    )

    response.headers["X-Trace-ID"] = trace_id
    return response



@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        logger.warning(f"Спроба доступу до неіснуючої сторінки: {request.url.path}", extra={'context': '404_Error'})
        return JSONResponse(
            status_code=404,
            content={
                "error": "Сторінку не знайдено",
                "message": "Халепа! Такого маршруту не існує. Перевірте адресу URL."
            }
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    current_trace_id = trace_id_var.get()
    logger.error(f"Необроблена помилка API: {str(exc)}", exc_info=True, extra={'context': 'API_Error'})
    return JSONResponse(
        status_code=500,
        content={
            "error_id": current_trace_id,
            "message": "Ой! Виникла непередбачена помилка системи.",
            "instruction": f"Будь ласка, збережіть код помилки ({current_trace_id}) та передайте його розробнику."
        }
    )


@app.post("/execute", summary="Виконати команду")
async def execute_command(req: CommandRequest):
    logger.info(f"Отримано команду: '{req.command}' для {req.target}", extra={'context': 'UserRequest'})

    if req.command.lower() == "зламайся":
        raise ValueError("Критичний збій бази даних! (Тест для Sentry)")

    return {"status": "success", "message": f"{req.target.capitalize()} отримав команду: {req.command}"}