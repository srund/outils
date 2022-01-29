#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 21:42:31 2022

Database related utilities for Odoo addons

@author: Simon Rundstedt
"""
#%%

import os

import psycopg2

#%%

def db_connection_from_handle(othandle):
    '''
    Open a connection to the target database.

    Parameters
    ----------
    othandle : TYPE
        DESCRIPTION.

    Returns
    -------
    conn : 

    '''
    raise NotImplementedError("Implement me")
    
#%%

#%%
SQL_LIST_MODULES = "SELECT name FROM ir_module_module WHERE state  = 'installed'"
def simple_listmodules(conn):
    '''
    List installed modules on the database represented by conn.

    Parameters
    ----------
    conn : Postgres connection
        Open connection to target database.

    Returns
    -------
    result : list[str]
        List of installed module names as strings. Excluding path.

    '''
    with conn.cursor() as c:
        result = c.execute(SQL_LIST_MODULES)
    return result