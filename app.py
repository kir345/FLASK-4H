import os
from pathlib import Path
import requests
import time
import argparse
import threading
from multiprocessing import Process
import asyncio
import aiohttp


images = []
with open('images.txt', 'r') as f:
    for img in f.readlines():
        images.append(img.strip())

PATH = Path('images')

def download_image(url, dir_path = PATH):
    start_time = time.time()
    answer = requests.get(url)
    file_name = url.split('/')[-1]
    with open(os.path.join(dir_path, file_name), 'wb') as f:
        for data in answer.iter_content(1024):
            f.write(data)
    end_time = time.time() - start_time
    print(f'Загрузка {file_name} заняла {end_time:.2f} сек')

def parse():
    pars = argparse.ArgumentParser(description='Сбор изображений по URL-адресам')
    pars.add_argument('-u', '--urls', default=images, nargs='+', type= str)
    return pars.parse_args()

async def download_imgage_as(url, dir_path = PATH):
    start_time = time.time()
    async with aiohttp.ClientSession() as sessia:
        async with sessia.get(url) as answer:
            item = await answer.read()
            file_name = url.split('/')[-1]
            with open(os.path.join(dir_path, file_name), 'wb') as f:
                f.write(item)
    end_time = time.time() - start_time
    print(f'Загрузка {file_name} заняла {end_time:.2f} сек')

def download_image_flow(urls):
    flows = []
    start_time = time.time()

    for url in urls:
        flow = threading.Thread(target=download_image, args=(url, ))
        flows.append(flow)
        flow.start()

    for flow in flows:
        flow.join()

    end_time = time.time() -  start_time
    print(f'Загрузка заняла {end_time:.2f} сек')

def download_image_proces(urls):
    proceses = []
    start_time = time.time()

    for url in urls:
        proces =  Process(target=download_image, args=(url, ))
        proceses.append(proces)
        proces.start()

    for proces in proceses:
        proces.join()

    end_time = time.time() - start_time
    print(f'Загрузка заняла {end_time:.2f} сек')

async def download_image_async(urls):
    problems = []
    start_time = time.time()

    for url in urls:
        problem =  asyncio.create_task(download_imgage_as(url))
        problems.append(problem)

    await asyncio.gather(*problems)

    end_time = time.time() - start_time
    print(f'Загрузка заняла {end_time:.2f} сек')


if __name__ == '__main__':
    urls =  parse().urls

    if not os.path.exists(PATH):
        os.mkdir(PATH)

    print(f'Загрузка {len(urls)} изображений через мультипотоки')
    download_image_flow

    print(f'Загрузка {len(urls)} изображений через мультипроцессы')
    download_image_proces

    print(f'Загрузка {len(urls)} изображений асинхронно')
    asyncio.run(download_image_async(urls))






