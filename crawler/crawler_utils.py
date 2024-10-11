import os
import socket
from datetime import datetime
from urllib.parse import urlparse, urljoin

class Logger:
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    LOG_LEVELS = {
        'ERROR': 0,
        'WARNING': 1,
        'INFO': 2,
        'SUCCESS': 3,
        'ALL': 4
    }

    def __init__(self, level='ERROR', log_to_file=False, filename='crawler.log'):
        # Capture machine/host and environment details
        self.hostname = socket.gethostname()
        self.environment = os.getenv("ENVIRONMENT", "development")  # Default to 'development'
        self.log_level = self.LOG_LEVELS.get(level, 0)  # Default to ERROR if level not found
        self.log_to_file = log_to_file
        self.filename = filename
        self.file = None

        if self.log_to_file:
            self.file = open(self.filename, 'a')

    def _get_timestamp(self):
        """Returns the current time formatted as a string."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _log(self, message, color, level_name):
        """ Helper method to print messages with spacing, timestamp, and machine/environment info. """
        if self.LOG_LEVELS[level_name] <= self.log_level:
            timestamp = self._get_timestamp()
            formatted_message = f"{timestamp} | {self.environment} | {self.hostname} | {color}{message}{self.Colors.ENDC}"
            print(formatted_message)

            if self.log_to_file:
                # Write to file and flush immediately after each log entry
                with open(self.filename, 'a') as file:
                    file.write(f"{timestamp} | {self.environment} | {self.hostname} | {message}\n")
                    file.flush()  # Ensure the data is written to disk immediately

    def log_header(self, message):
        self.log_info(message)  # Use log_info for headers

    def log_info(self, message):
        self._log(message, self.Colors.OKBLUE, 'INFO')

    def log_success(self, message):
        self._log(message, self.Colors.OKGREEN, 'SUCCESS')

    def log_warning(self, message):
        self._log(message, self.Colors.WARNING, 'WARNING')

    def log_error(self, message):
        self._log(message, self.Colors.FAIL, 'ERROR')

    def close(self):
        """Close the log file if opened."""
        if self.file:
            self.file.close()

class Utils:
    @staticmethod
    def clean_links(links, base_url):
        """
        Cleans and filters out duplicate links by normalizing them.
        
        Args:
        - links: Set of URLs to clean.
        - base_url: The base URL to resolve relative links.

        Returns:
        - A set of unique and cleaned URLs.
        """
        cleaned_links = set()
        for link in links:
            # Convert relative links to absolute using the base URL
            full_url = urljoin(base_url, link)

            # Parse and normalize the URL (remove fragments)
            parsed_url = urlparse(full_url)

            # Rebuild the URL without the fragment (#)
            normalized_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

            # Add the normalized URL to the cleaned_links set
            cleaned_links.add(normalized_url)

        return cleaned_links