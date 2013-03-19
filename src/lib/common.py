# -*- coding: utf-8 -*-

# Common module - some common routines
import os

def check_directories():
    """
    Check for directories existing required by SpiceCM.
    """
    if not os.path.exists(os.path.expanduser("~/.config/spicecm/")):
        print "SpiceCM configuration directory doesn't exist, creating"
        os.makedirs(os.path.expanduser("~/.config/spicecm/"))