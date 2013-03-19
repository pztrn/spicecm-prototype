#!/usr/bin/env python2

# SpiceCM - Connection manager for SPICE, written in python2/pyqt4.
# Copyright (c) 2013, Stanislav N. aka pztrn.
# Licensed under Terms and Conditions of GNU General Public
# License version 3 or higher.

import os, sys
import main

def launch():
    """
    Launch SpiceCM main window.
    """
    main.SpiceCM_Launch()

if __name__ == "__main__":
    launch()
else:
    print "SpiceCM main executable doesn't designed for imports!"
    exit()
