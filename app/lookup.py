import asyncio
import os
import maigret
from maigret import search as maigret_search
from maigret.sites import MaigretDatabase

async def check_username_maigret(username: str):
    try:
        # 1. Правильный путь к базе данных (ищем в папке установленного пакета)
        maigret_dir = os.path.dirname(maigret.__file__)
        db_path = os.path.join(maigret_dir, "resources", "data.json")
        
        db = MaigretDatabase().load_from_path(db_path)
        
        # 2. Берем топ-100 сайтов (чтобы бот не завис на 5 минут)
        sites = db.ranked_sites_dict(top=100) 
        
        # 3. Запускаем поиск
        results = await maigret_search(
            username=username,
            site_dict=sites,
            timeout=10,
        )
        
        found = []
        for site_name, result in results.items():
            if result["status"].is_found():
                found.append(f"✅ {site_name}: {result['url_user']}")   
                
        if not found:
            return f"По нику '{username}' профили не найдены."
            
        # Ограничиваем вывод, чтобы не превысить лимит сообщения в Telegram (4096 символов)
        result_text = f"Найдено {len(found)} профилей:\n\n" + "\n".join(found[:15])
        if len(found) > 15:
            result_text += f"\n\n... и еще {len(found) - 15}"
            
        return result_text
        
    except Exception as e:
        return f"[!] Ошибка при поиске: {str(e)}"