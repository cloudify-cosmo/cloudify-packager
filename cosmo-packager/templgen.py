import logging
import logging.config

import config

from fabric.api import *
from jinja2 import Environment, FileSystemLoader
from jinja2 import Template

logging.config.dictConfig(config.PACKAGER_LOGGER)
lgr = logging.getLogger('packager')


# @task
# def template_formatter2():
# 	# Load the jinja library's namespace into the current module.
# 	import jinja2

# 	# In this case, we will load templates off the filesystem.
# 	# This means we must construct a FileSystemLoader object.
# 	# 
# 	# The search path can be used to make finding templates by
# 	#   relative paths much easier.  In this case, we are using
# 	#   absolute paths and thus set it to the filesystem root.
# 	templateLoader = jinja2.FileSystemLoader( searchpath="/cosmo-packager/cosmo-packager/package-templates" )

# 	# An environment provides the data necessary to read and
# 	#   parse our templates.  We pass in the loader object here.
# 	templateEnv = jinja2.Environment( loader=templateLoader )

# 	# This constant string specifies the template file we will use.
# 	TEMPLATE_FILE = "python-modules-bootstrap.template"

# 	# Read the template file using the environment object.
# 	# This also constructs our Template object.
# 	template = templateEnv.get_template( TEMPLATE_FILE )

# 	# Specify any input variables to the template as a dictionary.
# 	templateVars = { "name" : "Test Example",
# 	                 "desc" : "A simple inquiry of function." }

# 	# Finally, process the template to produce our final text.
# 	outputText = template.render( templateVars )
# 	print outputText


def template_formatter(template_dir, template_file, var_dict):

	# "/cosmo-packager/cosmo-packager/package-templates", "python-modules-bootstrap.template", {"var1": "HA!","var2": "DENNIS!"}
	env = Environment(loader=FileSystemLoader(template_dir))
	template = env.get_template(template_file)

	# lgr.debug('generating template from %s/%s with vars: %s' % (template_dir, template_file, var_dict))
	vars = var_dict
	formatted = template.render(vars)
	print formatted


def make_file(dir, output_file, content):

	lgr.debug('creating file %s/%s with content %s' % (dir, output_file, content))
	with open('%s/%s' % (dir, output_file), 'w+') as f:
		f.write(content)