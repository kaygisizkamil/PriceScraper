import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

async def get_star_rating(review_percentage):
    if review_percentage >= 90:
        return 5
    elif review_percentage >= 80:
        return 4
    elif review_percentage >= 70:
        return 3
    elif review_percentage >= 60:
        return 2
    elif review_percentage >= 50:
        return 1
    else:
        return 0

async def fetch_product_data(session, page_number):
    try:
        url = f"https://www.vatanbilgisayar.com/notebook/?page={page_number}"

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


        async with session.get(url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")

            product_data_list = []

            image_link_elements = soup.find_all('a', class_='product-list__image-safe-link')
            image_links = [img.find('img')['data-src'] if img and img.find('img') and 'data-src' in img.find('img').attrs else "" for img in image_link_elements]

            product_elements = soup.find_all('div', class_='product-list__content')

            for product_element, image_link in zip(product_elements, image_links):
                # Extract product data
                product_name_element = product_element.select_one("div.product-list__product-name h3")
                product_name = product_name_element.text.strip()
                brand_name = product_name.split()[0]

                # Extract product link and then get the product ID from the link
                product_link_element = product_element.select_one("a.product-list__link")
                try:
                    product_link = product_link_element["href"]
                except TypeError:
                    continue

                price_element = product_element.select_one("span.product-list__price")
                price = price_element.text.strip()
                price = int(''.join(filter(str.isdigit, price)))

                # Add base URL to the product link
                base_url = "https://www.vatanbilgisayar.com"
                product_link = base_url + product_link

                # Extract review rating and count
                review_element = product_element.select_one("div.wrapper-star")
                review_score_element = review_element.select_one("span.score")
                review_score_style = review_score_element.get("style", "")
                review_score_match = re.search(r"width:(\d+)%", review_score_style)
                review_score = int(review_score_match.group(1)) if review_score_match else 0
                review_rating = await get_star_rating(review_score)

                # Extract review count
                review_count_element = review_element.select_one("a.comment-count")
                review_count_text = review_count_element.text.strip() if review_count_element else "0"
                review_count_match = re.search(r"\d+", review_count_text)
                review_count = review_count_match.group() if review_count_match else "0"

                product_data_list.append({
                    "product_name": product_name,
                    "brand_name": brand_name,
                    "price": price,
                    "review_rating": review_rating,
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

     