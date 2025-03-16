FROM python:3.10

WORKDIR /app

# Устанавливаем системные библиотеки, необходимые для OpenCV НУЖНО ИСПРАВИТЬ REUIERMRNS
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt .

# Добавляем OpenCV вручную перед установкой зависимостей
RUN pip install --no-cache-dir opencv-python-headless

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
