FROM python:3.13-slim-bookworm


ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Устанавливаем зависимости для Tesseract
RUN apt-get update && apt-get install -y \
tesseract-ocr \
tesseract-ocr-rus \
tesseract-ocr-eng \
libtesseract-dev \
&& rm -rf /var/lib/apt/lists/*

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/
# Копируем проект
WORKDIR /app

COPY . .

# Устанавливаем зависимости проекта
RUN uv pip freeze > requirements.txt
RUN pip install -r requirements.txt 


# Запуск через uvicorn
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]

