PROJECT_NAME=F1 Telemetry Simulation System
BACKEND_DIR=backend
FRONTEND_DIR=frontend
SIMULATOR_DIR=simulator

.PHONY: help up down logs backend-install backend-run backend-test frontend-install frontend-run simulator-build simulator-test simulator-live simulator-replay format clean

help:
	@echo "$(PROJECT_NAME)"
	@echo "make up              - start postgres, backend, and frontend with Docker Compose"
	@echo "make down            - stop Docker Compose services"
	@echo "make logs            - follow Docker Compose logs"
	@echo "make backend-install - install backend dependencies locally"
	@echo "make backend-run     - run FastAPI locally"
	@echo "make backend-test    - run backend pytest suite"
	@echo "make frontend-install- install frontend dependencies locally"
	@echo "make frontend-run    - run Vite locally"
	@echo "make simulator-build - build the C++ simulator"
	@echo "make simulator-test  - run simulator unit tests"
	@echo "make simulator-live  - run simulator in live mode"
	@echo "make simulator-replay- run simulator in replay mode"
	@echo "make clean           - remove common build artifacts"

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

backend-install:
	python -m pip install -r $(BACKEND_DIR)/requirements.txt

backend-run:
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend-test:
	cd $(BACKEND_DIR) && pytest

frontend-install:
	cd $(FRONTEND_DIR) && npm install

frontend-run:
	cd $(FRONTEND_DIR) && npm run dev -- --host 0.0.0.0 --port 5173

simulator-build:
	cmake -S $(SIMULATOR_DIR) -B $(SIMULATOR_DIR)/build && cmake --build $(SIMULATOR_DIR)/build

simulator-test:
	ctest --test-dir $(SIMULATOR_DIR)/build --output-on-failure

simulator-live:
	$(SIMULATOR_DIR)/build/f1_telemetry_simulator --config $(SIMULATOR_DIR)/config/default.ini --mode live

simulator-replay:
	$(SIMULATOR_DIR)/build/f1_telemetry_simulator --config $(SIMULATOR_DIR)/config/default.ini --mode replay --replay-file sample_data/demo_sessions/demo_session.csv

clean:
	-Remove-Item -Recurse -Force $(SIMULATOR_DIR)/build -ErrorAction SilentlyContinue
	-Remove-Item -Recurse -Force $(FRONTEND_DIR)/dist -ErrorAction SilentlyContinue
	-Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
