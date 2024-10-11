import unittest
from crawler.crawler import Crawler  
from test_cases.test_cases import test_cases

class TestCrawler(unittest.TestCase):
    
    def run_crawl_test(self, case):
        """
        Helper function to run the actual crawling test based on the case parameters.
        """
        start_url = case["start_url"]
        expected_urls = case["expected_urls"]
        clean_links = case.get("clean_links", False)  # Get clean_links flag, default to False if not provided

        # Create an instance of the Crawler
        crawler = Crawler()

        # Crawl the site and get visited URLs, using the clean_links flag from the test case
        visited_urls = crawler.crawl(start_url, max_depth=1, clean_links=clean_links)

        # If clean_links is True, ensure the visited URLs exactly match expected URLs
        if clean_links:
            self.assertCountEqual(
                visited_urls,
                expected_urls,
                msg=f"Failed: Visited URLs {visited_urls} did not match expected clean URLs {expected_urls}"
            )
        else:
            # When clean_links=False, check if all expected URLs are in the visited URLs
            for url in expected_urls:
                with self.subTest(url=url):
                    self.assertIn(
                        url,
                        visited_urls,
                        msg=f"Failed: Expected URL {url} not found in visited URLs {visited_urls}"
                    )
    
    # Generate individual test methods for each test case
    def test_base_crawler(self):
        """
        Run the Base Crawler Test.
        """
        case = next(c for c in test_cases if c["name"] == "Base Crawler Test - Simple Crawling")
        self.run_crawl_test(case)
    
    def test_link_cleaning(self):
        """
        Run the Link Cleaning Test.
        """
        case = next(c for c in test_cases if c["name"] == "Link Cleaning Test - Duplicate Links")
        self.run_crawl_test(case)

if __name__ == "__main__":
    unittest.main()
