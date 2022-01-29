#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 00:16:30 2022

@author: Simon Rundstedt
"""
#%%


import os
import sys

# import click

from . import config

#%%

def listaddons(othandle):
    """
    List all addons (projects)  found in the input OdootoolsHandle.

    Parameters
    ----------
    othandle : OdooToolsHandle
        OdooToolsHandle with directories to search for addons

    Returns
    -------
    allprojectdirs : list[str]
        List with full paths to found addons

    """
    allprojectdirs = [] # Project = an addon (a collection of modules)
    for addonsdir in othandle.addonsdirs:
        try:
            _, subdirs, _ = next(os.walk(addonsdir))
        except StopIteration:
            raise FileNotFoundError("Directory: {} not found.".format(addonsdir))
        projectdirs = [] # Project = an addon (a collection of modules)
        if othandle.addonsprefixes:
            # Filter on prefix
            for prefix in othandle.addonsprefixes:
                projectdirs.extend(
                    (p for p in subdirs if p.startswith(prefix)))
        else:
            # All folders are considered projects
            projectdirs.extend(subdirs)
        allprojectdirs.extend(
            (os.path.join(addonsdir,X) for X in projectdirs))
    # allprojectdirs.sort()
    return allprojectdirs
