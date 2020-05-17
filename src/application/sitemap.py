###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-05-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Added remapper
#
###

import logging
import os

from pathlib import Path

from common.options import Options
from common.content import Content
from controller.data_loader import DataLoader
from controller.logging_loader import LoggingLoader
from controller.remapper import Remapper
from controller.settings_loader import SettingsLoader

environment = 'localhost'
data_dir = os.path.join(os.getcwd(), 'src', 'data')

Options().environment = environment
Options().data_dir = data_dir

settings = SettingsLoader(environment).parse()

LoggingLoader().configure()

logger = logging.getLogger('SITEMAP')

logger.debug('data_dir: {0}'.format(data_dir))

Remapper().outgoing_content = DataLoader().mapping_outgoing()
Remapper().incoming_content = DataLoader().mapping_incoming()

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

    unmapped = '/posts/{0}'.format(stem)
    remapped = Remapper().remap_document(unmapped)

    logger.debug('unmapped: {0}'.format(unmapped))
    logger.debug('remapped: {0}'.format(remapped))

    logger.info('Parsing {0}'.format(file))

    meta, _, _ = Content().read_content('posts', file)

    xml += '  <url>\n'
    xml += '    <loc>https://cherryblog.org{0}</loc>\n'.format(remapped)
    xml += '    <lastmod>{0}</lastmod>\n'.format(meta['date'])
    xml += '    <changefreq>never</changefreq>\n'
    xml += '    <priority>{0}</priority>\n'.format(round(priority, 2))
    xml += '  </url>\n'

    if priority > 0.5:
        priority = round(priority - 0.1, 2)

for entry in DataLoader().pages_published:
    file = entry['file']
    stem = Path(file).stem

    unmapped = '/pages/{0}'.format(stem)
    remapped = Remapper().remap_document(unmapped)

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
    xml += '    <loc>https://cherryblog.org{0}</loc>\n'.format(remapped)
    xml += '    <lastmod>{0}</lastmod>\n'.format(meta['date'])
    xml += '    <changefreq>{0}</changefreq>\n'.format(update)
    xml += '    <priority>{0}</priority>\n'.format(round(priority, 2))
    xml += '  </url>\n'

xml += '</urlset>\n'

logger.debug('xml:\n{0}'.format(xml))

sitemap_path = os.path.join(data_dir, 'sitemap', 'sitemap.xml')
logger.info('Writing file {0}'.format(sitemap_path))

sitemap_file = open(sitemap_path, 'w')
sitemap_file.write(xml)
sitemap_file.close()

###
#
#   Version: 1.0.0
#   Date: 2020-05-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Build a sitemap
#
###
