
run_test:
	docker exec -it cloud-test-task_flask_1 /bin/sh -c "pytest -vv -s"

build:
	docker-compose up --build -d

lint:
	docker exec -it cloud-test-task_flask_1 /bin/sh -c "flake8 "