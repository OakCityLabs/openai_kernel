.PHONY: test format lint

test:
	python -m openai_kernel.mock_kernel install --user
	python tests/jkt_test_kernel.py

format:
	isort --force-single-line-imports openai_kernel tests
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place openai_kernel tests --exclude=__init__.py
	black openai_kernel tests
	isort openai_kernel tests

lint:
	black openai_kernel tests --check --exclude '/build/'
	isort --check-only openai_kernel tests
	flake8 openai_kernel tests
