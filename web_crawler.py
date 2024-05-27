import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_banner():
    banner = r"""
             __                         __       
 _    _____ / /    ___________ __    __/ /__ ____
| |/|/ / -_) _ \  / __/ __/ _ `/ |/|/ / / -_) __/
|__,__/\__/_.__/  \__/_/  \_,_/|__,__/_/\__/_/   
                                                 
    """
    print(banner)

class WebCrawler:
    def __init__(self, seed_urls, max_depth=3, rate_limit=1, user_agent='MyCrawler', storage=None):
        self.seed_urls = seed_urls
        self.max_depth = max_depth
        self.rate_limit = rate_limit
        self.user_agent = user_agent
        self.visited_urls = set()
        self.storage = storage if storage else {}
        self.headers = {'User-Agent': self.user_agent}

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_links(self, page_content, base_url):
        soup = BeautifulSoup(page_content, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = urljoin(base_url, anchor['href'])
            if self.is_valid_url(link):
                links.add(link)
        return links

    def obey_robots_txt(self, url):
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        try:
            response = requests.get(robots_url, headers=self.headers)
            if response.status_code == 200:
                robots_txt = response.text
                disallowed_paths = re.findall(r"Disallow: (.+)", robots_txt)
                for path in disallowed_paths:
                    if url.startswith(urljoin(robots_url, path.strip())):
                        return False
        except requests.RequestException:
            pass
        return True

    def save_content(self, url, content):
        self.storage[url] = content

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def crawl(self, url, depth, domain):
        if depth > self.max_depth or url in self.visited_urls or not self.obey_robots_txt(url):
            return
        self.visited_urls.add(url)
        time.sleep(self.rate_limit)
        logger.info(f"Crawling: {url}")
        page_content = self.fetch_page(url)
        if page_content:
            self.save_content(url, page_content)
            for link in self.parse_links(page_content, url):
                if self.get_domain(link) == domain:
                    self.crawl(link, depth + 1, domain)

    def start(self):
        for seed_url in self.seed_urls:
            seed_domain = self.get_domain(seed_url)
            self.crawl(seed_url, 0, seed_domain)

    def export_results(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            for url, content in self.storage.items():
                f.write(f"URL: {url}\n\n")
                f.write(content)
                f.write('\n\n')

def main():
    print_banner()

    parser = argparse.ArgumentParser(description='A simple web crawler.')
    parser.add_argument('seed_urls', metavar='URL', type=str, nargs='+', help='Seed URLs to start crawling from')
    parser.add_argument('--max_depth', type=int, default=3, help='Maximum depth to crawl (default: 3)')
    parser.add_argument('--rate_limit', type=int, default=1, help='Time delay between requests in seconds (default: 1)')
    parser.add_argument('--user_agent', type=str, default='MyCrawler', help='User-Agent string to use (default: MyCrawler)')
    parser.add_argument('--output_file', type=str, default='output.txt', help='Output file to save the results (default: output.txt)')

    args = parser.parse_args()

    crawler = WebCrawler(
        seed_urls=args.seed_urls,
        max_depth=args.max_depth,
        rate_limit=args.rate_limit,
        user_agent=args.user_agent
    )
    crawler.start()
    crawler.export_results(args.output_file)

    print(f"Crawling finished. Results saved to: {args.output_file}")

if __name__ == "__main__":
    main()
