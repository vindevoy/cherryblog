###
#
#   Version: 1.0.1
#   Date: 2020-04-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Full history: see below
#
#   Fixes:
#       - Added **_ to each of the exposed links. Facebook sends shit on the URL when you copy paste the blog's
#         address: ?fbclid=IwAR0qgVcdKo1bgunAT5wFYolJkt3YPT8ANxFNgIiNfTiWzcv4a72j3LPujRI
#         That is now filtered away with the **_
#
#       - Added the URL to the data section so that the templates know what URL was requested.
#         This allows solving the menu items not coloured correctly
#
###

import cherrypy
import getopt
import sys

from dataloader import DataLoader
from settingsloader import SettingsLoader
from singleton import Singleton
from templateloader import TemplateLoader


class Application(metaclass=Singleton):
    @cherrypy.expose
    def index(self, page_index=1, **_):
        data = DataLoader().get_index_data(page_index)
        data['url'] = '/index/{0}'.format(page_index)

        template = TemplateLoader('src/theme/default').get_template('screen_index.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def pages(self, page, **_):
        # page on the URL: http://www.yoursite.ext/pages/page
        data = DataLoader().get_page_data(page)
        data['url'] = '/pages/{0}'.format(page)

        template = TemplateLoader('src/theme/default').get_template('screen_page.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def posts(self, post, **_):
        data = DataLoader().get_post_data(post)
        data['url'] = '/posts/{0}'.format(post)

        template = TemplateLoader('src/theme/default').get_template('screen_post.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def categories(self, category, page_index=1, **_):
        data = DataLoader().get_category_data(category, page_index)
        data['url'] = '/categories/{0}/{1}'.format(category, page_index)

        template = TemplateLoader('src/theme/default').get_template('screen_category.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def print_page(self, page, **_):
        data = DataLoader().get_page_data(page)
        data['url'] = '/print_page/{0}'.format(page)

        template = TemplateLoader('src/theme/default').get_template('print_page.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def print_post(self, post, **_):
        data = DataLoader().get_post_data(post)
        data['url'] = '/print_post/{0}'.format(post)

        template = TemplateLoader('src/theme/default').get_template('print_post.html')
        rendered = template.render(data=data)

        return rendered


if __name__ == '__main__':
    environment = 'localhost'

    opts, args = getopt.getopt(sys.argv[1:], "e:", ["env="])

    for opt, arg in opts:
        if opt in ['-e', '--env']:
            environment = arg

    settings = SettingsLoader(environment).parse()

    cherrypy.quickstart(Application(), config=settings)

###
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original version
#
###
