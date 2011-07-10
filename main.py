#!/usr/bin/env python

#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

import sys
import os

from PySide.QtCore import QTranslator, QLocale
from PySide.QtGui import QApplication, QMessageBox

from gui.mainwindow import MainWindow
from ifmon.ifmon import setup_db

if __name__ == '__main__':
    app = QApplication(sys.argv)
    locale = QLocale.system().name()
    trans = QTranslator()
    trans.load('%s/locale/ifmon_%s' % (os.path.dirname(
        os.path.realpath(__file__)), locale.lower()))
    app.installTranslator(trans)
    try:
        setup_db()
    except:
        QMessageBox.critical(None, 'Database error',
            'Could not find the database.\n'
            'Please install it properly by running install.py on Ubuntu.\n'
            'For other Linux distributions, check the requirements.',
            QMessageBox.Ok)
        sys.exit(app.exit())
    else:
        mw = MainWindow()
        mw.show()
    sys.exit(app.exec_())

