import requests
from urllib.parse import urljoin, urlparse
from collections import deque
from bs4 import BeautifulSoup
from crawler.crawler_utils import Logger  
from crawler.crawler_utils import Utils


class Crawler:
    def __init__(self, logger=None):
        self.visited = set()
        self.queue = deque()
        self.logger = logger if logger else Logger(level='INFO')  # Default log level

    def is_valid(self, url):
        """
        Checks if a URL is valid and properly formatted.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def log(self, message, level='info'):
        """ Centralized logging method. """
        if level.lower() == 'error':
            self.logger.log_error(message)
        elif level.lower() == 'warning':
            self.logger.log_warning(message)
        elif level.lower() == 'success':
            self.logger.log_success(message)
        elif level.lower() == 'info':
            self.logger.log_info(message)

    def get_all_links(self, url):
        """
        Returns all the links (URLs) found on the page.
        
        Args:
        - url: The URL of the page to fetch.

        Returns:
        - A set of URLs found on the page.
        """
        links = set()  # Set to hold found links
        try:
            self.log(f"Attempting to fetch: {url}", level='info')
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                self.log(f"Received response for {url} with status code: {response.status_code}", level='success')
            else:
                self.log(f"Received response for {url} with status code: {response.status_code}", level='warning')
                return links

            # Parse HTML content to extract links
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(url, href)  # Convert relative URLs to absolute
                if self.is_valid(full_url):
                    self.log(f"Found valid link: {full_url}", level='success')
                    links.add(full_url)  # Add valid links to the set
        except requests.RequestException as e:
            self.log(f"Error fetching {url}: {e}", level='error')

        return links

    def crawl(self, start_url, max_depth=2, clean_links=False):
        """
        Crawl from the start_url to a maximum depth, storing links in a queue.
        """
        self.queue.append((start_url, 0))

        while self.queue:
            current_url, depth = self.queue.popleft()

            if depth > max_depth:
                continue  

            if current_url not in self.visited:
                self.logger.log_header(f"Crawling: {current_url} at depth {depth}")
                self.visited.add(current_url)

                # Get all links on the current page
                links = self.get_all_links(current_url)
                for link in links:
                    if link not in self.visited:
                        self.queue.append((link, depth + 1))  # Add to the queue with depth + 1

        # Clean and return unique links after the crawl is complete
        if clean_links:
            cleaned_links = Utils.clean_links(self.visited, start_url)
            self.logger.log_success(f"Cleaned unique URLs: {cleaned_links}")
            return cleaned_links

        self.logger.log_success(f"Visited URLs: {self.visited}")
        return self.visited