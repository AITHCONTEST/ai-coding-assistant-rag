.SILENT:

local venv:
	python -m venv venv
	. ./venv/bin/activate
	pip install -r requirements.txt


compose-run:
	docker-compose -p stackoverflow-rag -f docker/docker-compose.yaml --env-file .env up --build -d