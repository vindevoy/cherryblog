###
#
#   Full history: see below
#
#   Version: 2.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This is a split of the original application.py in the root directory, containing only the Application class
#
###

import cherrypy

from model.dataloader import DataLoader
from common.singleton import Singleton
from view.templateloader import TemplateLoader


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

    # @cherrypy.expose
    # def print_page(self, page, **_):
    #     data = DataLoader().get_page_data(page)
    #     data['url'] = '/print_page/{0}'.format(page)
    #
    #     template = TemplateLoader().get_template('print_page.html')
    #     rendered = template.render(data=data)
    #
    #     return rendered
    #
    # @cherrypy.expose
    # def print_post(self, post, **_):
    #     data = DataLoader().get_post_data(post)
    #     data['url'] = '/print_post/{0}'.format(post)
    #
    #     template = TemplateLoader().get_template('print_post.html')
    #     rendered = template.render(data=data)
    #
    #     return rendered

###
#
#   Version: 1.2.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Daemon functionality
#       - PID functionality
#       - UID and GID functionality
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Renaming categories to tags
#       - Dynamic paths to themes and data
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
