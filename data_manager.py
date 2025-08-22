import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any

class DataManager:
    """Менеджер для работы с данными"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Создает директорию для выходных файлов"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_search_history(self, query: str, results: List[Dict[str, Any]]):
        """Сохраняет историю поиска"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/search_history_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'results': results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def export_paragraphs_to_csv(self, paragraphs: List[str], filename: str = None):
        """Экспортирует параграфы в CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/paragraphs_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Paragraph'])
            for i, paragraph in enumerate(paragraphs, 1):
                writer.writerow([i, paragraph])
        
        return filename
    
    def export_links_to_csv(self, links: List[Dict[str, str]], filename: str = None):
        """Экспортирует ссылки в CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/links_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Text', 'URL'])
            for i, link in enumerate(links, 1):
                writer.writerow([i, link.get('text', ''), link.get('url', '')])
        
        return filename
    
    def save_page_content(self, title: str, content: Dict[str, Any]):
        """Сохраняет содержимое страницы"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{self.output_dir}/page_{safe_title}_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'content': content
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Получает статистику поисков"""
        stats = {
            'total_searches': 0,
            'total_pages_saved': 0,
            'last_search': None
        }
        
        if os.path.exists(self.output_dir):
            files = os.listdir(self.output_dir)
            stats['total_searches'] = len([f for f in files if f.startswith('search_history_')])
            stats['total_pages_saved'] = len([f for f in files if f.startswith('page_')])
            
            if stats['total_searches'] > 0:
                search_files = [f for f in files if f.startswith('search_history_')]
                search_files.sort()
                stats['last_search'] = search_files[-1]
        
        return stats
