# -*- coding: utf-8 -*-

# Servers list item module
# Handling item creation
import os
from PyQt4.QtGui import QWidget, QLabel, QVBoxLayout

class List_Item:
    """
    Creating a QTreeWidgetItem for specified server.
    """
    def __init__(self):
        pass

    def create_item(self, server_dict):
        # Server name
        label1 = QLabel()
        label1.setText("<b>" + server_dict["name"] + "</b>")

        # Server address
        label2 = QLabel()
        label2.setText("<i>" + server_dict["address"] + ":" + server_dict["port"] + "</i>")

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)

        widget = QWidget()
        widget.setLayout(layout)

        return widget