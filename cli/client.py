#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 16:24:20 2022

Don't use

Future client program of Odootools. Currently used a draft of possible ways
to go forward.

@author: Simon Rundstedt
"""
#%%

import configparser

import click

from odootools import addons
from odootools import config
from odootools import modules

#%%

OTHANDLE = config.OdooToolsHandle()

#%%

@click.group()
@click.option("--ot-conf",help="Alternative config file for Odootools.")
#@click.option("--ot-handle",help="Alternative config handle to load from the Odootools config file.")
@click.option("-d","--database", help="When applicable only perform subcommands on a particular database")
@click.pass_context
def main(ctx, **kwargs):
    '''
    '''
    ctx.ensure_object(dict) # As recommended by doc : https://click.palletsprojects.com/en/8.0.x/commands/#nested-handling-and-contexts
    click.echo(kwargs)
#    if kwargs["ot_handle"]:
#        raise NotImplementedError("Not implemented")
    if kwargs["database"]:
        ctx.obj["database"] = kwargs["database"]
    if kwargs["ot_conf"]:
        ctx.obj["othandle"] = config.load(kwargs["ot_conf"])

@main.command(help="Display projects")
@click.option('-p','--prefixes',help="Comma separated list of prefixes or '' to consider all folders as projects.")
@click.pass_obj
def addon(cobj,**kwargs):
    '''
    List projects (addons) consisting of multiple modules found in addonsdirs.
    '''
    click.echo(kwargs)
    othandle = cobj.get("othandle",OTHANDLE)
    if kwargs["prefixes"] is not None:
        othandle.addonsprefixes = list(
            filter(None,kwargs["prefixes"].split(",")))

    result = addons.listaddons(othandle)
    for r in result:
        click.echo(r)

@main.command(help="Display module information")
@click.option('--dublicates',help="Only print dublicate modules",is_flag=True,default = False)
#@click.option('-d','--diagnose', help="Diagnose the module configuration for errors",is_flag=True,default = False)
@click.option('-c/-x','--include-core/--exclude-core',help="Include or exclude core addons",is_flag=True,default = True)
@click.pass_obj # Enough to get ctx.obj
def module(cobj,**kwargs):
    '''
    List modules, find duplicates etc.
    '''
    othandle = cobj.get("othandle",OTHANDLE)

    result = modules.listmodules(othandle,kwargs["include_core"])
    if not kwargs["dublicates"]:
        for r in result:
            click.echo(r)
    else:
        for m,paths in modules.listduplicates(result).items():
            for p in paths:
                click.echo("{}\t{}".format(m,p))
        



#%%
if __name__ == '__main__':
    main(obj={})
