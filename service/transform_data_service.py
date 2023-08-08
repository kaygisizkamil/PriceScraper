import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from dateutil import parser
from model.hepsiburda_datas import HepsiburadaData
from model.data_from_different_sources import From_different_sources
from sqlalchemy.orm import scoped_session, sessionmaker
import requests



proxy_url = requests.get(
"https://ipv4.webshare.io/",
proxies={
"http": "http://oanuqvtk-rotate:s8dzk069y5jk@p.webshare.io:80/",
"https": "http://oanuqvtk-rotate:s8dzk069y5jk@p.webshare.io:80/"
}
).text

async def fetch_and_parse_product_data(session, data):
    results = []
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "",
    "Sec-Ch-Ua-Mobile": "?0",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Service-Worker-Navigation-Preload": "true",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.vatanbilgisayar.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    }

    async def fetch_data(session, data_tmp, proxy_url):
        specs = {
            'product_name': None,
            'product_link': None,
            'image_link': None,
            'fromWhere': None,
            'saved_time': None,
            'cpu': None,
            'ram': None,
            'screen': None,
            'gpu': None,
            'os': None,
            'ssd': None,
            'hdd': None
        }
        specs['product_name'] = data_tmp['product_name']
        specs['product_link'] = data_tmp['product_link']
        specs['image_link'] = data_tmp['image_link']
        specs['fromWhere'] = data_tmp['fromWhere']
        specs['saved_time'] = data_tmp['saved_time']
        
        async with session.get(data_tmp['product_link'], headers=headers, proxy=proxy_url) as response:
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        property_tab_items = soup.find_all('div', class_='col-lg-6 col-md-6 col-sm-12 col-xs-12 property-tab-item')
                        
                        # RAM
                        ram_item = next((item for item in property_tab_items if 'Ram Özellikleri' in item.text), None)
                        if ram_item:
                            ram_table = ram_item.find('table', class_='product-table')
                            if ram_table:
                                ram_rows = ram_table.find_all('tr')
                                for row in ram_rows:
                                    columns = row.find_all('td')
                                    if len(columns) >= 2:
                                        name = columns[0].text.strip()
                                        if name == 'Ram (Sistem Belleği)':
                                            specs['ram'] = columns[1].text.strip()

                        # Screen
                        screen_item = next((item for item in property_tab_items if 'Ekran Özellikleri' in item.text), None)
                        if screen_item:
                            screen_table = screen_item.find('table', class_='product-table')
                            if screen_table:
                                screen_rows = screen_table.find_all('tr')
                                for row in screen_rows:
                                    columns = row.find_all('td')
                                    if len(columns) >= 2:
                                        name = columns[0].text.strip()
                                        if name == 'Ekran Boyutu':
                                            specs['screen'] = columns[1].text.strip()

                        # GPU
                        gpu_item = next((item for item in property_tab_items if 'Ekran kartı' in item.text), None)
                        if gpu_item:
                            gpu_table = gpu_item.find('table', class_='product-table')
                            if gpu_table:
                                gpu_rows = gpu_table.find_all('tr')
                                for row in gpu_rows:
                                    columns = row.find_all('td')
                                    if len(columns) >= 2:
                                        name = columns[0].text.strip()
                                        if name == 'Ekran Kartı Chipseti':
                                            specs['gpu'] = columns[1].text.strip()

                        # Operating System
                        os_item = next((item for item in property_tab_items if 'İşletim Sistemi' in item.text), None)
                        if os_item:
                            os_table = os_item.find('table', class_='product-table')
                            if os_table:
                                os_rows = os_table.find_all('tr')
                                for row in os_rows:
                                    columns = row.find_all('td')
                                    if len(columns) >= 2:
                                        name = columns[0].text.strip()
                                        if name == 'İşletim Sistemi':
                                            specs['os'] = columns[1].text.strip()
                                            
                        # Processor
                        processor_item = next((item for item in property_tab_items if 'İşlemci Özellikleri' in item.text), None)
                        if processor_item:
                            processor_table = processor_item.find('table', class_='product-table')
                            if processor_table:
                                processor_rows = processor_table.find_all('tr')
                                processor_info = {}
                                for row in processor_rows:
                                    columns = row.find_all('td')
                                    if len(columns) >= 2:
                                        name = columns[0].text.strip()
                                        value = columns[1].text.strip()
                                        if name == 'İşlemci Markası':
                                            processor_info['Marka'] = value
                                        elif name == 'İşlemci Nesli':
                                            processor_info['Nesil'] = value
                                        elif name == 'İşlemci Teknolojisi':
                                            processor_info['Teknoloji'] = value
                                        elif name == 'İşlemci Numarası':
                                            processor_info['Numara'] = value
                                        elif name == 'İşlemci Hızı':
                                            processor_info['Hızı'] = value
                                        elif name == 'İşlemci Ön Bellek':
                                            processor_info['Ön Bellek'] = value
                                        elif name == 'İşlemci Çekirdek Sayısı':
                                            processor_info['Çekirdek Sayısı'] = value

                                # Remove the '<a>' tag and its content from the 'İşlemci Markası' value
                                if 'Marka' in processor_info:
                                    processor_info['Marka'] = processor_info['Marka'].split('\n')[0].strip()

                                processor = f"{processor_info.get('Nesil', '')} {processor_info.get('Marka', '')} {processor_info.get('Teknoloji', '')} {processor_info.get('Numara', '')}"
                                specs['cpu'] = processor
                                    # Processor
                        # Disk Capacity
                        storage_item = next((item for item in property_tab_items if 'HDD Özellikleri' in item.text), None)
                        if storage_item:
                            storage_table = storage_item.find('table', class_='product-table')
                            if storage_table:
                                storage_rows = storage_table.find_all('tr')
                                for row in storage_rows:
                                    columns = row.find_all('td')
                                    if len(columns) >= 2:
                                        name = columns[0].text.strip()
                                        if name == 'Disk Kapasitesi':
                                            storage_capacity = columns[1].find('p').text.strip()

                                            # Extract HDD and SSD capacities with units
                                            capacities = re.findall(r'(\d+\s*(?:TB|GB))', storage_capacity)
                                            if len(capacities) >= 1:
                                                if '+' not in storage_capacity:
                                                    specs['ssd'] = capacities[0]
                                                else:
                                                    specs['hdd'] = capacities[0]
                                            if len(capacities) >= 2:
                                                specs['ssd'] = capacities[1]
                                                specs['hdd']=None
                        results.append(specs)

    tasks = []

    async with aiohttp.ClientSession() as session:
        for item in data:
            tasks.append(fetch_data(session, item, proxy_url))
        await asyncio.gather(*tasks)

    return results


async def fetch_data_from_vatan_source(session: aiohttp.ClientSession, page_number: int)-> list:
        url = f'http://localhost:5000/api/vatan/notebooks/getall?page={page_number}'

        try:
            async with session.get(url) as response:
                data = await response.json()
                #print(data)
                return data
        except aiohttp.ClientError as e:
            print(f"An error occurred while fetching data from source, page {page_number}: {e}")
            return []
    