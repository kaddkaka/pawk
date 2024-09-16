test:
	pytest tests --doctest-modules prawk

install:
	uv tool install .

.PHONY: test install
