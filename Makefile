test:
	pytest tests --doctest-modules pawk 

install:
	uv tool install .

.PHONY: test install
