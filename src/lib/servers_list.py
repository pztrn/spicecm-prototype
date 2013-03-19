# -*- coding: utf-8 -*-

# Servers List module - responsible for all actions with server list.
import os
import json

class Servers_List:
    def __init__(self):
        # Servers list location
        self.servers_list_json = os.path.expanduser("~/.config/spicecm/servers_list.json")

        # Checking if config exist. If not - create empty dict
        # for later servers handling.
        if os.path.exists(self.servers_list_json):
            f = open(self.servers_list_json, "r")
            self.servers_data = json.loads(f.read())
            f.close()
            print "Loaded", len(self.servers_data), "servers."
        else:
            self.servers_data = {}
            print "Can't read servers list, file doesn't exist. Creating empty dictionary."

    def get_servers(self):
        """
        Return dictionary with servers.
        """
        return self.servers_data

    def add_server(self, server_dict):
        """
        Add server into list
        """
        self.servers_data[server_dict["name"]] = server_dict

    def remove_server(self, server_name):
        """
        Remove server from list
        """
        try:
            del self.servers_data[server_name]
            return 0
        except:
            return 1

    def write_servers_data(self):
        """
        Write server data on disk
        """
        print "Saving servers data..."
        f = open(self.servers_list_json, "w")
        data = json.dumps(self.servers_data, indent = 4)
        f.write(data)
        f.close()