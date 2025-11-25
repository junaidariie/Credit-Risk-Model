FROM python:3.11

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "$PORT"]


