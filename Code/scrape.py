from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import os

def getimage(var, max_images=100):
    try:
      
        os.makedirs(os.path.join(os.getcwd(), 'images'), exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")

    scrollnum = 200  
    sleepTimer = 2  
    url = f'https://in.pinterest.com/search/pins/?q={var}'

   
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])


    service = Service(executable_path='C:\Windows\chromedriver.exe')  


    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

  
    downloaded_images = 0
    image_urls = set()  

    while downloaded_images < max_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
        print(f'Scrolled down. Images downloaded: {downloaded_images}')
        time.sleep(sleepTimer)  
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for link in soup.find_all('img'):
            img_url = link.get('src')
            if img_url and img_url.startswith('https'): 
               
                if img_url in image_urls:
                    continue  

                
                image_urls.add(img_url)

                category_prefix = var.lower() 
                img_name = f"{category_prefix}_image_{downloaded_images + 1}.png"

           
                img_counter = 1
                while os.path.exists(os.path.join(os.getcwd(), 'Axe', img_name)):
                    img_name = f"{category_prefix}_image_{downloaded_images + 1}_{img_counter}.png"
                    img_counter += 1

                try:
                    
                    img_data = requests.get(img_url).content
                    with open(os.path.join(os.getcwd(), 'Axe', img_name), 'wb') as f:
                        f.write(img_data)
                    print(f"Downloaded: {img_name}")
                    downloaded_images += 1
                except Exception as e:
                    print(f"Failed to download {img_url}: {e}")
            
            if downloaded_images >= max_images:
                break  

    driver.quit()  

getimage('Axe', max_images=500)
  
