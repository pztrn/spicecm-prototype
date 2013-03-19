# -*- coding: utf8 -*-

# Construct server info messages

greeting_text = \
"""<h1>Welcome to SpiceCM!</h1>
SpiceCM allows you to manage your SPICE VDI connections.<br />
<br />
SpiceCM licensed under Terms and Conditions of GNU General
Public License version 3 or any higher version.<br />
<br />
<a href="http://spice-space.org/">What is SPICE?</a>

<h2>Participating in development of SpiceCM</h2>
Bugreports, ideas and suggestion you can send to
<a href="https://dev.pztrn.name/index.php?project=5&do=index&switch=1">
SpiceCM bugtracker</a>
"""

# Server info template
server_info = \
"""<h2>{0}</h2>
<b>Address:</b>{1}<br />
<b>Port:</b> {2}<br />

<h2>Graphics</h2>
<b>Color depth:</b> {3}<br />
<b>Fullscreen:</b> {4}
"""

def greeting_message():
    return greeting_text

def construct(server_dict):
    if server_dict["fullscreen"] == "0":
        fullscreen = "False"
    else:
        fullscreen = "True"
    return server_info.format(server_dict["name"], server_dict["address"], server_dict["port"], server_dict["depth"], fullscreen)