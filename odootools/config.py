#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 23:14:13 2022

Basic definitions to make Otools work.

@author: Simon Rundstedt
"""

#%%
import configparser

from dataclasses import dataclass,field

#%%


def load(conffile="/etc/odoo/odootool.ini",section=None):
    config = configparser.ConfigParser()
    config.read(conffile)
    confdict = dict(config[section] if section else config['DEFAULT'])

    confdict["addonsdirs"] = confdict["addonsdirs"].split(',')
    confdict["addonsprefixes"] = confdict["addonsprefixes"].split(',')
    
    return OdooToolsHandle(**confdict)
#%%
@dataclass
class OdooToolsHandle():
    '''
    Class representing the setup of an Odoo environment. Eg. User, filestore
    location, addons, etc
    '''
    # Based on Odoo SA's deb-package
    # Eg: see: /etc/systemd/system/multi-user.target.wants/odoo.service
    user: str = "odoo"
    group: str = "odoo"
    filestore: str = "/var/lib/odoo/.local/share/Odoo/filestore/"
    conf : str = "/etc/odoo/odoo.conf"
    coredir : str = "/usr/lib/python3/dist-packages/odoo/"

    # Odootools specific
    # TODO: Addons need to either contain all projects or a folder to find projects in.
    addons : list[str] = None # Detectable addons != The ones from conf
    addonsdirs : list[str] = field(default_factory=lambda: ["/opt/odootools/addons","/usr/share/"]) # Dirs with addons
    addonsprefixes : list[str] = field(default_factory=lambda: ["odoo-","odooext-"]) # Optional prefixes of addons

    # Extra functionality
    backupdir : str = "/var/backups"

    gitbranch : str = "main"

    synctarget : str = None
