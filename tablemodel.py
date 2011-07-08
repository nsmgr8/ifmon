#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

from datetime import datetime, timedelta

from PySide.QtCore import (Qt, QAbstractTableModel)

from sqlobject import AND
from ifmon import Bandwidth, Settings, save_data
from utils import smart_bytes

class BandwidthTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super(BandwidthTableModel, self).__init__(parent)
        self.header = ['From', 'To', 'Recieved', 'Transmitted', 'Total']
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
            if col > 1:
                return '%.2f %s' % smart_bytes(d)
            else:
                return d.strftime('%H:%M, %d %b %Y')

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]
            else:
                return section + 1

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

