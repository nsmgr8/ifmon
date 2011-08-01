#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

from datetime import timedelta, datetime
import sys

from PySide.QtCore import Qt, QTimer, QCoreApplication
from PySide.QtGui import QMainWindow, QMessageBox, QApplication, QIcon

from sqlobject import dberrors

from ui_mainwindow import Ui_MainWindow
from aboutdialog import AboutDialog
from tablemodel import BandwidthTableModel

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/ifmon.png'))

        try:
            self.model = BandwidthTableModel(self)
        except dberrors.OperationalError as e:
            QMessageBox.critical(self, 'Database Error',
                    'Could not access database.\nERROR: %s' % e)
            sys.exit(QApplication.exit())

        self.tableView.setModel(self.model)
        self.tableView.resizeColumnToContents(0)
        self.tableView.resizeColumnToContents(1)
        self.tableView.setAlternatingRowColors(True)

        self.dateFrom.setDate(self.model.settings.start)
        self.dateTo.setDate(self.model.settings.start + timedelta(days=29))
        self.statusBar().addWidget(self.labelTotal)
        self.updateTotal()

        self.actionAbout.triggered.connect(self.about)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateUsage)
        self.timer.start()

    def updateUsage(self):
        d = self.dateFrom.date()
        start = datetime(year=d.year(), month=d.month(), day=d.day())
        d = self.dateTo.date()
        end = datetime(year=d.year(), month=d.month(), day=d.day())
        try:
            self.model.populateData(start, end)
        except dberrors.OperationalError as e:
            QMessageBox.critical(self, 'Database Error',
                    'Could not access database.\nERROR: %s' % e)
            sys.exit(QApplication.exit())

        self.updateTotal()
        self.tableView.resizeColumnToContents(0)
        self.tableView.resizeColumnToContents(1)

    def updateTotal(self):
        if self.model.total['total'] > 0:
            stat = self.model.total
            total = BandwidthTableModel.smart_bytes(stat['total'])
            received = BandwidthTableModel.smart_bytes(stat['received'])
            transmitted = BandwidthTableModel.smart_bytes(stat['transmitted'])
            self.labelTotal.setText(QCoreApplication.translate("ifmon",
                "Total: <b>%s</b> (<b>%s</b> received, <b>%s</b> transmitted)")
                                    % (total, received, transmitted))

    def about(self):
        AboutDialog(self).exec_()

import resources.resources
