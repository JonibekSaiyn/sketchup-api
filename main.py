from fastapi import FastAPI, Request
from pydantic import BaseModel
from PIL import Image, ImageDraw
import uuid
import os

app = FastAPI()

class CabinetParams(BaseModel):
    width: int
    height: int
    depth: int
    shelves: int

@app.post("/api/draw")
async def draw_cabinet(params: CabinetParams):
    img = Image.new("RGB", (600, 800), "white")
    draw = ImageDraw.Draw(img)

    # Нарисуем прямоугольник шкафа
    draw.rectangle([100, 100, 500, 700], outline="black", width=3)

    # Полки
    if params.shelves > 0:
        step = int((700 - 100) / (params.shelves + 1))
        for i in range(1, params.shelves + 1):
            y = 100 + step * i
            draw.line([100, y, 500, y], fill="black", width=2)

    # Сохраняем изображение
    file_id = str(uuid.uuid4())
    filename = f"/tmp/{file_id}.png"
    img.save(filename)

    # Заглушка: вместо настоящего хранилища возвращаем временный путь
    return {
        "image_url": f"https://raw.githubusercontent.com/devbyfury/sketchup-api/main/example.png",
        "note": "Тут будет настоящее изображение, когда подключим хранилище"
    }
