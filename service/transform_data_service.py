import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from dateutil import parser
from model.hepsiburda_datas import HepsiburadaData
from model.data_from_different_sources import From_different_sources
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

async def fetch_and_parse_product_data_vatan(session, data):
    results = []
  #  concurrency_limit = 10  
   # semaphore = asyncio.Semaphore(concurrency_limit)
    async def process_data_for_single_product_vatan(data_tmp):
            try:
                #url = "https://www.vatanbilgisayar.com/dell-vostro-14-3400-11-nesil-core-i5-1135g7-8gb-256gb-1tb-15-6inc-mx330-2gb-w11.html"

                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cache-Control": "max-age=0",
                        "Referer": f"https://www.vatanbilgisayar.com/",
                        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": "\"Windows\"",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                    }
                
                    #async with aiohttp.ClientSession() as session:
                    specs = {
                        'price':None,
                        'brand_name':None,
                        'product_name':None,
                        'product_link':None,
                        'image_link':None,
                        'fromWhere':None,
                        'saved_time':None,
                        'cpu': None,
                        'ram': None,
                        'screen': None,
                        'gpu': None,
                        'os': None,
                        'ssd': None,
                        'hdd': None,
                        'review_rating':None,
                        'review_count':None
                    }
                    
                    specs['review_rating']=data_tmp['review_rating']
                    specs['review_count']=data_tmp['review_count']
                    specs['price']=data_tmp['price']
                    specs['brand_name']=data_tmp['brand_name']
                    specs['product_name']=data_tmp['product_name']
                    specs['product_link']=data_tmp['product_link']
                    specs['image_link']=data_tmp['image_link']
                    specs['fromWhere']=data_tmp['fromWhere']
                    specs['saved_time']=data_tmp['saved_time']
                    proxy="http://oanuqvtk-rotate:s8dzk069y5jk@p.webshare.io:80/"
                    

                    async with session.get(data_tmp['product_link'], headers=headers, proxy=proxy) as response:
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
                                            ram_value = columns[1].text.strip()
                                            specs['ram'] = ram_value.replace(' ', '').lower()


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
                                            screen_text= columns[1].text.strip()
                                            numeric_screen_size = re.search(r'(\d+[,.]\d+)', screen_text)
                                            if numeric_screen_size:
                                                screen_value = numeric_screen_size.group(1)
                                                # Replace comma with dot as the decimal separator
                                                screen_value = screen_value.replace(',', '.')
                                                specs['screen'] = screen_value
                                            else :
                                                specs['screen']=screen_text

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
                                            gpu_value = columns[1].text.strip()
                                            specs['gpu'] = gpu_value.lower()

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
                                            os_value= columns[1].text.strip()
                                            specs['os'] = os_value.lower()
                                            
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
                                specs['cpu'] = processor.lower()
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
                                                    specs['ssd'] = capacities[0].lower()
                                                else:
                                                    specs['hdd'] = capacities[0].lower()
                                            if len(capacities) >= 2:
                                                specs['ssd'] = capacities[1].lower()
                                                specs['hdd']=None
                        return specs
                        #results.append(specs)
                                                
                        #print(specs)    
            except aiohttp.ClientError as client_error:
                print(f"Aiohttp ClientError: {client_error}")
                return None
            except Exception as e:
                print(f"Exception: {e} while processing data, continuing...")
                return None
# Chunk the data for parallel processing
    chunk_size = 5
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    for chunk in chunked_data:
        tasks = [process_data_for_single_product_vatan(data_tmp) for data_tmp in chunk]
        chunk_results = await asyncio.gather(*tasks)
        results.extend(chunk_results)
        
    #print(results)
    return results
    
    
async def fetch_and_parse_product_data_hb(session, data):
    results = []
  #  concurrency_limit = 10  
   # semaphore = asyncio.Semaphore(concurrency_limit)
    async def process_data_for_single_product_hb(data_tmp):
            try:
                #url = "https://www.vatanbilgisayar.com/dell-vostro-14-3400-11-nesil-core-i5-1135g7-8gb-256gb-1tb-15-6inc-mx330-2gb-w11.html"

                    headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
                            "Cache-Control": "max-age=0",
                            "Sec-Ch-Ua": "",
                            "Sec-Ch-Ua-Mobile": "?0",
                            "Sec-Ch-Ua-Platform": "\"\"",
                            "Upgrade-Insecure-Requests": "1",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "Service-Worker-Navigation-Preload": "true",
                            "Sec-Fetch-Site": "same-origin",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-User": "?1",
                            "Sec-Fetch-Dest": "document",
                            "Referer": "https://www.hepsiburada.com/",
                            "Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "en-US,en;q=0.9",
                    }
                
                    #async with aiohttp.ClientSession() as session:
                    specs = {
                        'price':None,
                        'brand_name':None,
                        'product_name':None,
                        'product_link':None,
                        'image_link':None,
                        'fromWhere':None,
                        'saved_time':None,
                        'cpu': None,
                        'ram': None,
                        'screen': None,
                        'gpu': None,
                        'os': None,
                        'ssd': None,
                        'hdd': None,
                        'review_rating':None,
                        'review_count':None
                    }
                    specs['review_rating']=data_tmp['review_rating']
                    specs['review_count']=data_tmp['review_count']
                    specs['price']=data_tmp['price']
                    specs['brand_name']=data_tmp['brand_name']
                    specs['product_name']=data_tmp['product_name']
                    specs['product_link']=data_tmp['product_link']
                   # specs['image_link']=data_tmp['image_link'] reurns wron
                    specs['fromWhere']=data_tmp['fromWhere']
                    specs['saved_time']=data_tmp['saved_time']
                    proxy="http://oanuqvtk-rotate:s8dzk069y5jk@p.webshare.io:80/"
                    

                    async with session.get(data_tmp['product_link'], headers=headers, proxy=proxy) as response:
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        tech_spec_table = soup.find('table', class_='data-list tech-spec')
                        if tech_spec_table:
                            # Initialize variables to store individual CPU properties
                            cpu_nesli = None
                            cpu_tipi = None
                            cpu_islemci = None
                            
                            # Iterate through each row in the table
                            for row in tech_spec_table.find_all('tr'):
                                th = row.find('th')
                                td = row.find('td')
                                if th and td:
                                    property_name = th.get_text(strip=True)
                                    property_value = td.get_text(strip=True).lower() 
                                    
                                    # Extract CPU properties
                                    if property_name == 'İşlemci Nesli':
                                        cpu_nesli = property_value
                                    elif property_name == 'İşlemci Tipi':
                                        cpu_tipi = property_value
                                    elif property_name == 'İşlemci':
                                        cpu_islemci = property_value
                                    # Map other property names to the corresponding keys in the 'specs' dictionary
                                    elif property_name == 'Ram (Sistem Belleği)':
                                        specs['ram'] = property_value
                                    elif property_name == 'Ekran Boyutu':
                                        screen_text = property_value
                                        numeric_screen_size = re.search(r'(\d+[,.]\d+)', screen_text)
                                        if numeric_screen_size:
                                            screen_value = numeric_screen_size.group(1)
                                            # Replace comma with dot as the decimal separator
                                            screen_value = screen_value.replace(',', '.')
                                            specs['screen'] = screen_value
                                   
                                    elif property_name == 'Ekran Kartı':
                                        specs['gpu'] = property_value
                                    elif property_name == 'İşletim Sistemi':
                                        specs['os'] = property_value
                                    elif property_name == 'SSD Kapasitesi':
                                        specs['ssd'] = property_value
                                    elif property_name == 'Harddisk Kapasitesi':
                                        specs['hdd'] = property_value
                                  
                                    # Construct the 'cpu' property if at least one component is present
                                    if cpu_nesli or cpu_tipi or cpu_islemci:
                                        cpu_components = [comp for comp in (cpu_nesli, cpu_tipi, cpu_islemci) if comp]
                                        specs['cpu'] = ' '.join(cpu_components)
                                    link_tag = soup.find('link', rel='preload', imagesrcset=True)
                                    
                            if link_tag and 'imagesrcset' in link_tag.attrs:
                                        imagesrcset = link_tag['imagesrcset']
                                        image_link_match = re.search(r'^(.*?)/format:webp', imagesrcset)
                                        if image_link_match:
                                            image_link = image_link_match.group(1)
                                            if len(image_link) <= 255:
                                                specs['image_link'] = image_link        

                        return specs
                        #results.append(specs)
                                                
                        #print(specs)    
            except aiohttp.ClientError as client_error:
                print(f"Aiohttp ClientError: {client_error}")
                return None
            except Exception as e:
                print(f"Exception: {e} while processing data, continuing...")
                return None
# Chunk the data for parallel processing
    chunk_size = 5
    chunked_data = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    for chunk in chunked_data:
        tasks = [process_data_for_single_product_hb(data_tmp) for data_tmp in chunk]
        chunk_results = await asyncio.gather(*tasks)
        results.extend(chunk_results)
        
   # print(results)
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
    
async def fetch_data_from_hb_source(session: aiohttp.ClientSession, page_number: int)-> list:
    url = f'http://localhost:5000/api/hepsiburda/notebooks/getall?page={page_number}'

    try:
        async with session.get(url) as response:
            data = await response.json()
            #print(data)
            return data
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching data from source, page {page_number}: {e}")
        return []