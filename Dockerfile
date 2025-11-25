FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Railway assigns PORT dynamically; expose a default for local use
EXPOSE 8000

# Use sh so $PORT is expanded to an integer
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
