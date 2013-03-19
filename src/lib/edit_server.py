# -*- coding: utf-8 -*-

# Edit server dialog module
import os

from PyQt4.QtGui import QDialog
from PyQt4 import uic

class Edit_Server_Dialog(QDialog):
    def __init__(self, servers_list_instance, core_instance, server_name, item_index):
        QDialog.__init__(self)
        self.servers_list = servers_list_instance
        self.core = core_instance
        self.servers_data = self.servers_list.get_servers()
        self.item_index = item_index

        self.ui = uic.loadUi("ui/server.ui", self)
        self.ui.setWindowTitle("Edit SPICE server")
        self.ui.show()

        self.ui.add_button.setText("Edit")

        self.ui.server_name.setText(self.servers_data[server_name]["name"])
        self.ui.server_address.setText(self.servers_data[server_name]["address"])
        self.ui.server_port.setText(self.servers_data[server_name]["port"])
        self.ui.server_password.setText(self.servers_data[server_name]["password"])

        self.ui.add_button.clicked.connect(self.edit_server)
        self.ui.cancel_button.clicked.connect(self.close)

    def edit_server(self):
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
        self.core.set_current_item(self.item_index)
        self.close()
