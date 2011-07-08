#
#   ifmon - A network usage viewer for Linux
#
#   Copyright (c) 2011, M. Nasimul Haque
#
#   MIT license
#

from PySide.QtGui import QDialog, QPixmap

from ui_aboutdialog import Ui_AboutDialog

class AboutDialog(QDialog, Ui_AboutDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.labelIcon.setPixmap(QPixmap(':/ifmon.png'))

