# Web Crawler

## Overview

The Web Crawler is a simple command-line application that allows users to crawl web pages and collect links. The application supports depth-limited crawling, a command-line interface (CLI) for user interaction, and configurable options through a YAML file.

## Features

- **Crawling Capabilities**: Crawl from a specified starting URL and collect all valid links.
- **Depth Control**: Limit the depth of crawling to avoid overly deep traversals.
- **Command-Line Interface**: Interactive CLI that allows users to start crawling or exit the application.
- **Configuration Management**: Ability to read starting URLs from a YAML configuration file.
- **Test Suite**: Robust unit tests to ensure the functionality of the crawler as well as additonal functionality.

## Project Arcitechture

See below a basic diagram of the arcitecture of the project

## Repository structure



## Installation

1. **Set up Docker**: Ensure you have Docker installed and running on your machine.

3. **Build the Docker image**:
The project uses a Makefile with the following commands:

make build - Builds the docker image

make start-cli - Starts the cli which provides interaction with the crawler

make test-server - Runs the test server which serves test web pages to local host

make test - Runs the test crawler on local host and evaluates unit tests

make clean - Runs docker-compose down and cleans volumes

4. **Run the application**:

See above

## Configuration

The application uses a YAML configuration file called `crawler-config.yml`. This file allows users to define starting URLs for crawling. 

### Example `crawler-config.yml`

```yaml
urls:
  - http://test-webserver:8000/test_site_1.html
  - http://example.com 
  ```

### Testing

Test cases can be added to /testing/test_cases.py

### Limitations and ideas for future development

Git ops and deployment

Linting and precommit

Deployment of image to registry

Run on kubernetes
