.SILENT:

local venv:
	python3 -m venv venv
	. ./venv/bin/activate
	pip install -r requirements.txt
	. ./utils/fix_libs.sh

compose-run:
	docker-compose -p stackoverflow-rag -f docker/docker-compose.yaml --env-file .env up --build -d