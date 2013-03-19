# -*- coding: utf-8 -*-

# SPICE client launcher. Nuff said.
import os
import commands

from PyQt4.QtCore import QThread, QProcess, SIGNAL

class Client_Launcher:
    def __init__(self, core_instance, serverslist_instance, server_name):
        #QThread.__init__(self)
        self.core = core_instance
        self.servers_list = serverslist_instance
        self.server_name = str(server_name)
        self.spice_process = QProcess()
        self.core.add_to_disabled(self.server_name)

    def start(self):
        servers = self.servers_list.get_servers()
        server_data = servers[self.server_name]

        # Forming command
        self.command = "/usr/bin/spicec -h {0} -p {1} ".format(server_data["address"], server_data["port"])
        if len(server_data["password"]) != 0:
            self.command += "-w {0} ".format(server_data["password"])

        if server_data["fullscreen"] != "0":
            self.command += "-f "

        if server_data["depth"] == "16 bit":
            self.command += "--color-depth 16"
        else:
            self.command += "--color-depth 32"

        process_state = self.spice_process.startDetached(self.command)
        if process_state:
            watcher = Client_Watcher(self.core, server_data["port"], self.server_name)
            watcher.run()


class Client_Watcher(QThread):
    """
    Check if detached process is running.
    If process completed - remove server name from
    disabled servers.

    Dirty hack. Really dirty. But IDK how to do it in a
    proper way. Feel free so suggest on bugtracker.
    """
    def __init__(self, core_instance, port, server_name):
        QThread.__init__(self)
        self.core = core_instance
        self.port = port
        self.server_name = server_name

    def run(self):
        print "Started process watcher thread..."
        watch_times = 0
        while True:
            data = commands.getoutput("ps ax | grep '/usr/bin/spicec' | grep -v grep")
            if len(data) > 0:
                self.usleep(100000)
                self.core.process_events()
                watch_times += 1
            else:
                break

        print "Process watcher thread stopped. Watched", watch_times, "times."
        self.finished()
        self.quit()

    def finished(self):
        self.core.remove_from_disabled(self.server_name)