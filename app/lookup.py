import asyncio
import logging
import os
import maigret
from maigret import search as maigret_search
from maigret.sites import MaigretDatabase

# Создаем логгер (можно один раз на весь файл)
logger = logging.getLogger("maigret")
logger.setLevel(logging.WARNING)

async def check_username_maigret(username: str):
    try:
        maigret_dir = os.path.dirname(maigret.__file__)
        db_path = os.path.join(maigret_dir, "resources", "data.json")
        
        db = MaigretDatabase().load_from_path(db_path)
        sites = db.ranked_sites_dict(top=100) 
        
        # Добавлен аргумент logger=logger
        results = await maigret_search(
            username=username,
            site_dict=sites,
            logger=logger, 
            timeout=10,
        )
        
        found = []
        for site_name, result in results.items():
            if result["status"].is_found():
                found.append(f"✅ {site_name}: {result['url_user']}")   
                
        if not found:
            return f"По нику '{username}' профили не найдены."
            
        result_text = f"Найдено {len(found)} профилей:\n\n" + "\n".join(found[:15])
        if len(found) > 15:
            result_text += f"\n\n... и еще {len(found) - 15}"
            
        return result_text
        
    except Exception as e:
        return f"[!] Ошибка при поиске: {str(e)}"