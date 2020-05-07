###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-05-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Build a sitemap
#
###

import logging
import os

from pathlib import Path

from common.options import Options
from common.content import Content
from controller.data_loader import DataLoader
from controller.logging_loader import LoggingLoader
from controller.settings_loader import SettingsLoader

environment = 'localhost'
data_dir = os.path.join(os.getcwd(), 'src', 'data')

Options().environment = environment
Options().data_dir = data_dir

settings = SettingsLoader(environment).parse()

LoggingLoader().configure()

logger = logging.getLogger('SITEMAP')

# Override the drafts because Google will never find them in production most likely
Options().include_drafts = False

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

priority = 1.0

page_priorities = {'about': {'priority': 1.0, 'update': 'monthly'},
                   'documentation': {'priority': 0.9, 'update': 'monthly'},
                   'credits': {'priority': 0.1, 'update': 'yearly'}
                   }

for entry in DataLoader().posts_published:
    file = entry['file']
    stem = Path(file).stem

    logger.info('Parsing {0}'.format(file))

    meta, _, _ = Content().read_content('posts', file)

    xml += '  <url>\n'
    xml += '    <loc>https://cherryblog.org/posts/{0}</loc>\n'.format(stem)
    xml += '    <lastmod>{0}</lastmod>\n'.format(meta['date'])
    xml += '    <changefreq>never</changefreq>\n'
    xml += '    <priority>{0}</priority>\n'.format(round(priority, 2))
    xml += '  </url>\n'

    if priority > 0.5:
        priority = round(priority - 0.1, 2)

for entry in DataLoader().pages_published:
    file = entry['file']
    stem = Path(file).stem

    logger.info('Parsing {0}'.format(file))

    meta, _, _ = Content().read_content('pages', file)

    try:
        priority = page_priorities[stem]['priority']
    except KeyError:
        priority = 0.5

    try:
        update = page_priorities[stem]['update']
    except KeyError:
        update = 'monthly'

    xml += '  <url>\n'
    xml += '    <loc>https://cherryblog.org/pages/{0}</loc>\n'.format(stem)
    xml += '    <lastmod>{0}</lastmod>\n'.format(meta['date'])
    xml += '    <changefreq>{0}</changefreq>\n'.format(update)
    xml += '    <priority>{0}</priority>\n'.format(round(priority, 2))
    xml += '  </url>\n'

xml += '</urlset>\n'


sitemap_file = open(os.path.join(data_dir, 'sitemap', 'sitemap.xml'), 'w')
sitemap_file.write(xml)
sitemap_file.close()
