import os
import wx

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import sys
# add the project path into the sys.path
sys.path.append(os.getcwd())
# sys.path.append('/tmp/progetti/teammaker')
# sys.path.append('/tmp/progetti/teammaker/venv/Lib/site-packages')
# add the virtualenv site-packages path to the sys.path
venv_path = '\\'.join([os.getcwd(), 'venv\\Lib\\site-packages'])
sys.path.append(venv_path)

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
