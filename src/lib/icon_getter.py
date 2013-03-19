# -*- coding: utf-8 -*-

# Icon getter module - get icon for current icon theme.
# Due to: https://bugreports.nokia.com/browse/QTBUG-18807
import os
from PyQt4.QtGui import QIcon

def get_desktop():
    desktop_environment = "generic"
    if os.environ.get("KDE_FULL_SESSION") == "true":
        desktop_environment = "kde"
    elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        desktop_environment = "gnome"
    return desktop_environment

def iconFromTheme(*names, **kwargs):
    size = kwargs["size"] if "size" in kwargs else 32
    try:
        from PyKDE4.kdeui import KIcon
        for name in names:
            if KIcon.hasThemeIcon(name):
                return KIcon(name)
    except:
        pass
    if get_desktop() == "generic":
        try:
            from gtk import icon_theme_get_default
            iconTheme = icon_theme_get_default()
            for name in names:
                iconInfo = iconTheme.lookup_icon(name, size, 0)
                if iconInfo:
                    return QIcon(iconInfo.get_filename())
        except:
            pass
    for name in names:
        if QIcon.hasThemeIcon(name):
            return QIcon(QIcon.fromTheme(name))

        return QIcon()