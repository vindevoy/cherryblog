###
#
#   Full history: see below
#
#   Version: 2.5.0
#   Date: 2020-05-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Remapping of URLs to documents
#
###

import cherrypy
import logging

from datetime import datetime
from htmlmin.minify import html_minify

from common.options import Options
from common.singleton import Singleton
from controller.data_loader import DataLoader
from controller.page_cacher import PageCacher
from controller.remapper import Remapper
from view.templateloader import TemplateLoader


class Application(metaclass=Singleton):
    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('APPLICATION')
        self.__logger.setLevel(Options().default_logging_level)

    @cherrypy.expose
    def index(self, page_index=1, **_):
        start = datetime.now()

        request = '/index/{0}'.format(page_index)

        if Options().caching and PageCacher().cached_already(request):
            minified = PageCacher().get_cached(request)

        else:
            data = DataLoader().index_data(page_index)
            data['url'] = request

            template = TemplateLoader().get_template('screen_index.html')
            rendered = template.render(data=data)
            minified = html_minify(rendered)

            if Options().caching:
                PageCacher().cache(request, minified)

        finished = datetime.now()
        self.__logger.info('{0} {1}'.format(request, finished - start))

        return minified

    @cherrypy.expose
    def pages(self, page, **_):
        start = datetime.now()

        request = '/pages/{0}'.format(page)
        self.__logger.debug('pages - request: {0}'.format(request))

        if Options().caching and PageCacher().cached_already(request):
            minified = PageCacher().get_cached(request)

        else:
            remapped = Remapper().remap_url(request)
            self.__logger.debug('pages - remapped: {0}'.format(remapped))

            if request != remapped:
                page = remapped.split('/')[2]
                self.__logger.debug('pages - page: {0}'.format(page))

            # page on the URL: http://www.yoursite.ext/pages/page
            data = DataLoader().pages_data(page)
            data['url'] = remapped

            template = TemplateLoader().get_template('screen_page.html')
            rendered = template.render(data=data)
            minified = html_minify(rendered)

            if Options().caching:
                PageCacher().cache(request, minified)

        finished = datetime.now()
        self.__logger.info('{0} {1}'.format(request, finished - start))

        return minified

    @cherrypy.expose
    def posts(self, post, **_):
        start = datetime.now()

        request = '/posts/{0}'.format(post)
        self.__logger.debug('posts - request: {0}'.format(request))

        if Options().caching and PageCacher().cached_already(request):
            minified = PageCacher().get_cached(request)

        else:
            remapped = Remapper().remap_url(request)
            self.__logger.debug('posts - remapped: {0}'.format(remapped))

            if request != remapped:
                post = remapped.split('/')[2]
                self.__logger.debug('posts - post: {0}'.format(post))

            data = DataLoader().posts_data(post)
            data['url'] = remapped

            template = TemplateLoader().get_template('screen_post.html')
            rendered = template.render(data=data)
            minified = html_minify(rendered)

            if Options().caching:
                PageCacher().cache(request, minified)

        finished = datetime.now()
        self.__logger.info('{0} {1}'.format(request, finished - start))

        return minified

    @cherrypy.expose
    def tags(self, tag, page_index=1, **_):
        start = datetime.now()

        request = '/tags/{0}/{1}'.format(tag, page_index)
        self.__logger.debug('tags - tag: {0}'.format(tag))

        if Options().caching and PageCacher().cached_already(request):
            minified = PageCacher().get_cached(request)

        else:
            short_request = 'tags/{0}'.format(tag)
            self.__logger.debug('tags - short_request: {0}'.format(short_request))

            remapped = Remapper().remap_url(short_request)
            self.__logger.debug('tags - remapped: {0}'.format(remapped))

            if short_request != remapped:
                tag = remapped.split('/')[2]
                self.__logger.debug('tags - tag: {0}'.format(tag))

            data = DataLoader().tags_data(tag, page_index)
            data['url'] = remapped

            template = TemplateLoader().get_template('screen_tag.html')
            rendered = template.render(data=data)
            minified = html_minify(rendered)

            if Options().caching:
                PageCacher().cache(request, minified)

        finished = datetime.now()
        self.__logger.info('{0} {1}'.format(request, finished - start))

        return minified

    @cherrypy.expose
    def search(self, query='', page_index=1, **_):
        start = datetime.now()

        request = '/search/{0}/{1}'.format(query, page_index)

        data = DataLoader().search_data(query, page_index)
        data['url'] = request

        template = TemplateLoader().get_template('screen_search.html')
        rendered = template.render(data=data)
        minified = html_minify(rendered)

        finished = datetime.now()
        self.__logger.info('{0} {1}'.format(request, finished - start))

        return minified

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
#   Version: 2.4.0
#   Date: 2020-05-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Using HTML minify
#
#   Version: 2.3.0
#   Date: 2020-04-26
#   Author: Yves Vindevogel (vindevoy)
#
#   Caching enabled or not
#
#   Version: 2.2.0
#   Date: 2020-04-22
#   Author: Yves Vindevogel (vindevoy)
#
#   Added page caching
#
#   Version: 2.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Added logging of the requests for performance insights
#
#   Version: 2.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This is a split of the original application.py in the root directory, containing only the Application class
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
