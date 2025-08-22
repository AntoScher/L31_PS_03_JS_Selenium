from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import json
import time
from datetime import datetime
from functools import wraps

from main import create_driver, search_wikipedia, print_contents, print_paragraphs, print_links
from logger import setup_logger
from data_manager import DataManager
from config import Config

app = Flask(__name__)
CORS(app)

# Настройка лимитера запросов
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Инициализация Redis для кэширования
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Инициализация логгера и менеджера данных
logger = setup_logger()
data_manager = DataManager()

# HTML шаблон для веб-интерфейса
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wikipedia Navigator API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .container { display: flex; gap: 20px; }
        .search-panel { flex: 1; }
        .results-panel { flex: 2; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, button { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 4px; }
        .error { color: red; }
        .success { color: green; }
        .loading { display: none; }
    </style>
</head>
<body>
    <h1>Wikipedia Navigator API</h1>
    <div class="container">
        <div class="search-panel">
            <h2>Поиск</h2>
            <div class="form-group">
                <label for="query">Поисковый запрос:</label>
                <input type="text" id="query" placeholder="Введите запрос...">
            </div>
            <div class="form-group">
                <label for="action">Действие:</label>
                <select id="action">
                    <option value="search">Поиск статьи</option>
                    <option value="contents">Получить оглавление</option>
                    <option value="paragraphs">Получить параграфы</option>
                    <option value="links">Получить ссылки</option>
                </select>
            </div>
            <button onclick="performAction()">Выполнить</button>
            <div class="loading" id="loading">Загрузка...</div>
        </div>
        <div class="results-panel">
            <h2>Результаты</h2>
            <div id="results"></div>
        </div>
    </div>

    <script>
        async function performAction() {
            const query = document.getElementById('query').value;
            const action = document.getElementById('action').value;
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');

            if (!query) {
                results.innerHTML = '<div class="error">Введите поисковый запрос</div>';
                return;
            }

            loading.style.display = 'block';
            results.innerHTML = '';

            try {
                const response = await fetch(`/api/${action}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();
                
                if (response.ok) {
                    displayResults(data);
                } else {
                    results.innerHTML = `<div class="error">Ошибка: ${data.error}</div>`;
                }
            } catch (error) {
                results.innerHTML = `<div class="error">Ошибка сети: ${error.message}</div>`;
            } finally {
                loading.style.display = 'none';
            }
        }

        function displayResults(data) {
            const results = document.getElementById('results');
            let html = '<div class="success">Запрос выполнен успешно!</div>';
            
            if (data.results) {
                html += '<div class="result">';
                if (Array.isArray(data.results)) {
                    data.results.forEach((item, index) => {
                        html += `<p><strong>${index + 1}.</strong> ${item}</p>`;
                    });
                } else {
                    html += `<pre>${JSON.stringify(data.results, null, 2)}</pre>`;
                }
                html += '</div>';
            }
            
            results.innerHTML = html;
        }
    </script>
</body>
</html>
"""

def cache_result(func):
    """Декоратор для кэширования результатов"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Создаем ключ кэша
        cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
        
        # Проверяем кэш
        cached_result = redis_client.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for {cache_key}")
            return json.loads(cached_result)
        
        # Выполняем функцию
        result = func(*args, **kwargs)
        
        # Сохраняем в кэш на 1 час
        redis_client.setex(cache_key, 3600, json.dumps(result))
        logger.info(f"Cache miss for {cache_key}, stored result")
        
        return result
    return wrapper

@app.route('/')
def index():
    """Главная страница с веб-интерфейсом"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
@limiter.limit("10 per minute")
@cache_result
def api_search():
    """API для поиска статей"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        logger.info(f"API search request: {query}")
        
        # Выполняем поиск
        driver = search_wikipedia(query)
        if not driver:
            return jsonify({'error': 'Failed to initialize browser'}), 500
        
        # Получаем заголовок страницы
        title = driver.title
        
        # Сохраняем историю поиска
        data_manager.save_search_history(query, [{'title': title, 'url': driver.current_url}])
        
        driver.quit()
        
        return jsonify({
            'success': True,
            'query': query,
            'title': title,
            'url': driver.current_url
        })
        
    except Exception as e:
        logger.error(f"API search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/contents', methods=['POST'])
@limiter.limit("20 per minute")
def api_contents():
    """API для получения оглавления"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        logger.info(f"API contents request: {query}")
        
        driver = search_wikipedia(query)
        if not driver:
            return jsonify({'error': 'Failed to initialize browser'}), 500
        
        contents = print_contents(driver)
        contents_text = [item.text for item in contents] if contents else []
        
        driver.quit()
        
        return jsonify({
            'success': True,
            'query': query,
            'results': contents_text
        })
        
    except Exception as e:
        logger.error(f"API contents error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/paragraphs', methods=['POST'])
@limiter.limit("15 per minute")
def api_paragraphs():
    """API для получения параграфов"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        logger.info(f"API paragraphs request: {query}")
        
        driver = search_wikipedia(query)
        if not driver:
            return jsonify({'error': 'Failed to initialize browser'}), 500
        
        paragraphs = driver.find_elements('tag name', 'p')
        paragraphs_text = [p.text for p in paragraphs if p.text.strip()]
        
        # Экспортируем в CSV
        data_manager.export_paragraphs_to_csv(paragraphs_text)
        
        driver.quit()
        
        return jsonify({
            'success': True,
            'query': query,
            'results': paragraphs_text[:10]  # Возвращаем первые 10 параграфов
        })
        
    except Exception as e:
        logger.error(f"API paragraphs error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/links', methods=['POST'])
@limiter.limit("15 per minute")
def api_links():
    """API для получения ссылок"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        logger.info(f"API links request: {query}")
        
        driver = search_wikipedia(query)
        if not driver:
            return jsonify({'error': 'Failed to initialize browser'}), 500
        
        links = driver.find_elements('css selector', "a[href^='/wiki/']")
        links_data = [
            {'text': link.text, 'url': link.get_attribute('href')}
            for link in links if link.text.strip()
        ]
        
        # Экспортируем в CSV
        data_manager.export_links_to_csv(links_data)
        
        driver.quit()
        
        return jsonify({
            'success': True,
            'query': query,
            'results': links_data[:20]  # Возвращаем первые 20 ссылок
        })
        
    except Exception as e:
        logger.error(f"API links error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API для получения статистики"""
    try:
        stats = data_manager.get_search_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        logger.error(f"API stats error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'redis_connected': redis_client.ping()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
