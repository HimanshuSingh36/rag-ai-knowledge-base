FROM python:3.12-slim

WORKDIR /app

COPY Backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Backend/ .

EXPOSE 5002

CMD ["python", "app.py"]