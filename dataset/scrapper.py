import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import re
import csv
import pandas as pd
import streamlit as st

class WebScraper:
    def __init__(self, base_url, max_depth=100000):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited_urls = set()
        self.urls_to_visit = {base_url}

    def get_urls_from_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tags = soup.find_all('a')
            urls = [a.get('href') for a in a_tags if a.get('href')]
            urls = [url for url in urls if not url.startswith('javascript:') and not url.startswith('#')]
            urls = [urljoin(url, u) for u in urls if urljoin(url, u).startswith(self.base_url)]
            file_extension_regex = re.compile(r'.*\.[a-zA-Z0-9]+$')
            urls = [u for u in urls if not file_extension_regex.match(u)]
            return urls
        except requests.RequestException as e:
            st.error(f"Failed to retrieve {url}: {e}")
            return []

    def crawl(self):

        print(self.max_depth)
        depth = 0

        my_bar = st.progress(0, text="Crawling URLs...")

        while self.urls_to_visit and depth < self.max_depth:
            current_urls = self.urls_to_visit.copy()
            self.urls_to_visit.clear()
            depth += 1
            total_urls = len(current_urls)

            for i, url in enumerate(current_urls):
                if url not in self.visited_urls:
                    st.write(f"Crawling URL: {url}")
                    self.visited_urls.add(url)
                    new_urls = self.get_urls_from_page(url)
                    self.urls_to_visit.update(new_urls)
                    my_bar.progress((i + 1) / total_urls, text=f"Crawling URL {i + 1} of {total_urls}...")
                    time.sleep(1)

        return self.visited_urls

    def extract_data_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            data = []
            for tag in soup.find_all(['h1', 'h2', 'h3']):
                heading = self.remove_unicode(tag.get_text(strip=True))
                text = []
                for sibling in tag.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3']:
                        break
                    if sibling.get_text():
                        text.append(self.clean_text(sibling.get_text()))
                if text:
                    data.append({"url": url, "heading": heading, "text": ' '.join(text)})

            return data
        except requests.RequestException as e:
            st.error(f"Failed to extract data from {url}: {e}")
            return []

    def remove_unicode(self, text):
        return re.sub(r'[^\x00-\x7F]+', '', text)

    def normalize_newlines(self, text):
        return re.sub(r'\n\n+', '\n\n', text)

    def clean_text(self, text):
        return self.normalize_newlines(self.remove_unicode(text))

    def save_data_to_csv(self, data, filename='dataset/data/output.csv'):
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def web_scraping_pipeline(self):
        all_urls = self.crawl()
        all_data = []

        for url in all_urls:
            data = self.extract_data_from_url(url)
            all_data.extend(data)

        # if all_data:
        #     self.save_data_to_csv(all_data)

        if all_data:
            df = pd.DataFrame(all_data)
            return df
        else:
            st.error("No data was collected.")

# Usage
# if __name__ == "__main__":
#     scraper = WebScraper("https://example.com", max_depth=100)
#     scraper.web_scraping_pipeline()
