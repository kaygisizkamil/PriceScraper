import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

async def fetch_product_data(session, page_number):
    try:
        url = f"https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={page_number}"

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


        async with session.get(url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")

            product_data_list = []

            product_elements = soup.find_all('div', class_='product-item')
            for product_element in product_elements:
                # Extract product data
                product_name_element = product_element.select_one("a.product-link")
                product_name = product_name_element.text.strip()
                brand_name = product_name.split()[0]

                # Extract product link and then get the product ID from the link
                product_link = product_name_element['href']

                price_element = product_element.select_one("div.price-value")
                price = price_element.text.strip()
                price = int(''.join(filter(str.isdigit, price)))

                # Extract review rating and count
                review_element = product_element.select_one("div.review")
                review_score_element = review_element.select_one("span.star")
                review_score_style = review_score_element.get("style", "")
                review_score_match = re.search(r"width:(\d+)%", review_score_style)
                review_score = int(review_score_match.group(1)) if review_score_match else 0
               # review_rating = await get_star_rating(review_score)

                review_count_element = review_element.select_one("span.review-count")
                review_count_text = review_count_element.text.strip() if review_count_element else "0"
                review_count_match = re.search(r"\d+", review_count_text)
                review_count = review_count_match.group() if review_count_match else "0"

                # Extract image link
                image_link_element = product_element.select_one("img.product-image")
                image_link = image_link_element['src'] if image_link_element else ""

                product_data_list.append({
                    "product_name": product_name,
                    "brand_name": brand_name,
                    "price": price,
                    "review_rating": review_score,
                    "review_count": review_count,
                    "product_link": product_link,
                    "image_link": image_link
                })

            return product_data_list

    except Exception as e:
        print(f"Exception in page {page_number}: {e}")
        return None

async def get_product_data(page_number):
    async with aiohttp.ClientSession() as session:
        return await fetch_product_data(session, page_number)