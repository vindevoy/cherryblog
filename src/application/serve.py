###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Renaming categories to tags
#       - Dynamic paths to themes and data
#
###

import cherrypy
import getopt
import os
import sys

from dataloader import DataLoader
from optionsloader import OptionsLoader
from settingsloader import SettingsLoader
from singleton import Singleton
from templateloader import TemplateLoader


class Application(metaclass=Singleton):
    @cherrypy.expose
    def index(self, page_index=1, **_):
        data = DataLoader().get_index_data(page_index)
        data['url'] = '/index/{0}'.format(page_index)

        template = TemplateLoader().get_template('screen_index.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def pages(self, page, **_):
        # page on the URL: http://www.yoursite.ext/pages/page
        data = DataLoader().get_page_data(page)
        data['url'] = '/pages/{0}'.format(page)

        template = TemplateLoader().get_template('screen_page.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def posts(self, post, **_):
        data = DataLoader().get_post_data(post)
        data['url'] = '/posts/{0}'.format(post)

        template = TemplateLoader().get_template('screen_post.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def tags(self, tag, page_index=1, **_):
        data = DataLoader().get_tag_data(tag, page_index)
        data['url'] = '/tags/{0}/{1}'.format(tag, page_index)

        template = TemplateLoader().get_template('screen_tag.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def print_page(self, page, **_):
        data = DataLoader().get_page_data(page)
        data['url'] = '/print_page/{0}'.format(page)

        template = TemplateLoader().get_template('print_page.html')
        rendered = template.render(data=data)

        return rendered

    @cherrypy.expose
    def print_post(self, post, **_):
        data = DataLoader().get_post_data(post)
        data['url'] = '/print_post/{0}'.format(post)

        template = TemplateLoader().get_template('print_post.html')
        rendered = template.render(data=data)

        return rendered


if __name__ == '__main__':
    environment = 'localhost'
    data_dir = ""
    theme_dir = ""

    opts, args = getopt.getopt(sys.argv[1:], 'd:e:t:', ['env=', 'data=', 'theme='])

    for opt, arg in opts:
        if opt in ['-d', '--data']:
            data_dir = arg
        if opt in ['-e', '--env']:
            environment = arg
        if opt in ['-t', '--theme']:
            theme_dir = arg

    if data_dir == '':
        data_dir = os.path.join(os.getcwd(), 'src', 'data')

    if theme_dir == '':
        theme_dir = os.path.join(os.getcwd(), 'src', 'theme', 'default')

    OptionsLoader().environment = environment
    OptionsLoader().data_dir = data_dir
    OptionsLoader().theme_dir = theme_dir

    settings = SettingsLoader(environment).parse()

    cherrypy.quickstart(Application(), config=settings)

###
#
#   Version: 1.0.1
#   Date: 2020-04-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - Added **_ to each of the exposed links. Facebook sends shit on the URL when you copy paste the blog's
#         address: ?fbclid=IwAR0qgVcdKo1bgunAT5wFYolJkt3YPT8ANxFNgIiNfTiWzcv4a72j3LPujRI
#         That is now filtered away with the **_
#
#       - Added the URL to the data section so that the templates know what URL was requested.
#         This allows solving the menu items not coloured correctly
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
