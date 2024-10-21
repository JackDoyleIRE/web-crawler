import asyncio
import aiohttp
import time
from urllib.parse import urljoin, urlparse
from collections import deque
from bs4 import BeautifulSoup
from crawler.crawler_utils import Logger 
from crawler.crawler_utils import RateLimiter
from typing import Optional, Set, Tuple, List

class Crawler:
    '''Craler class with main methods for getting links and travering found links'''
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self.visited: Set[str] = set()
        self.queue: deque[Tuple[str, int]] = deque()
        self.logger: Logger = logger if logger else Logger(level='INFO')  # Default log level

    def is_valid(self, url: str) -> bool:
        """
        Checks if a URL is valid and properly formatted.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def log(self, message: str, level: str = 'info') -> None:
        """ Centralized logging method. """
        if level.lower() == 'error':
            self.logger.log_error(message)
        elif level.lower() == 'warning':
            self.logger.log_warning(message)
        elif level.lower() == 'success':
            self.logger.log_success(message)
        elif level.lower() == 'info':
            self.logger.log_info(message)

    async def get_all_links(self, session: aiohttp.ClientSession, url: str) -> Set[str]:
        """
        Asynchronously fetches the content of the page and extracts all links.
        
        Args:
        - session: The aiohttp session.
        - url: The URL of the page to fetch.

        Returns:
        - A set of URLs found on the page.
        """
        links: Set[str] = set()  # Set to hold found links
        try:
            self.log(f"Attempting to fetch: {url}", level='info')
            client = RateLimiter(client)
            async with client.get(url, timeout=10) as response:
                if response.status == 200:
                    self.log(f"Received response for {url} with status code: {response.status}", level='success')
                    html_content = await response.text()
                else:
                    self.log(f"Received response for {url} with status code: {response.status}", level='warning')
                    return links

            # Parse HTML content to extract links
            soup = BeautifulSoup(html_content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(url, href)  # Convert relative URLs to absolute
                if self.is_valid(full_url):
                    self.log(f"Found valid link: {full_url}", level='success')
                    links.add(full_url)  # Add valid links to the set
        except aiohttp.ClientError as e:
            self.log(f"Error fetching {url}: {e}", level='error')

        return links

    async def crawl(self, start_url: str, max_depth: int = 2) -> Set[str]:
        """
        Crawl from the start_url to a maximum depth, storing links in a queue.
        """
        self.queue.append((start_url, 0))

        async with aiohttp.ClientSession() as session:
            while self.queue:
                tasks: List[asyncio.Future] = []  # List of tasks for concurrent fetching
                for _ in range(len(self.queue)):
                    current_url, depth = self.queue.popleft()

                    if depth > max_depth:
                        continue  

                    if current_url not in self.visited:
                        self.logger.log_header(f"Crawling: {current_url} at depth {depth}")
                        self.visited.add(current_url)
                        # Add the task to fetch links asynchronously
                        tasks.append(self.get_all_links(session, current_url))

                # Wait for all tasks to complete
                results = await asyncio.gather(*tasks)

                # Process the results and add new URLs to the queue
                for links in results:
                    for link in links:
                        if link not in self.visited:
                            self.queue.append((link, depth + 1))  # Add to the queue with depth + 1

        self.logger.log_success(f"Visited URLs: {self.visited}")
        return self.visited

