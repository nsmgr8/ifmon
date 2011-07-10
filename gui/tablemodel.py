#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

from datetime import datetime, timedelta

from PySide.QtCore import (Qt, QAbstractTableModel, QDateTime, QLocale,
                           QCoreApplication)

from sqlobject import AND
from ifmon.ifmon import Bandwidth, Settings, save_data
from ifmon.utils import smart_bytes

class BandwidthTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super(BandwidthTableModel, self).__init__(parent)
        self.header = [
            QCoreApplication.translate('ifmon', 'Booted at'),
            QCoreApplication.translate('ifmon', 'Uptime'),
            QCoreApplication.translate('ifmon', 'Recieved'),
            QCoreApplication.translate('ifmon', 'Transmitted'),
            QCoreApplication.translate('ifmon', 'Total')
        ]
        for settings in Settings.select():
            self.settings = settings
            break
        else:
            now = datetime.now()
            start = datetime(year=now.year, month=now.month, day=1)
            self.settings = Settings(start=start, auto_update=False)
        self.populateData()

    def rowCount(self, parent):
        return len(self.bws)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            col = index.column()
            d = self.bws[index.row()].at(col)
            return {
                0: lambda x: QLocale().toString(QDateTime(x), u'hh:mm - dd MMM, yyyy'),
                1: lambda x: self.formatUptime(x),
            }.get(col, lambda x: self.smart_bytes(x))(d)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

    @staticmethod
    def formatUptime(time):
        s = ''
        loc = QLocale()
        if time.days > 0:
            d = QCoreApplication.translate('ifmon', 'days') if time.days > 1 \
                    else QCoreApplication.translate('ifmon', 'day')
            s = '%s %s, ' % (loc.toString(time.days), d)
        mm, ss = divmod(time.seconds, 60)
        hh, mm = divmod(mm, 60)
        def padded(d):
            if d < 10:
                return loc.toString(0) + loc.toString(d)
            else:
                return loc.toString(d)
        s += '%s:%s:%s' % (padded(hh), padded(mm), padded(ss))
        return s

    @staticmethod
    def smart_bytes(bytes_):
        sb = smart_bytes(bytes_)
        return "%s %s" % (QLocale().toString(sb[0]), sb[1])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]
            else:
                return QLocale().toString(section + 1)

        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Vertical:
                return Qt.AlignRight

    def populateData(self, start=None, end=None):
        save_data()
        if not start:
            start = self.settings.start
        else:
            self.settings.start = start
        if end:
            query = AND(Bandwidth.q.booted_at >= start,
                        Bandwidth.q.retrieved_at <= (end + timedelta(days=1)))
        else:
            query = Bandwidth.q.booted_at >= start
        self.bws = list(Bandwidth.select(query))
        received, transmitted = 0, 0
        for bw in self.bws:
            received += bw.received
            transmitted += bw.transmitted
        self.total = {'total': received+transmitted, 'received': received,
                      'transmitted': transmitted}
        self.reset()

