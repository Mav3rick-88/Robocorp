from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from urllib.request import urlretrieve
from urllib.request import Request, urlopen
import datetime
import os
from time import sleep
#import RPA.Browser.Selenium as Browser


class Browser:
    def __init__(self):
        pass

    def star_page():
        firefox_options = Options()
        firefox_options.add_argument('--ignore-ssl-errors=yes')
        firefox_options.add_argument('--ignore-certificate-errors')
        service = Service()
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver
    
    def get_search_results_count(driver):
        # Assuming the number of results is contained in an element with a specific class name
        # You'll need to replace 'results-count-class' with the actual class name or use a different locator
        results_element = driver.find_element(By.CLASS_NAME, 'results-count-class')
        results_text = results_element.text
        # Extract the number from the text. This might need to be adjusted based on the format of the text.
        # For example, if the text is "About 1,000 results", the following line extracts "1000".
        num_results = int(''.join(filter(str.isdigit, results_text)))
        return num_results


    def open_page(driver, url):
        driver.get(url)

    def find_element(driver, value):
        elemet = driver.find_element(By.CLASS_NAME, value)
        return elemet
    
    def find_elements_under_element(parent_element, child_locator, child_value):
        return parent_element.find_elements(child_locator, child_value)

    def close(driver):
        driver.quit()
    
    def click(element):
        element.click()
    
    def download_image(in_folder, in_url, in_name_name):
        news_image_src=in_url
        req = Request(news_image_src)
        max_attempts = 5
        attempts = 0
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        file_path = f"{in_folder}/{in_name_name}.jpg"

        # Create 'Images' directory if it doesn't exist
        images_dir = in_folder
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        # Continue with the rest of your code...
        while not os.path.exists(file_path) and attempts < max_attempts:
            try:
                with urlopen(req) as response, open(file_path, 'wb') as out_file:
                    data = response.read()  # Read the response data
                    out_file.write(data)  # Write the data to a file
                print(f"Fil e {file_path} successfully downloaded.")
            except Exception as e:
                print(f"Attempt {attempts + 1} failed: {e}")
                attempts += 1
                sleep(2)  # Wait for 2 seconds before trying again

        if not os.path.exists(file_path):
            print(f"Failed to download the file after {max_attempts} attempts.")
        return file_path
        """ 
        with urlopen(req) as response, open(f"Images/{in_name_name}.jpg", 'wb') as out_file:
            data = response.read()  # Read the response data
            out_file.write(data)  # Write the data to a file
        """

    

            # Optional: Save the DataFrame to a CSV file

    def get_download_sub(driver):
        children = search_result.find_elements(By.XPATH,"./*")
        page_counter = 2
        counter = 0
        in_counter = 0
        money_text = ['$', 'USD', 'dollar', 'Dollar', 'Usd']
        full_text = ""
        date_folder = f"Images/{today}"
        # Iterate over the children
        for child in children:
            full_text = child.text
            #image = child.find_element(By.XPATH, "img")
            data_news = []

            for child in children:
                full_text = child.text
                news_image = child.find_element(By.CLASS_NAME, "Image")
                news_image_src = news_image.get_attribute("src")

                # Assuming full_text contains at least two '\n', allowing for a split into three parts
                if len(full_text) < 1:
                    ...
                else:
    
                    news_header, news_text, new_date = full_text.split('\n', 2)
                    words = news_header.split()
                    # Take the first four words from the list
                    first_four_words = words[:4]
                    # Join these four words back into a string
                    image_name = ' '.join(first_four_words)
                    download_image(date_folder, news_image_src, image_name)
                    # Check if the news_text contains any of the words in money_text
                    is_money = False  # Initialize a flag to False
                    for money in money_text:
                        if money in full_text:
                            is_money = True  # Set the flag to True if the condition is met
                            break  # Exit the loop if the condition is met
                    data_news.append({
                    'Title': news_header,
                    'Description': news_text,
                    'Date': new_date,
                    'Money?': is_money,
                    'Image': news_image_src 
                    })

            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(data_news)

            # Optional: Save the DataFrame to a CSV file
            df.to_csv(save_path, index=False)  

    def next_page(driver):
        driver.find_element(By.XPATH, '/html/body/div[3]/bsp-search-results-module/form/div[2]/div/bsp-search-filters/div/main/div[4]/div[3]/a/svg').click()          
        return driver
    start=star_page()
    today = datetime.date.today().strftime('%d-%m-%Y')
    save_path = f"Output/{today}.csv"
    webpage=open_page(start, "https://apnews.com/")
    magnify=find_element(start, 'icon-magnify')
    click(magnify)
    search_bar=find_element(start, 'SearchOverlay-search-input')
    search_bar.clear()
    search_bar.send_keys("Biden")
    search_bar.submit()
    #resutl_number = get_search_results_count(start)
    #print(resutl_number)
    search_result = WebDriverWait(start, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div[3]/bsp-search-results-module/form/div[2]/div/bsp-search-filters/div/main/div[3]/bsp-list-loadmore/div[2]""")))
    children = search_result.find_elements(By.XPATH,"./*")
    page_counter = 2
    money_text = ['$', 'USD', 'dollar', 'Dollar', 'Usd']
    full_text = ""
    date_folder = f"Images/{today}"
    # Iterate over the children
    for child in children:
        full_text = child.text
        #image = child.find_element(By.XPATH, "img")
        data_news = []

        for child in children:
            full_text = child.text
            news_image = child.find_element(By.CLASS_NAME, "Image")
            news_image_src = news_image.get_attribute("src")

            # Assuming full_text contains at least two '\n', allowing for a split into three parts
            if len(full_text) < 1:
                ...
            else:
  
                news_header, news_text, new_date = full_text.split('\n', 2)
                words = news_header.split()
                # Take the first four words from the list
                first_four_words = words[:4]
                # Join these four words back into a string
                image_name = ' '.join(first_four_words)
                image_path=download_image(date_folder, news_image_src, image_name)
                # Check if the news_text contains any of the words in money_text
                is_money = False  # Initialize a flag to False
                for money in money_text:
                    if money in full_text:
                        is_money = True  # Set the flag to True if the condition is met
                        break  # Exit the loop if the condition is met
                data_news.append({
                'Title': news_header,
                'Description': news_text,
                'Date': new_date,
                'Money?': is_money,
                'Image': image_path 
                })
    close(start)

        # Convert the list of dictionaries to a DataFrame
        

        # Optional: Save the DataFrame to a CSV file
        

    for page_counter in range(2, 20):
        sub_start=star_page()
        subpage_url = f"https://apnews.com/search?q=biden&p={str(page_counter)}"
        #sub_start=start.get(subpage_url)
        webpage =open_page(sub_start, subpage_url)
        

        search_result = WebDriverWait(sub_start, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/div[3]/bsp-search-results-module/form/div[2]/div/bsp-search-filters/div/main/div[2]/bsp-list-loadmore/div[2]""")))
        sub_children_sub = search_result.find_elements(By.XPATH,"./*")
        for child in sub_children_sub:
            full_text = child.text
                            #news_image = child.find_element(By.CLASS_NAME, "Image")
            news_image=child.find_element(By.CLASS_NAME, "Image")
            news_image_src = news_image.get_attribute("src")

            # Assuming full_text contains at least two '\n', allowing for a split into three parts
            if len(full_text) < 1 and full_text.count('\n') == 1 :
                ...
            elif full_text.count('\n') < 2:
                ...
            else:
    
                news_header, news_text, new_date = full_text.split('\n', 2)
                words = news_header.split()
                # Take the first four words from the list
                first_four_words = words[:4]
                # Join these four words back into a string
                image_name = ' '.join(first_four_words)
                image_path=download_image(date_folder, news_image_src, image_name)
                # Check if the news_text contains any of the words in money_text
                is_money = False
                for money in money_text:
                    if money in full_text:
                        is_money = True
                        break
                data_news.append({
                'Title': news_header,
                'Description': news_text,
                'Date': new_date,
                'Money?': is_money,
                'Image': image_path 
                })


            for child in sub_children_sub:
                full_text = child.text

        close(sub_start)
    df = pd.DataFrame(data_news)
    df.to_csv(save_path, index=False)
    print("done")

