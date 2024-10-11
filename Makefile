# Define variables
DOCKER_COMPOSE=docker-compose
DOCKER_COMPOSE_DOWN=$(DOCKER_COMPOSE) down --volumes
DOCKER_COMPOSE_REMOVE=$(DOCKER_COMPOSE) rm -f  # Force remove containers
DOCKER_COMPOSE_BUILD=$(DOCKER_COMPOSE) build
DOCKER_COMPOSE_EXEC=$(DOCKER_COMPOSE) exec

# Command to start the web server, reusing if already running
START_SERVER_COMMAND=$(DOCKER_COMPOSE) up -d test-webserver
RUN_TESTS_COMMAND=$(DOCKER_COMPOSE) run test-runner
START_COMMAND=$(DOCKER_COMPOSE) run crawler python main.py --start
DOCKER_CONTAINER_NAME=test-webserver  # For reusing test-webserver container

# Command to check if the web server is already running
CHECK_RUNNING_COMMAND=$(DOCKER_COMPOSE) ps | grep $(DOCKER_CONTAINER_NAME)

# Default target
.PHONY: all
all: build

# Build the Docker containers (crawler and webserver)
.PHONY: build
build:
	@echo "Building Docker containers..."
	$(DOCKER_COMPOSE_BUILD)

# Start the CLI (crawler)
.PHONY: start-cli
start-cli:
	$(START_COMMAND)

# Clean up the project (removing containers)
.PHONY: clean
clean:
	@echo "Cleaning up Docker containers and volumes..."
	$(DOCKER_COMPOSE_DOWN)  # Bring down and remove volumes
	@echo "Removing any stopped containers..."
	$(DOCKER_COMPOSE_REMOVE)  # Remove any stopped containers

# Stop the Docker containers (without removing them)
.PHONY: stop
stop:
	@echo "Stopping Docker containers..."
	$(DOCKER_COMPOSE_DOWN)

# Start the test web server, reusing the container if already running
.PHONY: test-server
test-server:
	@echo "Checking if $(DOCKER_CONTAINER_NAME) is already running..."
	@if $(CHECK_RUNNING_COMMAND); then \
	    echo "$(DOCKER_CONTAINER_NAME) is already running."; \
	else \
	    echo "Starting the server..."; \
	    $(START_SERVER_COMMAND); \
	fi

# Run the tests (after ensuring the server is running)
.PHONY: test
test: test-server
	@echo "Running tests..."
	$(RUN_TESTS_COMMAND)



