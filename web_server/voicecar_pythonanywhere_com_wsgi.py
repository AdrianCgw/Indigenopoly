# This file contains the WSGI configuration required to serve up your
# web application at http://VoiceCar.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

import sys
path = '/home/VoiceCar/webcom'
if path not in sys.path:
    sys.path.append(path)

from app_logic import app as application #noqa
