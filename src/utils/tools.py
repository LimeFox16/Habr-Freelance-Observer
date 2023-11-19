from bs4 import BeautifulSoup
from posixpath import basename
from typing import List
from urllib.parse import urlparse
import aiohttp

from src.misc.loader import cursor, logger
        
        
async def get_response_data(page: int = 1) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url = f'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other&page={page}'
        ) as response:
            resp_data = await response.read()
    return resp_data


async def return_num(link):
    parse_object = urlparse(link)
    return basename(parse_object.path)


async def get_last_task_id():
    html_content = await get_response_data(page=1)
    soup = BeautifulSoup(html_content)
    last_task = soup.find('li', {'class': 'content-list__item'})
    title = last_task.find('div', {'class': 'task__title'}).find('a')
    
    return await return_num(title.get("href"))


async def get_tasks_info_on_page(page: int = 1, tasks_info: List[dict] = []):
    if page > 5:
        return tasks_info
    
    last_task_id = cursor.execute("SELECT (task_id) FROM Key")
    last_task_id = last_task_id.fetchone()[0]
    
    html_content = await get_response_data(page)
    soup = BeautifulSoup(html_content)
    tasks_list = soup.find_all('li', {'class': 'content-list__item'})

    for task in tasks_list:
        task: BeautifulSoup
        
        title = task.find('div', {'class': 'task__title'}).find('a')
        task_id = await return_num(title.get("href"))
        logger.info(f"last_task_id {last_task_id} >= {task_id}")
        if int(last_task_id) >= int(task_id):
            logger.info(f"return {tasks_info}")
            return tasks_info
        logger.info(f"false")
        is_urgent = False
        if 'content-list__item_marked' in task.get('class'):
           is_urgent = True

        link = 'https://freelance.habr.com/tasks/' + task_id

        task_price = task.find('div', {'class': 'task__price'})
        price = task_price.find('span', {'class': 'negotiated_price'})

        if price:
            price = price.get_text()
        else:
            price = task_price.find('span', {'class': 'count'})
            price = price.text


        tags_list = task.find_all('li', {'class': 'tags__item'})

        tasks_info.append(
            {
                'title': title.get_text(),
                'url': link,
                'price': price,
                'tags': [f'#{x.get_text().replace(" ", "_")}' for x in tags_list],
                'urgent': is_urgent
            }
        )

    return await get_tasks_info_on_page(page=page + 1, tasks_info=tasks_info)

async def get_unread_tasks():
    data = await get_tasks_info_on_page(page=1, tasks_info=[])
    return data