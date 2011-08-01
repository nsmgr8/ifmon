import urwid

from mainview import MainView
from ifmon.ifmon import setup_db

class AppController(object):

    def __init__(self):
        self.view = MainView()

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=self.uninp)
        self.update()
        self.loop.run()

    def update(self, loop=None, user_data=None):
        self.view.populate()
        self.alarm = self.loop.set_alarm_in(1.0, self.update)

    def uninp(self, inp):
        if inp in ['q', 'Q']:
            raise urwid.ExitMainLoop()

def main(argv=None):
    try:
        setup_db()
    except:
        print 'Database Error'
        print '=============='
        print 'Could not find the database.'
        print 'Please install it properly by running install.py on Ubuntu.'
        print 'For other Linux distributions, check the requirements.',
    else:
        app = AppController()
        app.main()

