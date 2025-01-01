.SILENT:

local venv:
	python3 -m venv venv
	. ./venv/bin/activate
	pip install -r requirements.txt
	. ./utils/fix_libs.sh

compose-run:
	docker-compose -p stackoverflow-rag -f docker/docker-compose.yaml --env-file .env up --build -d

tests:
	python3 tests/utils/create_test_dataset.py
	python3 -m tests.helpfulness_test
	python3 -m tests.reference_test