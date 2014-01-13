import logging
import logging.config

import config

from jinja2 import Environment, FileSystemLoader
# from jinja2 import Template

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


def template_formatter(template_dir, template_file, var_dict):
    """
    receives a template and returns a formatted version of it
    according to a provided variable dictionary
    """

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    lgr.debug('generating template from %s/%s with vars: %s' % (
        template_dir, template_file, var_dict))
    return(template.render(var_dict))


def make_file(dir, output_file, content):
    """
    creates a file from content
    """

    lgr.debug('creating file %s/%s with content %s' % (
        dir, output_file, content))
    with open('%s/%s' % (dir, output_file), 'w+') as f:
        f.write(content)
