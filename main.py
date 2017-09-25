import os
import wx

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import sys
# add the project path into the sys.path
sys.path.append('/tmp/Fantacalcio/teammaker')
# add the virtualenv site-packages path to the sys.path
sys.path.append('/tmp/Fantacalcio/teammaker/venv/Lib/site-packages')


# noinspection PyUnresolvedReferences
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from teammaker.controller import Controller


class App(wx.App):
    # noinspection PyPep8Naming,PyMethodMayBeStatic
    def OnInit(self):
        Controller()
        return True


if __name__ == '__main__':
    app = App(False)
    app.MainLoop()
