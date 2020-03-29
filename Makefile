###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

setup:
	@mkdir -p ./src/application
	@mkdir -p ./src/theme/default
	@mkdir -p ./src/data/pages
	@mkdir -p ./src/data/blog
	@echo "[OK] Setup has created the /src directory and sub-directories"

dependencies:
	@pip3 install cherrypy
	@pip3 install jinja2
	@echo "[OK] Dependencies in Python installed"

clean:
	@rm -rf ./__pycache__
	@rm -rf ./src/application/__pycache__

serve:
	@python3 ./src/application/serve.py
