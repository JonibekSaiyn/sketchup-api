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

    # Нарисовать контур шкафа
    draw.rectangle([100, 100, 500, 700], outline="black", width=3)

    # Полки
    if params.shelves > 0:
        step = int((700 - 100) / (params.shelves + 1))
        for i in range(1, params.shelves + 1):
            y = 100 + step * i
            draw.line([100, y, 500, y], fill="gray", width=2)

    # Подпись
    draw.text((120, 60), f"{params.width}x{params.height}x{params.depth}, {params.shelves} полки", fill="black")

    # Сохраняем изображение
    file_id = str(uuid.uuid4())
    filename = f"/tmp/{file_id}.png"
    img.save(filename)

    # Пока что: используем заглушку
    return {
        "message": "Изображение создано локально",
        "note": "Для настоящей картинки нужно подключить хостинг изображений"
    }
