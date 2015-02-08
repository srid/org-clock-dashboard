# Provide access to global pyobjc
VIRTUALENV_ARGS=--system-site-packages

all:
	bin/python play.py

deploy:
	bin/python setup.py py2app

setup:
	virtualenv ${VIRTUALENV_ARGS} .
	bin/pip install -r requirements.txt

clean:
	rm -rf bin lib include pip-*.json
