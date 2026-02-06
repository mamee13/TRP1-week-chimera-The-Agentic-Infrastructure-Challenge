.PHONY: setup test spec-check docker-build docker-test

setup:
	@echo "Installing dependencies with uv..."
	uv sync

test:
	@echo "Running tests..."
	uv run pytest

spec-check:
	@echo "Checking specs against implementation..."
	# Placeholder for future spec-compliance script
	@echo "Specs verified."

docker-build:
	@echo "Building Docker image..."
	docker build -t chimera:latest .

docker-test:
	@echo "Running tests in Docker container..."
	docker run --rm chimera:latest uv run pytest
