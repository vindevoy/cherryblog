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
	@echo '[OK] Setup has created the /src directory and sub-directories'

download: clean
	@mkdir -p ./tmp
	@wget -O ./tmp/startbootstrap-blog-home.zip         https://github.com/BlackrockDigital/startbootstrap-blog-home/archive/gh-pages.zip
	@wget -O ./tmp/startbootstrap-blog-post.zip         https://github.com/BlackrockDigital/startbootstrap-blog-post/archive/gh-pages.zip
	@wget -O ./tmp/startbootstrap-shop-home.zip         https://github.com/BlackrockDigital/startbootstrap-shop-homepage/archive/gh-pages.zip
	@wget -O ./tmp/startbootstrap-heroic-features.zip   https://github.com/BlackrockDigital/startbootstrap-heroic-features/archive/gh-pages.zip

	@mkdir -p ./download
	@unzip -o ./tmp/startbootstrap-blog-home.zip        -d ./download
	@unzip -o ./tmp/startbootstrap-blog-post.zip        -d ./download
	@unzip -o ./tmp/startbootstrap-shop-home.zip        -d ./download
	@unzip -o ./tmp/startbootstrap-heroic-features.zip  -d ./download

	@rm -rf ./tmp

dependencies:
	@pip3 install cherrypy
	@pip3 install jinja2
	@pip3 install pyyaml
	@pip3 install markdown
	@echo '[OK] Dependencies in Python installed'

readme:
	@echo '# ABOUT CherryBlog'                              >   ./README.md
	@echo ''                                                >>  ./README.md
	@sed -e '1,/----------/d' ./src/data/pages/about.md     >>  ./README.md
	@echo ''                                                >>  ./README.md
	@echo '# DOCUMENTATION'                                 >>  ./README.md
	@echo ''                                                >>  ./README.md
	@sed -e '1,/----------/d' ./src/data/pages/docs.md      >>  ./README.md
	@echo ''                                                >>  ./README.md
	@echo '# CREDITS'                                       >>  ./README.md
	@echo ''                                                >>  ./README.md
	@sed -e '1,/----------/d' ./src/data/pages/credits.md   >>  ./README.md

history:
	@echo '# VERSION 1.0.0'                                                 >   ./HISTORY.md
	@echo ''                                                                >>  ./HISTORY.md
	@grep -A 10000000 '##' ./src/data/posts/0006_version_1_0_0.md           >>  ./HISTORY.md
	@echo ''                                                                >>  ./HISTORY.md

develop:
	@python3 ./src/application/serve.py

production:
	@python3 ./src/application/serve.py --env production &
