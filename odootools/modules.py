#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 09:00:28 2022

@author: Simon Rundstedt
"""
#%%

import os
import sys

# import click

from . import config
from . import addons

#%%

def dirismodule(dirname):
    '''
    Test if directory 'dirname' is an Odoo module

    Parameters
    ----------
    path : str
        Path to directory of directory to test.

    Returns
    -------
    Boolean :
        Wether or not the directory is a module
    '''
    # More naughty version:
    # return any((os.path.exists(os.path.join(dirname + X) for X in ("__manifest__.py","__openerp__.py")))
    return os.path.exists(os.path.join(dirname, "__manifest__.py"))

def _list_modules_in_dir(dirname):
    """
    Find all Odoo modules in directory dirname.

    Parameters
    ----------
    dirname : str
        Directory to search for Odoo modules

    Returns
    -------
    ret : list[str]
        List with full paths to found modules´

    """
    try:
        _, subdirs, _ = next(os.walk(dirname))
    except StopIteration:
        raise FileNotFoundError("Directory: {} not found.".format(dirname))
    return [os.path.join(dirname, d) for d in subdirs if dirismodule(
            os.path.join(dirname, d))]

def listduplicates(modules):
    """
    Find module names defined more than once and return a name->path mapping
    of them.

    Parameters
    ----------
    modules : list[str]
        List of paths of modules

    Returns
    -------
    dict
        Dictionary mapping module names to paths for duplicate names in modules

    """
    moddict = {os.path.basename(m):set() for m in modules} # Dict(str->set()) since paths are unique in an OS
    for m in modules:
        n = os.path.basename(m)
        moddict[n].add(m)
    return { n:m for n,m in moddict.items() if len(m) > 1 }

def listcoremodules(othandle):
    '''
    List core modules found in othandle.

    Parameters
    ----------
    othandle : OdooToolsHandle
        OdooToolsHandle object

    Returns
    -------
    modules : list[str]
        A sorted list of full paths to found modules.
    '''
    modules = _list_modules_in_dir(os.path.join(othandle.coredir,'addons'))
    modules.sort()
    return modules
    
def listmodules(othandle,includecore=True):
    """
    List modules found in othandle

    Parameters
    ----------
    othandle : OdooToolsHandle
        OdooToolsHandle object

    Returns
    -------
    modules : list[str]
        A sorted list of full paths to found modules.
    """
    modules = []
    for dirname in addons.listaddons(othandle):
        modules.extend(_list_modules_in_dir(dirname))
    if includecore:
        modules.extend(listcoremodules(othandle))
    modules.sort()
    return modules
# #%%
#
# @click.command()
# @click.option("-f","--fullpath",help="Print full path of found modules", is_flag=True, default=False)
# def main(**kwargs):
#     mhandle = base.OdooToolsHandle()
#     result = listmodules(mhandle)
#     if not kwargs["fullpath"]:
#         result = [ os.basename(r) for r in result]
#         result.sort()
#     for r in result:
#         click.echo(r)
#
# #%%
#
# if __name__ == '__main__':
#     main()
#
