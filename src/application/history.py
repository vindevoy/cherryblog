import logging
import os

from common.options import Options
from common.content import Content
from controller.logging_loader import LoggingLoader
from controller.settings_loader import SettingsLoader

environment = 'localhost'
data_dir = os.path.join(os.getcwd(), 'src', 'data')

Options().environment = environment
Options().data_dir = data_dir

settings = SettingsLoader(environment).parse()

LoggingLoader().configure()

logger = logging.getLogger('HISTORY')

output = ''

for file in sorted(os.listdir(os.path.join(os.getcwd(), 'src', 'data', 'posts')), reverse=True):
    logger.info('Parsing {0}'.format(file))

    meta, content, _ = Content().read_content('posts', file)

    if meta['tags'] is None:
        continue

    history = False
    history_tags = ['history', 'History']

    for ht in history_tags:
        if ht in meta['tags']:
            history = True

    if not history:
        continue

    output += '# {0}\n'.format((meta['title']))
    output += '\n'

    skip = True

    for line in content.splitlines():
        if not skip:
            output += '{0}\n'.format(line)

        if line.startswith('##'):
            skip = False

    output += '\n\n'

history_file = open(os.path.join(os.getcwd(), 'HISTORY.md'), 'w')
history_file.write(output)
history_file.close()
