# Provide access to global pyobjc
VIRTUALENV_ARGS=--system-site-packages

setup:
	virtualenv ${VIRTUALENV_ARGS} .
	bin/pip install -r requirements.txt

all:
	bin/python play.py

clean:
	rm -rf bin lib include pip-*.json
