import datetime
import urwid

from sqlobject import AND
from ifmon.ifmon import Bandwidth, Settings, save_data
from ifmon.utils import smart_bytes

class MainView(urwid.Frame):

    palette = [
        ('bg', 'white', 'dark gray'),
        ('header', 'white', 'dark red',),
        ('footer', 'black', 'yellow',),
        ('banner', 'dark red', 'white',),
        ('thead', 'dark red', 'yellow',),
        ('tfoot', 'yellow', 'dark red',),
        ('data 0', 'black', 'dark cyan',),
        ('data 1', 'black', 'light blue',),
        ('filler bg', '', 'light magenta'),
        ('button normal', 'light gray', 'dark blue', 'standout'),
        ('button select', 'white', 'dark green',),
    ]

    def __init__(self):
        header = urwid.AttrWrap(urwid.Text(('banner',
                                            ' .oO Bandwidth Monitor Oo. '),
                                           align='center'),
                                'header')
        self.status = urwid.Text(('banner', ' Ready '), align='right')
        help_text = 'Use arrow keys to scroll the list and move to the' \
                ' buttons. Press "q" to quit.'
        footer = urwid.AttrWrap(urwid.Columns([urwid.Text(help_text),
                                               self.status]),
                                'footer')

        self.start = urwid.Text(('date', ''), align='right')
        self.end = urwid.Text(('date', datetime.date.today() \
                                       .strftime('  %d %B %Y  ')),
                              align='left')
        dates = urwid.Filler(urwid.Columns([
            self.start, urwid.Text(' to ', align='center'), self.end,
        ]), ('fixed top', 1))

        thead, tfoot = [], []
        self.total = {}
        for label in ['Booted at', 'Uptime', 'Received', 'Transmitted', 'Total']:
            thead.append(urwid.AttrWrap(urwid.Text(label, align='right'),
                                        'thead'))
            self.total[label] = urwid.Text('', align='right')
            tfoot.append(urwid.AttrWrap(self.total[label], 'tfoot'))
        self.total['Booted at'].set_text('Total')
        thead = urwid.Filler(urwid.Columns(thead, 1, min_width=12))
        tfoot = urwid.Filler(urwid.Columns(tfoot, 1, min_width=12))

        self.tbody = urwid.ListBox([])
        qbutton = urwid.Filler(urwid.Columns([
#            urwid.Padding(urwid.AttrWrap(urwid.Button('Settings',
#                                                      self.settings_dialog),
#                                         'button normal', 'button select'),
#                          'right', 12),
            urwid.Divider('~'),
            urwid.Padding(urwid.AttrWrap(urwid.Button('Quit', self.quit),
                                         'button normal', 'button select'),
                          'center', 8),
            urwid.Divider('~')], 3))
        body = urwid.AttrMap(urwid.Pile([
            ('fixed', 3, dates),
            ('fixed', 1, thead),
            self.tbody,
            ('fixed', 1, tfoot),
            ('fixed', 3, qbutton)
        ]), 'bg')
        super(MainView, self).__init__(body=body, header=header, footer=footer)

        for settings in Settings.select():
            self.settings = settings
            break
        else:
            now = datetime.datetime.now()
            start = datetime.datetime(year=now.year, month=now.month, day=1)
            self.settings = Settings(start=start)

        self.populate()

    def populate(self, start=None, end=None):
        save_data()
        if not start:
            start = self.settings.start
        else:
            self.settings.start = start
        if end:
            query = AND(Bandwidth.q.booted_at >= start,
                        Bandwidth.q.retrieved_at <= (end + datetime.timedelta(days=1)))
        else:
            query = Bandwidth.q.booted_at >= start
        self.bws = list(Bandwidth.select(query))
        received, transmitted = 0, 0
        uptime = datetime.timedelta(days=0)
        for bw in self.bws:
            received += bw.received
            transmitted += bw.transmitted
            uptime = uptime + bw.uptime()
        self.totaldata = {'total': received+transmitted, 'received': received,
                'transmitted': transmitted, 'uptime': uptime}
        self.reset()

    def reset(self):
        rows = []
        for j, bw in enumerate(self.bws):
            cols = []
            for i in range(5):
                data = bw.at(i)
                text = {
                    0: lambda x: x.strftime('%H:%M %d/%m/%y'),
                    1: lambda x: str(x),
                }.get(i, lambda x: '%.2f %s' % smart_bytes(x))(data)
                cols.append(urwid.AttrWrap(urwid.Text(text, align='right'),
                                           'data %d' % (j%2,)))
            rows.append(urwid.Columns(cols, 1, min_width=12))
        self.tbody.body = urwid.SimpleListWalker(rows)
        self.start.set_text(('date', self.settings.start.strftime('  %d %B %Y  ')))
        self.total['Uptime'].set_text(str(self.totaldata['uptime']))
        self.total['Received'].set_text('%.2f %s' % smart_bytes(self.totaldata['received']))
        self.total['Transmitted'].set_text('%.2f %s' % smart_bytes(self.totaldata['transmitted']))
        self.total['Total'].set_text('%.2f %s' % smart_bytes(self.totaldata['total']))

        self.status.set_text(('banner', datetime.datetime.now().strftime('  %d %B, %Y - %H:%M:%S  ')))

    def quit(self, w):
        raise urwid.ExitMainLoop()

    def settings_dialog(self, w):
        pass

