###
#
#   Version: 1.2.1
#   Date: 2020-04-25
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - all logging is now in application.log instead of ENVIRONMENT.log (settings determine it for the run)
#       - better history generation
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

update:
	@git pull origin

	@echo '[OK] Update done'

install-certbot:
	@wget https://dl.eff.org/certbot-auto -P /tmp
	@mv /tmp/certbot-auto /usr/local/bin/certbot-auto
	@chown root:root /usr/local/bin/certbot-auto
	@chmod 755 /usr/local/bin/certbot-auto

install-certificate:
	@/usr/local/bin/certbot-auto certonly --standalone

update-certificate:
	@echo "0 0,12 * * * root python3 -c 'import random; import time; time.sleep(random.random() * 3600)' && /usr/local/bin/certbot-auto renew -q" | tee -a /etc/crontab > /dev/null

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
	@python3 ./src/application/main.py 2>&1 | tee ./log/application.log

production:
	@mkdir -p /var/log/cherryblog
	@python3 ./src/application/main.py --env production 2>&1 | tee /var/log/cherryblog/application.log &

stop:
	@cat ./log/cherryblog.pid | xargs kill


###
#
#   Version: 1.2.0
#   Date: 2020-04-11
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - stop command
#       - better history generation
#
#   Version: 1.1.0
#   Date: 2020-04-11
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Add logging
#
#   Version: 1.0.1
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Cleaned some commands
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
#   Original file
#
###
