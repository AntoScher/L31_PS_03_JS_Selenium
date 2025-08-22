.PHONY: help install test lint clean docker-build docker-run docker-stop api cli

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

test: ## Запустить тесты
	pytest tests/ -v --cov=. --cov-report=html

test-fast: ## Запустить быстрые тесты
	pytest tests/ -v -m "not slow"

lint: ## Проверить код линтером
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

security: ## Проверить безопасность
	bandit -r . -f json -o bandit-report.json
	safety check --json --output safety-report.json

clean: ## Очистить временные файлы
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Собрать Docker образ
	docker build -t wikipedia-navigator .

docker-run: ## Запустить в Docker
	docker-compose up -d

docker-stop: ## Остановить Docker контейнеры
	docker-compose down

api: ## Запустить API сервер
	python api_server.py

cli: ## Запустить CLI приложение
	python main.py

dev: ## Запустить в режиме разработки
	python api_server.py --debug

logs: ## Показать логи
	tail -f logs/wikipedia_navigator_*.log

stats: ## Показать статистику
	curl http://localhost:8000/api/stats

health: ## Проверить здоровье сервиса
	curl http://localhost:8000/health

all: install test lint security ## Выполнить все проверки
