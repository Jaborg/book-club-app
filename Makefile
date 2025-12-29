setup:
	 python3 -m venv .venv
	 .venv/bin/python3 -m pip install --upgrade pip
	 .venv/bin/pip3 install -r requirements.txt


run_app:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run_app_docker:
	docker compose up -d --build

close_docker:
	docker compose down --volumes