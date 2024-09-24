# Validating template variables
import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

check_parameter = 'whitebox-ai'
if not re.match(MODULE_REGEX, check_parameter):
    print('ERROR: %s is not a valid Python project name!' % check_parameter)

    # exits with status 1 to indicate failure
    sys.exit(1)

check_parameter = 'whitebox-ai'
if not re.match(MODULE_REGEX, check_parameter):
    print('ERROR: %s is not a valid Python project name!' % check_parameter)

    # exits with status 1 to indicate failure
    sys.exit(1)