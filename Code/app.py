from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import requests
import time

def scrape_images_unsplash(search_term, output_dir, max_images=200, min_size_kb=20, scroll_pause=2):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-logging")
    service = Service(executable_path="C:\\Windows\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    url = f"https://unsplash.com/s/photos/{search_term}"
    driver.get(url)
    time.sleep(3)
    os.makedirs(output_dir, exist_ok=True)
    downloaded_images = 0
    seen_images = set()
    while downloaded_images < max_images:
        image_elements = driver.find_elements(By.TAG_NAME, "img")
        for img in image_elements:
            if downloaded_images >= max_images:
                break
            img_url = img.get_attribute("src")
            if img_url and img_url not in seen_images:
                seen_images.add(img_url)
                try:
                    response = requests.get(img_url, stream=True)
                    response.raise_for_status()
                    size_kb = int(response.headers.get('Content-Length', 0)) / 1024
                    if size_kb < min_size_kb:
                        continue
                    image_name = f"{output_dir}/image_{downloaded_images + 1}.jpg"
                    with open(image_name, "wb") as f:
                        f.write(response.content)
                    downloaded_images += 1
                except Exception as e:
                    pass
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
    driver.quit()

scrape_images_unsplash(search_term="Crowbar", output_dir="crowbar", max_images=200, min_size_kb=20)
