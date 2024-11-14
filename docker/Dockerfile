FROM python:3.12

WORKDIR /app

COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY ../.env .env
COPY ../src src/

ENTRYPOINT ["python", "-m", "src.main"]