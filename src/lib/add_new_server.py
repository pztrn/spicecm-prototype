# -*- coding: utf-8 -*-

# Add new server dialog module
import os

from PyQt4.QtGui import QDialog
from PyQt4 import uic

class Add_New_Server_Dialog(QDialog):
    def __init__(self, servers_list_instance, core_instance):
        QDialog.__init__(self)
        self.servers_list = servers_list_instance
        self.core = core_instance

        self.ui = uic.loadUi("ui/server.ui", self)
        self.ui.setWindowTitle("Add new SPICE server")
        self.ui.show()

        self.ui.add_button.clicked.connect(self.add_new_server)
        self.ui.cancel_button.clicked.connect(self.close)

    def add_new_server(self):
        server_name = self.ui.server_name.text()
        server_address = self.ui.server_address.text()
        server_port = self.ui.server_port.text()
        server_password = self.ui.server_password.text()

        color_depth = self.ui.color_depth.itemText(self.ui.color_depth.currentIndex())
        fullscreen = self.ui.fullscreen_checkbox.checkState()

        server_data = {
            "name"          : str(server_name),
            "address"       : str(server_address),
            "port"          : str(server_port),
            "password"      : str(server_password),
            "depth"         : str(color_depth),
            "fullscreen"    : str(fullscreen)
        }

        self.servers_list.add_server(server_data)
        self.core.populate_servers_list()
        self.close()
