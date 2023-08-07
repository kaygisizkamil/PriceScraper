import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import urllib.parse

async def extract_product_properties(session, page_number):
    try:
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
            "Referer": "https://www.n11.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        }
        url = f"https://www.n11.com/bilgisayar/dizustu-bilgisayar?pg={page_number}"
        async with session.get(url, headers=headers) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
                list_ul = soup.find("ul", class_="list-ul")
                product_items = list_ul.find_all("li", class_="column")
                product_data_list = [] 

                # Extract product ID, brand, and name
                for product_item in product_items :
                    product_link = product_item.find("a", class_="plink")
                    product_id = product_link["data-id"]
                    brand, name = product_link["title"].split(" ", 1)
                    name = f"{brand} {name}"


                    # Extract image link
                    image_link = product_item.find("img", class_="lazy")["data-original"]

                    # Extract price
                    price_container = product_item.find("span", class_="newPrice")
                    #price = re.sub(r"[^0-9.,]", "", price_container.text)                 
                    parts =price_container.text.split(",")
                    integer_part = parts[0] # Take the part before the comma
                    integer_part = integer_part.replace(".","")  
                    price = int(integer_part)

                    rating_map = {
                        "r100": 5.0,
                        "r90": 4.5,
                        "r80": 4.0,
                        "r70": 3.5,
                        "r60": 3.0,
                        "r50": 2.5,
                        "r40": 2.0,
                        "r30": 1.5,
                        "r20": 1.0,
                        "r10": 0.5,
                        "rating": 0.0
                    }

                    rating_container = product_item.find("div", class_="ratingCont")
                    review_rating = 0
                    review_count = 0
                    if rating_container:
                        rating_span = rating_container.find("span", class_="rating")
                        if rating_span:
                            rating_class = rating_span.get("class")[1]
                            review_rating = rating_map.get(rating_class, 0)

                        review_count_span = rating_container.find("span", class_="ratingText")
                        if review_count_span:
                            review_count = int(review_count_span.text.strip("()"))

                    # Extract decoded URL
                    decoded_url = product_link["href"]
                    product_data_list.append({
                               "product_name": name,
                                "brand_name": brand,                                                           
                                "price": price,
                                "review_rating": review_rating,
                                "review_count": review_count,
                                "image_link": image_link,
                                "product_link": decoded_url
                    })
                return product_data_list
    except Exception as e:
        print(f"Exception in page {page_number}: {e}")
        return None

async def get_product_data(page_number):
        async with aiohttp.ClientSession() as session:
            return await extract_product_properties(session, page_number)


