import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class WebCrawler:
    def __init__(self):
        self.index = dict()
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    href = urljoin(base_url or url, href)
                    # Only crawl links within the same domain
                    if urlparse(href).netloc == urlparse(base_url or url).netloc:
                        self.crawl(href, base_url=base_url or url)
                    if not href.startswith(base_url or url):
                        self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower():
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")


