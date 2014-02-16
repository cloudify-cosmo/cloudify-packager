import logging
import logging.config

import config
# import os
# run_env = os.environ['RUN_ENV']
# config = __import__(run_env)

import sys
from jinja2 import Environment, FileSystemLoader
# from jinja2 import Template

try:
    logging.config.dictConfig(config.PACKAGER_LOGGER)
    lgr = logging.getLogger('packager')
except ValueError:
    sys.exit('could not initiate logger. try sudo...')


def template_formatter(template_dir, template_file, var_dict):
    """
    receives a template and returns a formatted version of it
    according to a provided variable dictionary
    """

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    lgr.debug('generating template from %s/%s with package vars' % (
        template_dir, template_file))
    return(template.render(var_dict))


def make_file(output_file, content):
    """
    creates a file from content
    """

    lgr.debug('creating file: \n%s \nwith content: \n%s' % (
        output_file, content))
    with open('%s' % output_file, 'w+') as f:
        f.write(content)
