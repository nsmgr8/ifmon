#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

from datetime import timedelta, datetime
import sys

from PySide.QtCore import Qt, QTimer
from PySide.QtGui import QMainWindow, QMessageBox, QApplication, QIcon

from sqlobject import dberrors

from ui_mainwindow import Ui_MainWindow
from aboutdialog import AboutDialog
from tablemodel import BandwidthTableModel
from utils import smart_bytes

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

        self.updateButton.clicked.connect(self.updateUsage)
        self.checkAuto.stateChanged.connect(self.setAutoUpdate)
        self.actionAbout.triggered.connect(self.about)

        self.timer = QTimer()
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.updateUsage)
        self.checkAuto.setCheckState(self.model.settings.auto_update and \
                                     Qt.Checked or Qt.Unchecked)

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
            total = "%.2f %s" % smart_bytes(stat['total'])
            received = "%.2f %s" % smart_bytes(stat['received'])
            transmitted = "%.2f %s" % smart_bytes(stat['transmitted'])
            self.labelTotal.setText("Total: <b>%s</b> (<b>%s</b> received, "
                                    "<b>%s</b> transmitted)" %
                                    (total, received, transmitted))

    def setAutoUpdate(self, state):
        if state == Qt.Unchecked:
            if self.timer.isActive():
                self.timer.stop()
            self.action_Update_Now.setEnabled(True)
            self.updateButton.setEnabled(True)
            self.model.settings.auto_update = False
        else:
            if not self.timer.isActive():
                self.timer.start()
            self.model.settings.auto_update = True
            self.action_Update_Now.setEnabled(False)
            self.updateButton.setEnabled(False)

    def about(self):
        AboutDialog(self).exec_()

import resources
