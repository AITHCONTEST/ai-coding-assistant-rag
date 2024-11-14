.SILENT:

local venv:
	python -m venv venv
	. ./venv/bin/activate
	pip install -r requirements.txt

run:
	python -m src.main

docker-run:
	docker build -f docker/Dockerfile . -t stackoverflow-rag
	docker run -d --name stackoverflow-rag stackoverflow-rag

compose-run:
	docker-compose -p stackoverflow-rag -f docker/docker-compose.yaml --env-file .env up --build -d