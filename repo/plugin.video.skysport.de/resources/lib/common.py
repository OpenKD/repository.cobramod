# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from kodi_six.utils import py2_encode

from base64 import b64encode as base64_b64encode, b64decode as base64_b64decode
from hashlib import md5 as hashlib_md5
from time import sleep as time_sleep
from uuid import UUID as uuid_UUID

import xbmc
import xbmcgui

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


class Common:


    def __init__(self, addon=None, addon_handle=None):
        self.addon = addon
        self.addon_handle = addon_handle
        self.addon_id = self.addon.getAddonInfo('id')
        self.addon_name = self.addon.getAddonInfo('name')
        self.addon_path = self.addon.getAddonInfo('path')

        self.cache = StorageServer.StorageServer(py2_encode('{0}.videoid').format(self.addon_name), 24 * 30)


    def log(self, msg):
        xbmc.log(str(msg), xbmc.LOGDEBUG)


    def build_url(self, query):
        return 'plugin://{0}?{1}'.format(self.addon_id, urlencode(query))


    def b64enc(self, data):
        enc_data = base64_b64encode(data)
        missing_padding = len(enc_data) % 4
        if missing_padding != 0:
            enc_data = '{0}{1}'.format(enc_data, py2_encode('=') * (4 - missing_padding))
        return enc_data


    def b64dec(self, data):
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data = '{0}{1}'.format(data, py2_encode('=') * (4 - missing_padding))
        return base64_b64decode(data)


    def get_listitem(self):
        return xbmcgui.ListItem()


    def get_dialog(self):
        return xbmcgui.Dialog()


    def dialog_ok(self, msg):
        self.get_dialog().ok(self.addon_name, msg)


    def dialog_notification(self, msg, icon=xbmcgui.NOTIFICATION_INFO, time=5000, sound=True):
        self.get_dialog().notification(self.addon_name, msg, icon, time, sound)


    def set_setting(self, key, value):
        return self.addon.setSetting(key, value)


    def get_setting(self, key):
        return self.addon.getSetting(key)


    def uniq_id(self):
        device_id = ''
        mac_addr = xbmc.getInfoLabel('Network.MacAddress')

        # hack response busy
        i = 0
        while not py2_encode(':') in mac_addr and i < 3:
            i += 1
            time_sleep(1)
            mac_addr = xbmc.getInfoLabel('Network.MacAddress')
        if py2_encode(':') in mac_addr:
            device_id = str(uuid_UUID(hashlib_md5(mac_addr.encode('utf-8')).hexdigest()))
        else:
            self.log('[{0}] error: failed to get device id ({1})'.format(self.addon_id, str(mac_addr)))
            self.dialog_ok('Ger??te-Id konnte nicht ermittelt werden.')
        return device_id
