#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 09:00:28 2022

@author: Simon Rundstedt
"""
#%%

import ast
import os
import sys

# import click

from . import config
from . import addons

#%% Internal:


#%% Public
MANIFEST_REQUIRED_FIELDS = ("name",)
def loadmanifest(path):
    '''
    '''
    with open(path) as mfile:
        # literal_eval is designed to be safe.
        retdict = ast.literal_eval(mfile.read())
        if not isinstance(retdict, dict):
            raise TypeError(f"Dict not read from {path}")
    for f in MANIFEST_REQUIRED_FIELDS:
        if f not in retdict:
            # TODO: Custom exception?
            raise ValueError("Required manifest field {} missing.".format(f))
    return retdict

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

# TODO : Split to this and _get_manifest_depends(manifest_file) Reason: Easier testing, more finegrained usage
def moduledependencies(path):
    '''
    Return dependencies of the module in path.

    Parameters
    ==========
    path : str
        Path of module.

    Returns
    =======
    dict :
        The manifest dictionary entry 'depends'
    '''
    manifest = loadmanifest(os.path.join(path,"__manifest__.py")) # TODO: Add for __openerp__ too?
    return manifest.get("depends",[])

def dependency_dictgraph(modulepaths,strict=False):
    '''
    Return a digraph in a Dict[str]->set(str)] format.

    Parameters
    ==========
    modulepaths : Iterable
        Iterable of module paths.
    strict : Boolean
        Raise an error if a path in modulepaths doesn't exist.
        If False ignore missing paths.

    Returns
    =======
    Dict :
        Dictionary str->set(str) with strings being module names.
    '''
    ret = {}
    for path in modulepaths:
        if not os.path.exists(path):
            if strict:
                raise FileNotFoundError("Path not found: {}".format(path))
            else:
                # Ignore the missing module
                continue

        name = os.path.basename(path)
        depends = moduledependencies(path)
        if name not in ret:
            ret[name] = set() # Module folder name is unique key to module
        for d in depends:
            ret[name].add(d)
    return ret

def _list_modules_in_dir(dirname):
    """
    Find all Odoo modules in directory dirname.

    Parameters
    ----------
    dirname : str
        Directory to search for Odoo modules.

    Returns
    -------
    ret : list[str]
        List with full paths to found modules.

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
