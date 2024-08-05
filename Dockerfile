# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочий каталог
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Команда для запуска вашего приложения
CMD ["python3", "main.py"]