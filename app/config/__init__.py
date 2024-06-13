import os
import sys

import app.config.settings


# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
_current = getattr(sys.modules['app.config.settings'], '{0}Config'.format(APP_ENV))()