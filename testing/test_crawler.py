import unittest
import asyncio
from typing import Dict, Any
from crawler.crawler import Crawler  
from test_cases.test_cases import test_cases

class TestCrawler(unittest.IsolatedAsyncioTestCase):  # Updated to IsolatedAsyncioTestCase for async support
    
    async def run_crawl_test(self, case: Dict[str, Any]) -> None:
        """
        Helper function to run the actual crawling test based on the case parameters.
        """
        start_url: str = case["start_url"]
        expected_urls: list[str] = case["expected_urls"]

        # Create an instance of the Crawler
        crawler = Crawler()

        # Crawl the site and get visited URLs asynchronously
        visited_urls: set[str] = await crawler.crawl(start_url, max_depth=1)

        for url in expected_urls:
             with self.subTest(url=url):
                 self.assertIn(
                    url,
                    visited_urls,
                    msg=f"Failed: Expected URL {url} not found in visited URLs {visited_urls}"
                 )
    
    # Generate individual test methods for each test case
    async def test_base_crawler(self) -> None:
        """
        Run the Base Crawler Test.
        """
        case: Dict[str, Any] = next(c for c in test_cases if c["name"] == "Base Crawler Test - Simple Crawling")
        await self.run_crawl_test(case)  # Await the asynchronous test


if __name__ == "__main__":
    unittest.main()


