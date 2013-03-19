# -*- coding: utf-8 -*-
import os
import sys
import signal

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib import common
from lib import icon_getter
from lib import spice_server_info
from lib import list_item
from lib import servers_list
from lib import add_new_server
from lib import edit_server
from lib import client_launcher
from lib import about_dialog

class SpiceCM_Window(QMainWindow):
    """
    SpiceCM main window
    """
    def __init__(self):
        QWidget.__init__(self)
        # Disabled items list - while we launch SPICE client, server(s)
        # we are connected to added to this list and on every item selection
        # we will check if we connected to server.
        self.disabled_servers = []

        # Check directories for existing
        common.check_directories()

        # Load UI
        self.ui = uic.loadUi("ui/mainwindow.ui", self)
        self.ui.show()

        # Adjusting splitter
        self.ui.splitter.setSizes([200, 500])
        self.ui.spice_item_description.setText(spice_server_info.greeting_message())

        # Getting servers list
        self.servers_list = servers_list.Servers_List()
        self.list_item = list_item.List_Item()

        # Adding actions to toolbar
        connect_to_server_icon = icon_getter.iconFromTheme("player_play")
        self.connect_to_server_action = QAction(connect_to_server_icon, "Connect to server", self)
        self.connect_to_server_action.setShortcut("Ctrl+G")
        self.connect_to_server_action.triggered.connect(self.connect_to_server)

        add_server_icon = icon_getter.iconFromTheme("add")
        add_server = QAction(add_server_icon, "Add new server", self)
        add_server.setShortcut("Ctrl+N")
        add_server.triggered.connect(self.add_new_server)

        edit_server_icon = icon_getter.iconFromTheme("stock_edit")
        edit_server = QAction(edit_server_icon, "Edit server", self)
        edit_server.setShortcut("Ctrl+E")
        edit_server.triggered.connect(self.edit_server)

        remove_server_icon = icon_getter.iconFromTheme("stock_delete")
        remove_server = QAction(remove_server_icon, "Remove server", self)
        remove_server.setShortcut("Ctrl+E")
        remove_server.triggered.connect(self.remove_server)

        self.ui.toolBar.addAction(self.connect_to_server_action)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(add_server)
        self.ui.toolBar.addAction(edit_server)
        self.ui.toolBar.addAction(remove_server)

        self.ui.spice_items_list.currentItemChanged.connect(self.update_server_info_widget)
        self.ui.spice_items_list.itemActivated.connect(self.connect_to_server)
        self.ui.action_Exit.triggered.connect(self.close_from_menu)
        self.ui.action_About_SpiceCM.triggered.connect(self.show_about_dialog)

        self.ui.spice_items_list.setColumnHidden(1, True)

        self.populate_servers_list()

    def populate_servers_list(self):
        """
        Populate servers list
        """
        # Update servers list
        self.servers_data = self.servers_list.get_servers()

        # Populate it!
        self.ui.spice_items_list.clear()
        for item in self.servers_data:
            item_widget = self.list_item.create_item(self.servers_data[item])

            item_for_list = QTreeWidgetItem()
            item_for_list.setText(1, item)
            self.ui.spice_items_list.addTopLevelItem(item_for_list)
            self.ui.spice_items_list.setItemWidget(item_for_list, 0, item_widget)

    def add_new_server(self):
        """
        Open "Add new server" dialog and eventually
        add new server.
        """
        add_new_server.Add_New_Server_Dialog(self.servers_list, self)

    def edit_server(self):
        """
        Edit selected server.
        """
        item_index = self.ui.spice_items_list.currentIndex().row()
        server_name = QString((self.ui.spice_items_list.currentItem().text(1)))
        edit_server.Edit_Server_Dialog(self.servers_list, self, str(server_name), item_index)

    def remove_server(self):
        """
        Remove server from list.
        """
        server_name = QString((self.ui.spice_items_list.currentItem().text(1)))
        self.servers_list.remove_server(str(server_name))
        self.populate_servers_list()

    def set_current_item(self, item_index):
        root = self.ui.spice_items_list.invisibleRootItem()
        child = root.childCount()
        for idx in range(0, child):
            if idx == item_index:
                item = root.child(idx)
                self.ui.spice_items_list.setCurrentItem(item)


    def update_server_info_widget(self):
        server_name = QString((self.ui.spice_items_list.currentItem().text(1)))
        server_name = str(server_name)
        if server_name in self.disabled_servers:
            self.connect_to_server_action.setEnabled(False)
        else:
            self.connect_to_server_action.setEnabled(True)
        try:
            server_name = QString((self.ui.spice_items_list.currentItem().text(1)))
            self.ui.spice_item_description.setText(spice_server_info.construct(self.servers_data[str(server_name)]))
        except:
            # Happens only on server editing, due to some bugs in
            # QTreeWidget, so passing
            pass

    def connect_to_server(self):
        """
        Connect to SPICE server.
        """
        self.connect_to_server_action.setEnabled(False)
        server_name = QString((self.ui.spice_items_list.currentItem().text(1)))
        print "Connecting to", str(server_name)
        p = client_launcher.Client_Launcher(self, self.servers_list, server_name)
        p.start()

    def add_to_disabled(self, server_name):
        """
        Add specified server to disabled list.
        """
        self.disabled_servers.append(server_name)

    def remove_from_disabled(self, server_name):
        """
        Remove server from disabled list.
        """
        self.connect_to_server_action.setEnabled(True)
        idx = self.disabled_servers.index(server_name)
        self.disabled_servers.pop(idx)

    def process_events(self):
        """
        Nuff said.
        """
        QApplication.processEvents()

    def show_about_dialog(self):
        """
        About dialog. Nuff said.
        """
        about_dialog.About_Dialog()

    def close_from_menu(self):
        """
        Close SpiceCM from menu.
        """
        self.close()

    def closeEvent(self, event):
        """
        Close SpiceCM...
        """
        print "Closing SpiceCM..."
        self.servers_list.write_servers_data()

class SpiceCM_Launch:
    """
    Launch SpiceCM.
    """
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QApplication(sys.argv)
        spicecm_window = SpiceCM_Window()
        sys.exit(app.exec_())
