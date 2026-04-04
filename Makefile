.PHONY: dev dev-backend dev-frontend install install-backend install-frontend

install-backend:
	cd backend && uv venv .venv --clear && uv pip install setuptools scipy && uv pip install fastapi "uvicorn[standard]" python-multipart pandas pydantic-settings pandasai pytest pytest-asyncio httpx

install-frontend:
	cd frontend && npm install

install: install-backend install-frontend

dev-backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Run in two terminals:"
	@echo "  make dev-backend"
	@echo "  make dev-frontend"
