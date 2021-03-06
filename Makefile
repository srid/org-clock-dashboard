# Provide access to global pyobjc
VIRTUALENV_ARGS=--system-site-packages

all:
	/usr/bin/python orgclock.py

deploy:
	/usr/bin/python setup.py py2app
	rm -rf ~/Applications/orgclock.app
	mv dist/orgclock.app ~/Applications/orgclock.app

run:
	open -a orgclock

# XXX: We can't use virtualenv due to https://github.com/jaredks/rumps/issues/9
# Ensure that pip is installed globally.
setup:
	sudo /usr/bin/python -m pip install -r requirements.txt

clean:
	rm -rf bin lib include pip-*.json
