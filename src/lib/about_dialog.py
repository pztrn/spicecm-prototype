# -*- coding: utf-8 -*-

# About dialog module

from PyQt4 import uic
from PyQt4.QtGui import QDialog

class About_Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi("ui/about.ui", self)
        self.ui.show()