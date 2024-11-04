import os
import socket
from datetime import datetime
from typing import Optional, Literal

class Logger:
    class Colors:
        HEADER: str = '\033[95m'
        OKBLUE: str = '\033[94m'
        OKGREEN: str = '\033[92m'
        WARNING: str = '\033[93m'
        FAIL: str = '\033[91m'
        ENDC: str = '\033[0m'
        BOLD: str = '\033[1m'
        UNDERLINE: str = '\033[4m'

    LOG_LEVELS: dict[str, int] = {
        'ERROR': 0,
        'WARNING': 1,
        'INFO': 2,
        'SUCCESS': 3,
        'ALL': 4
    }

    def __init__(self, level: str = 'ERROR', log_to_file: bool = False, filename: str = 'crawler.log'):
        # Capture machine/host and environment details
        self.hostname: str = socket.gethostname()
        self.environment: str = os.getenv("ENVIRONMENT", "development")  # Default to 'development'
        self.log_level: int = self.LOG_LEVELS.get(level, 0)  # Default to ERROR if level not found
        self.log_to_file: bool = log_to_file
        self.filename: str = filename
        self.file: Optional[os.TextIOWrapper] = None

        if self.log_to_file:
            self.file = open(self.filename, 'a')

    def _get_timestamp(self) -> str:
        """Returns the current time formatted as a string."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _log(self, message: str, color: str, level_name: Literal['ERROR', 'WARNING', 'INFO', 'SUCCESS']) -> None:
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

    def log_header(self, message: str) -> None:
        self.log_info(message)  # Use log_info for headers

    def log_info(self, message: str) -> None:
        self._log(message, self.Colors.OKBLUE, 'INFO')

    def log_success(self, message: str) -> None:
        self._log(message, self.Colors.OKGREEN, 'SUCCESS')

    def log_warning(self, message: str) -> None:
        self._log(message, self.Colors.WARNING, 'WARNING')

    def log_error(self, message: str) -> None:
        self._log(message, self.Colors.FAIL, 'ERROR')

    def close(self) -> None:
        """Close the log file if opened."""
        if self.file:
            self.file.close()
