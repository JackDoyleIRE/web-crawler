import sys
import yaml
import asyncio  
from typing import List, Optional, Union
from crawler.crawler import Crawler
from crawler.crawler_utils import Logger

class CLI:
    ''' Command line interface to interact with the web crawler'''
    def __init__(self) -> None:
        self.logger: Logger = Logger(level='ALL')  # Default log level is All
        self.crawler: Crawler = Crawler(logger=self.logger)  # Initialize Crawler with the default logger

    def show_menu(self) -> None:
        '''Command line interface menu'''
        print("-" * 40)
        print("Welcome to the Web Crawler CLI!")
        print("-" * 40)
        # Display current logging configuration
        log_to_file_status = "Yes" if self.logger.log_to_file else "No"
        print(f"Current Logger Configuration: [Level: {self.logger.log_level}, Logging to File: {log_to_file_status}]")
        print("-" * 40)
        print("1. Configure Logger")
        print("2. Start Crawling")
        print("3. Exit")
        print("-" * 40)

    def load_urls_from_config(self, config_file: str = 'crawler/crawler-config.yml') -> List[str]:
        """Load URLs from the given YAML configuration file."""
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config.get('urls', [])
        except Exception as e:
            self.logger.log_error(f"Failed to load configuration file: {e}")
            return []

    def configure_logger(self) -> None:
        """Configure the logger settings based on user input."""
        log_level: str = input("Enter log level (ERROR, WARNING, INFO, SUCCESS, ALL): ").strip().upper()
        log_to_file: str = input("Do you want to log to a file? (yes/no): ").strip().lower()
        
        if log_to_file == 'yes':
            filename: str = input("Enter the filename for logs (default: 'crawler.log'): ").strip() or 'crawler.log'
            self.logger = Logger(level=log_level, log_to_file=True, filename=filename)
        else:
            self.logger = Logger(level=log_level)

        self.crawler = Crawler(logger=self.logger)  # Update the crawler with the new logger config

    async def start_crawling(self) -> None:
        """Handle the crawling process asynchronously."""
        urls: List[str] = self.load_urls_from_config()

        if urls:
            self.logger.log_info("Available URLs from config:")
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")
            print("0. Enter a new URL")

            selected_option: int = int(input("Select a URL by number (0 to enter new URL): "))

            if selected_option == 0:
                start_url: str = input("Enter the URL to start crawling: ")
            else:
                start_url: str = urls[selected_option - 1]
        else:
            start_url: str = input("Enter the URL to start crawling: ")

        max_depth: int = int(input("Enter the maximum depth: "))

        # Await the asynchronous crawl method
        result_links: set[str] = await self.crawler.crawl(start_url, max_depth)
        
        # Display the result and clarify the status
        if result_links:
            self.logger.log_success(f"Crawling completed successfully. Total links found: {len(result_links)}")
            self.logger.log_info("Cleaned Links:")
            for link in result_links:
                print(link)
        else:
            self.logger.log_error("No links found during the crawl.")
        
        # Confirm if logs were written to a file
        if self.logger.log_to_file:
            print(f"Logs have been written to {self.logger.filename}.")

    def start(self) -> None:
        """Starts the CLI for user interaction."""
        while True:
            self.show_menu()  # Show the menu at the start of each iteration
            choice: str = input("Choose an option: ")

            if choice == '1':
                self.configure_logger()  # Configure logger when option 1 is selected
            elif choice == '2':
                # Use asyncio.run() to handle the async crawling method
                asyncio.run(self.start_crawling())
            elif choice == '3':
                self.logger.log_warning("Exiting... Goodbye!") if self.logger else print("Exiting... Goodbye!")
                if self.logger and self.logger.file:  # Close the log file if it was opened
                    self.logger.close()
                sys.exit()
            else:
                self.logger.log_error("Invalid option. Please try again.") if self.logger else print("Invalid option. Please try again.")
