FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY create_database.py .
COPY inference.py .
COPY .env .
COPY /dataset/data.pkl ./dataset/data.pkl

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

CMD ["bash", "./entrypoint.sh"]