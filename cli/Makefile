.PHONY: help install dev test lint format build upload clean

help:
	@echo "Available commands:"
	@echo "  install     Install package in development mode"
	@echo "  dev         Install development dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  build       Build package"
	@echo "  upload      Upload to PyPI"
	@echo "  clean       Clean build artifacts"

install:
	pip install -e .

dev:
	pip install -e .[dev]

test:
	pytest tests/

lint:
	flake8 chan_downloader/
	mypy chan_downloader/

format:
	black chan_downloader/

build:
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
