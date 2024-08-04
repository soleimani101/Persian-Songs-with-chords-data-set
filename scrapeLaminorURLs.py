import requests
from bs4 import BeautifulSoup
import time

def scrape_urls(base_url, max_retries=3, delay=1):
    url_list = []
    page_number = 1

    while True:
        url = base_url + str(page_number)
        success = False

        # Retry mechanism
        for attempt in range(max_retries):
            try:
                response = requests.get(url)
                if response.status_code == 404:
                    return url_list
                elif response.status_code == 200:
                    success = True
                    break
            except requests.RequestException:
                time.sleep(delay)

        if not success:
            print(f"Failed to retrieve page {page_number} after {max_retries} attempts.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        chord_info_elements = soup.find_all(class_='smh-chord-info')
        for element in chord_info_elements:
            href = element.get('href')
            if href:
                url_list.append(href)

        page_number += 1
        if(page_number == 56):
            return url_list

        print(page_number)


# Base URL for the pages
base_url = "https://laminor.org/rhythms/2-4?page="

# Scrape the URLs
extracted_urls = scrape_urls(base_url)

# Save the extracted URLs to a text file
with open('extracted_urls_24.txt', 'w') as file:
    for url in extracted_urls:
        file.write(url + '\n')

print(f"Extracted {len(extracted_urls)} URLs.")
