import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import urllib.parse
from decimal import Decimal

async def get_product_data_infos(session, page_number):
    try:
        page_url = f"https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={page_number}"
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

        async def get_product_and_image_data(page_url):
            product_data_list = []
            proxy="http://oanuqvtk-rotate:s8dzk069y5jk@p.webshare.io:80/"
                    

            response = await session.get(page_url, headers=headers,proxy=proxy)
            soup = BeautifulSoup(await response.text(), "html.parser")
            script_tags = soup.find_all("script", type="text/javascript")

            for script_tag in script_tags:
                script_text = script_tag.get_text()
                if "window.MORIA.VERTICALFILTER" in script_text:
                    # Use regex to extract the required data
                    matches = re.findall(r'"productId":"(.*?)","brand":"(.*?)".*?"name":"(.*?)"', script_text)
                    product_data_list = matches

                    # Extract image links from the script tag
                    image_links = re.findall(r'"link":"(https://productimages.hepsiburada.net.*?)",', script_text)
                    # Replace {size} in image links with the specified size
                    image_links = [link.replace("{size}", str(200)) for link in image_links]

                    # Extract prices 
                    price_strings = re.findall(r'"price":(\d+(?:\.\d+)?)', script_text)  

                    # Extract all prices from the string list  
                    prices = []  
                    for price in price_strings:
                        if "." in price:
                            parts = price.split(".")
                            integer_part = parts[0]    
                        else:     
                            parts = price.split(",")   
                            integer_part = parts[0]
                            
                        integer_part = integer_part.replace(".", "")  
                        decimal_price = Decimal(integer_part)    
                        prices.append(decimal_price.to_integral_value())
                   
                    # Extract customer review rating and count
                    review_ratings = re.findall(r'"customerReviewRating":(\d+(?:\.\d+)?)', script_text)
                    review_counts = re.findall(r'"customerReviewCount":(\d+)', script_text)

                    # Extract and decode the URL
                    url_part = re.findall(r'"url":"(.*?)"', script_text)
                    decoded_urls = [urllib.parse.unquote(url) for url in url_part]
                    decoded_urls = ['https://www.hepsiburada.com/' + url if not url.startswith('http') else url for url in decoded_urls]

                    # Add "https://" to URLs that don't already have it
                    return product_data_list, image_links, prices, review_ratings, review_counts, decoded_urls

            # Return None if no reasonable product data is found
            return None, None, None, None, None, None

        # Call the nested function with the page_url argument
        product_data, image_links, prices, review_ratings, review_counts, decoded_urls = await get_product_and_image_data(page_url)

        if not product_data or not image_links or not prices or not review_ratings or not review_counts or not decoded_urls:
            # Stop if no reasonable product data is found
            return None

        product_data_lists = []
        for i, (product, image_link, price, rating, count, decoded_url) in enumerate(zip(product_data, image_links, prices, review_ratings, review_counts, decoded_urls)):
            _, brand, name = product
            name = name.rstrip('\\')
            name=name.lower()
            brand=brand.lower()
            if(len(decoded_url)>255):continue

            product_data_lists.append({
                "product_name": name,
                "brand_name": brand,
                "price": price,
                "review_rating": rating,
                "review_count": count,
                "product_link": decoded_url,
                "image_link": image_link
            })

        return product_data_lists

    except Exception as e:
        print(f"Exception in page {page_number}: {e}")
        return None

async def get_product_data(page_number):
    async with aiohttp.ClientSession() as session:
        return await get_product_data_infos(session, page_number)