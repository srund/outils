#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 10:16:49 2022

@author: Simon Rundstedt
"""
#%%

import os
import networkx as nx

from odootools import addons
from odootools import config
from odootools import modules

#%%

#def module_digraph_from_paths(paths,excludepaths=None,strict=True,exclude="flatten"):
#    ''''''

_VALIDCOREOPTIONS = ("include",'exclude',"flatten")
def module_digraph(othandle,strict=True,core="include"):
    '''
    Load module dependencies as a Networkx DiGraph from an OdooToolsHandle.

    Parameters
    ==========
    othandle : OdooToolsHandle
        OdooToolsHandle object
    strict : Boolean
        Raise an error if a path in modulepaths doesn't exist.
    core : str
        How to deal with Odoo core modules.
        Valid values 'include','exclude','flatten'.
        Set to 'flatten' to map core modules to dummy module 'core'

    Returns
    =======
    DiGraph :
        A Networkx DiGraph of the module dependencies.
    '''
    if core not in _VALIDCOREOPTIONS:
        raise ValueError(f"Option 'core' not in  {_VALIDCOREOPTIONS}")
    # TODO: Maybe do check against dublicates ? For now lets just build the
    # basic functionality.
    # TODO: Refactor and split into smaller chunks
    modulepaths = modules.listmodules(othandle,includecore=False)
#    modulenames = { os.path.basename(p) for p in  modulepaths }

    mod_core_paths = modules.listcoremodules(othandle)
    mod_core_names = { os.path.basename(p) for p in  mod_core_paths }
    dg = nx.DiGraph()
    for path in modulepaths:
        if strict and not os.path.exists(path):
            raise FileNotFoundError("Path not found: {}".format(path))
        else:
            name = os.path.basename(path)
            depends = modules.moduledependencies(path)
            if name not in dg: # Nodes not attached to anything is allowed.
                dg.add_node(name)
            for d in depends:
                if d not in mod_core_names or core == "include":
                    dg.add_edge(name,d)
                else:
                    if core == "exclude":
                        pass
                    elif core == "flatten":
                        dg.add_edge(name,"core")
                    else:
                        # Shouldn't happen
                        pass
    if core == "include":
        for path in mod_core_paths:
            # mod_core_paths should only contain things that exist or already
            # have triggered an Exception.
            name = os.path.basename(path)
            depends = modules.moduledependencies(path)
            if name not in dg: # Nodes not attached to anything is allowed.
                dg.add_node(name)
                for d in depends:
                    if not d in mod_core_names:
                        raise ValueError(
                           f"Dependency from core detected: {name}->{d}")
                    dg.add_edge(name,d)
            
    return dg
    