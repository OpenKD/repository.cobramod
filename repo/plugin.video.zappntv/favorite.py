# -*- coding: utf-8 -*-

import logging
import json
import sys

import xbmcaddon
import xbmcvfs
import xbmc

from resources.lib import kodiutils
from resources.lib import kodilogging

try:
    from urllib.parse import quote, unquote, quote_plus, unquote_plus
except ImportError:
    from urllib import quote, unquote, quote_plus, unquote_plus

def log(info):
    if kodiutils.get_setting_as_bool("debug"):
        logger.warning(info)

logger = logging.getLogger(xbmcaddon.Addon().getAddonInfo('id'))
kodilogging.config()

__profile__ = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))

if not xbmcvfs.exists(__profile__):
    xbmcvfs.mkdirs(__profile__)

favorites_file_path = __profile__+"favorites.json"

log(u'launched: favorit.py with {0} arguments'.format(len(sys.argv)))

log(str(sys.argv))

if len(sys.argv) > 1:
    if sys.argv[1] == 'add' and len(sys.argv) == 6:
        # get parameters
        path = unquote(sys.argv[2])
        name = unquote(sys.argv[3])
        icon = unquote(sys.argv[4])
        fanart = unquote(sys.argv[5])

        if sys.version_info[0] < 3:
            # decode utf-8
            path = path.decode('utf-8')
            name = name.decode('utf-8')
            icon = icon.decode('utf-8')
            fanart = fanart.decode('utf-8')

        log(u'add favorite: {0}, {1}'.format(path, name))

        # load favorites
        favorites = {}
        if not favorites and xbmcvfs.exists(favorites_file_path):
            favorites_file = xbmcvfs.File(favorites_file_path)
            favorites = json.load(favorites_file)
            favorites_file.close()

        favorites.update({path : {'name': name, 'icon': icon, 'fanart': fanart}})
        # save favorites
        favorites_file = xbmcvfs.File(favorites_file_path, 'w')
        json.dump(favorites, favorites_file, indent=2)
        favorites_file.close()

        kodiutils.notification(kodiutils.get_string(32010), kodiutils.get_string(32011).format(name))
        xbmc.executebuiltin('Container.Refresh')
    elif sys.argv[1] == 'remove' and len(sys.argv) == 3:
        data = unquote(sys.argv[2])

        if sys.version_info[0] < 3:
            # decode utf-8
            data = data.decode('utf-8')

        # load favorites
        favorites = {}
        if not favorites and xbmcvfs.exists(favorites_file_path):
            favorites_file = xbmcvfs.File(favorites_file_path)
            favorites = json.load(favorites_file)
            favorites_file.close()

        if data in favorites:
            name = favorites[data]['name']
            del favorites[data]
            # load favorites
            favorites_file = xbmcvfs.File(favorites_file_path, 'w')
            json.dump(favorites, favorites_file, indent=2)
            favorites_file.close()

            kodiutils.notification(kodiutils.get_string(32010), kodiutils.get_string(32012).format(name))
            xbmc.executebuiltin('Container.Refresh')
