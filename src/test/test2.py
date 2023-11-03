import asyncio
import aiohttp
from urllib.request import urlopen, Request
from fake_headers import Headers, random_browser, random_os, headers
from bs4 import BeautifulSoup
from pprint import pprint
from posixpath import basename#, dirname
from urllib.parse import urlparse


def return_num(link):
    parse_object = urlparse(link)
    return basename(parse_object.path)

async def get_response_data() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url = 'https://freelance.habr.com/tasks'
        ) as response:
            resp_data = await response.read()
    return resp_data

async def main():
    html_content = await get_response_data()
    soup = BeautifulSoup(html_content)
    tasks_list = soup.find_all('li', {'class': 'content-list__item'})

    for task in tasks_list:
        task: BeautifulSoup
        
        if 'content-list__item_marked' in task.get('class'):
            print("Срочный заказ")

        title = task.find('div', {'class': 'task__title'}).find('a')

        link = 'https://freelance.habr.com/tasks/' + return_num(title.get("href"))

        task_price = task.find('div', {'class': 'task__price'})
        price = task_price.find('span', {'class': 'negotiated_price'})

        if price:
            price = price.get_text()
        else:
            price = task_price.find('span', {'class': 'count'})
            price = price.text


        tags_list = task.find_all('li', {'class': 'tags__item'})

        print(' '.join(f'#{x.get_text().replace(" ", "_")}' for x in tags_list))
        print(title.get_text())
        print(link)
        print('Цена:', price)
        print()




if __name__ == "__main__":
    asyncio.run(main())