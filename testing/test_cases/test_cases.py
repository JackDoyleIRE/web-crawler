test_cases = [
    # Initial test case - Crawler base functionality
    {
        "name": "Base Crawler Test - Simple Crawling",
        "start_url": "http://test-webserver:8000/test_base_crawl.html",
        "expected_urls": [
            "https://example.com",
            "http://test-webserver:8000/local-page",
            "http://test-webserver:8000/local-page2"
        ],
        "clean_links": False  # Disable link cleaning for this test
    },
    # 
]

