###
#
#   Version: 1.1.0
#   Date: 2020-04-11
#   Author: Yves Vindevogel (vindevoy)
#
#   Add logging
#
###

# Clean is only for development. If you want to clean the logs in production for example,
# use the proper Linux tools

clean:
	@find . -name '__pycache__' -type d -delete
	@find . -name '*.log' -type f -delete
	@rm -rf ./tmp ./log ./download

	@echo '[OK] Cleaned'

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

	@echo '[OK] Download done'

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

	@echo '[OK] README.md created'

history:
	@python3 ./src/application/history.py

	@echo '[OK] HISTORY.md created'

	@rm -f ./src/data/pages/releases.md
	@echo '---'                                             >   ./src/data/pages/releases.md
	@echo ''                                                >>  ./src/data/pages/releases.md
	@echo 'title: "Release notes"'                          >>  ./src/data/pages/releases.md
	@echo ''                                                >>  ./src/data/pages/releases.md
	@echo 'image: "blossom4.jpg"'                           >>  ./src/data/pages/releases.md
	@echo ''                                                >>  ./src/data/pages/releases.md
	@echo 'author: "Yves Vindevogel"'                       >>  ./src/data/pages/releases.md
	@date +"date: \"%Y-%m-%d\""                             >>  ./src/data/pages/releases.md
	@echo ''                                                >>  ./src/data/pages/releases.md
	@echo '----------'                                      >>  ./src/data/pages/releases.md
	@echo ''                                                >>  ./src/data/pages/releases.md
	@cat ./HISTORY.md                                       >>  ./src/data/pages/releases.md
	@echo ''                                                >>  ./src/data/pages/releases.md

	@echo '[OK] history copied to pages'

develop:
	@mkdir -p ./log
	@python3 ./src/application/main.py 2>&1 | tee ./log/develop.log

production:
	@mkdir -p /var/log/cherryblog
	@python3 ./src/application/main.py --env production 2>&1 | tee /var/log/cherryblog/production.log &

stop:

###
#
#   Version: 1.0.1
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Cleaned some commands
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
#   Original file
#
###
