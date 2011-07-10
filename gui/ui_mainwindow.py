# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Jul 10 16:33:12 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 500)
        MainWindow.setMinimumSize(QtCore.QSize(600, 500))
        MainWindow.setMaximumSize(QtCore.QSize(650, 16777215))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.dateFrom = QtGui.QDateEdit(self.centralwidget)
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setObjectName(_fromUtf8("dateFrom"))
        self.horizontalLayout.addWidget(self.dateFrom)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.dateTo = QtGui.QDateEdit(self.centralwidget)
        self.dateTo.setCalendarPopup(True)
        self.dateTo.setObjectName(_fromUtf8("dateTo"))
        self.horizontalLayout.addWidget(self.dateTo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkAuto = QtGui.QCheckBox(self.centralwidget)
        self.checkAuto.setObjectName(_fromUtf8("checkAuto"))
        self.horizontalLayout.addWidget(self.checkAuto)
        self.updateButton = QtGui.QPushButton(self.centralwidget)
        self.updateButton.setObjectName(_fromUtf8("updateButton"))
        self.horizontalLayout.addWidget(self.updateButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.labelTotal = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelTotal.setFont(font)
        self.labelTotal.setMargin(4)
        self.labelTotal.setIndent(10)
        self.labelTotal.setObjectName(_fromUtf8("labelTotal"))
        self.gridLayout.addWidget(self.labelTotal, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_Update_Now = QtGui.QAction(MainWindow)
        self.action_Update_Now.setObjectName(_fromUtf8("action_Update_Now"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menu_File.addAction(self.action_Update_Now)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Help.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.action_Update_Now, QtCore.SIGNAL(_fromUtf8("triggered()")), self.updateButton.click)
        QtCore.QObject.connect(self.dateFrom, QtCore.SIGNAL(_fromUtf8("editingFinished()")), self.action_Update_Now.trigger)
        QtCore.QObject.connect(self.dateTo, QtCore.SIGNAL(_fromUtf8("editingFinished()")), self.action_Update_Now.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bandwidth Monitor", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.dateFrom.setDisplayFormat(QtGui.QApplication.translate("MainWindow", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "To", None, QtGui.QApplication.UnicodeUTF8))
        self.dateTo.setDisplayFormat(QtGui.QApplication.translate("MainWindow", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAuto.setText(QtGui.QApplication.translate("MainWindow", "&Auto update", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("MainWindow", "&Update Now", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTotal.setText(QtGui.QApplication.translate("MainWindow", "Total: 0B", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Update_Now.setText(QtGui.QApplication.translate("MainWindow", "&Update Now", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Update_Now.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+U", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

