# Настройка CI/CD для Wikipedia Navigator

Этот документ описывает настройку непрерывной интеграции и развертывания (CI/CD) для проекта Wikipedia Navigator.

## 🚀 GitHub Actions Workflows

Проект использует три основных workflow:

### 1. Основной CI/CD пайплайн (`.github/workflows/ci-cd.yml`)

**Триггеры:**
- Push в ветки `main` и `develop`
- Pull Request в ветку `main`

**Этапы:**
1. **Тестирование** - запуск тестов на разных версиях Python
2. **Безопасность** - проверка безопасности кода
3. **Сборка Docker** - создание и публикация Docker образа
4. **Развертывание** - деплой в продакшен

### 2. Проверка Pull Requests (`.github/workflows/pr-check.yml`)

**Триггеры:**
- Pull Request в ветки `main` и `develop`

**Этапы:**
1. Проверка форматирования кода
2. Запуск unit тестов
3. Сканирование безопасности
4. Автоматический комментарий в PR

### 3. Автоматические релизы (`.github/workflows/release.yml`)

**Триггеры:**
- Push тегов вида `v*` (например, `v1.0.0`)

**Этапы:**
1. Запуск тестов
2. Сборка Docker образа
3. Создание GitHub Release
4. Загрузка отчетов о покрытии

## 🔧 Настройка Secrets

Для работы CI/CD необходимо настроить следующие secrets в GitHub:

### Docker Hub
```bash
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password
```

### GitHub Token (автоматически доступен)
```bash
GITHUB_TOKEN=auto_generated
```

## 📋 Настройка в GitHub

### 1. Создание репозитория
```bash
# Клонируйте репозиторий
git clone https://github.com/your-username/wikipedia-navigator.git
cd wikipedia-navigator

# Добавьте remote origin
git remote add origin https://github.com/your-username/wikipedia-navigator.git
```

### 2. Настройка Secrets
1. Перейдите в Settings → Secrets and variables → Actions
2. Добавьте следующие secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

### 3. Настройка Branch Protection
1. Перейдите в Settings → Branches
2. Добавьте правило для ветки `main`:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

## 🏃‍♂️ Запуск CI/CD

### Первый коммит
```bash
# Добавьте все файлы
git add .

# Создайте первый коммит
git commit -m "feat: Initial commit with CI/CD setup"

# Отправьте в GitHub
git push -u origin main
```

### Создание Pull Request
```bash
# Создайте новую ветку
git checkout -b feature/new-feature

# Внесите изменения
# ...

# Закоммитьте изменения
git add .
git commit -m "feat: Add new feature"

# Отправьте ветку
git push origin feature/new-feature
```

### Создание релиза
```bash
# Создайте тег
git tag v1.0.0

# Отправьте тег
git push origin v1.0.0
```

## 📊 Мониторинг

### GitHub Actions Dashboard
- Перейдите в Actions вкладку репозитория
- Просматривайте статус всех workflow

### Artifacts
- Отчеты о покрытии тестами
- Результаты сканирования безопасности
- Docker образы

### Notifications
- Email уведомления о статусе сборки
- Slack/Discord интеграция (опционально)

## 🔍 Troubleshooting

### Частые проблемы

#### 1. Тесты не проходят
```bash
# Запустите тесты локально
make test

# Проверьте покрытие
make test-fast
```

#### 2. Docker сборка падает
```bash
# Проверьте Dockerfile
docker build -t wikipedia-navigator .

# Проверьте docker-compose
docker-compose build
```

#### 3. Проблемы с secrets
- Убедитесь, что secrets настроены правильно
- Проверьте права доступа к Docker Hub

#### 4. Проблемы с кэшем
```bash
# Очистите кэш GitHub Actions
# Перейдите в Actions → Clear cache
```

## 📈 Метрики качества

### Покрытие тестами
- Минимум 80% покрытия кода
- Отчеты генерируются автоматически

### Качество кода
- Flake8 проверка стиля
- Bandit проверка безопасности
- Safety проверка зависимостей

### Производительность
- Время сборки Docker образа
- Время выполнения тестов
- Размер Docker образа

## 🚀 Дальнейшие улучшения

### Возможные расширения:
1. **Kubernetes деплой** - автоматическое развертывание в K8s
2. **AWS/GCP интеграция** - деплой в облачные сервисы
3. **Slack уведомления** - уведомления о статусе сборки
4. **Автоматическое обновление зависимостей** - Dependabot
5. **Performance тесты** - нагрузочное тестирование API

### Мониторинг продакшена:
1. **Health checks** - проверка здоровья сервиса
2. **Metrics** - сбор метрик производительности
3. **Logs** - централизованное логирование
4. **Alerts** - уведомления о проблемах
