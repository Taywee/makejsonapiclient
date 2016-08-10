.PHONY: all

all:
	PYTHONPATH="$(shell pwd)" ./setup.py bdist_wheel
