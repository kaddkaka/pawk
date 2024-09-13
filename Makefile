test:
	pytest --doctest-modules main.py tests.py util.py

install:
	uv tool install .

.PHONY: test install
