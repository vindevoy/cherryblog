###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

clean:
	@rm -rf ./__pycache__
	@rm -rf ./src/application/__pycache__
	@rm -rf ./tmp

setup:
	@mkdir -p ./src/application
	@mkdir -p ./src/theme/default
	@mkdir -p ./src/data/pages
	@mkdir -p ./src/data/blog
	@mkdir -p ./src/data/site
	@touch ./src/data/site/settings.yml
	@echo "[OK] Setup has created the /src directory and sub-directories"

download: clean
	@mkdir -p ./tmp
	@wget -O ./tmp/startbootstrap-blog-home.zip https://github.com/BlackrockDigital/startbootstrap-blog-home/archive/gh-pages.zip
	@wget -O ./tmp/startbootstrap-blog-post.zip https://github.com/BlackrockDigital/startbootstrap-blog-post/archive/gh-pages.zip
	@mkdir -p ./download
	@unzip -o ./tmp/startbootstrap-blog-home.zip -d ./download
	@unzip -o ./tmp/startbootstrap-blog-post.zip -d ./download
	@rm -rf ./tmp

dependencies:
	@pip3 install cherrypy
	@pip3 install jinja2
	@echo "[OK] Dependencies in Python installed"


serve:
	@python3 ./src/application/serve.py
