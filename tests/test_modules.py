#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 15:06:01 2022

@author: Simon Rundstedt
"""
#%%
import os
import sys

import unittest

# Note non-relative import. The unittest module will take care of import from
# project root
from odootools import config
from odootools import modules

#%%

TESTDIR = os.path.dirname(__file__)

class TestFindModules(unittest.TestCase):
    '''
    '''
    def setUp(self):
        '''
        '''
        self.handle = config.load(os.path.join(TESTDIR, 'test_handle.ini'))

    def test_listmodules_non_found(self):
        '''
        '''
        self.handle.addonsdirs = ["tests/testdirs/addons3"]
        flines = modules.listmodules(self.handle,includecore=False)
        self.assertListEqual([],flines)

    def test_list_modules_file_not_found(self):
        '''
        '''
        self.assertRaises(FileNotFoundError,
                          modules._list_modules_in_dir,"/doesnt/exist")

    #
    # DEV NOTE: test_listmodules... are indirect tests of _list_modules_in_dir
    #
    def test_listmodules_prefix_nbr_of_entries(self):
        '''
        '''
        with open(os.path.join(TESTDIR,"test_modules_01_list_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            t_nbr_lines = len(list(filter(None,tlines)))
        self.assertEqual(len(modules.listmodules(self.handle)),t_nbr_lines)


    def test_listmodules_prefix(self):
        '''
        '''
        with open(os.path.join(TESTDIR,"test_modules_01_list_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = modules.listmodules(self.handle)
        flines.sort()
        self.assertListEqual(flines,tlines)

    def test_listmodules_no_prefix(self):
        '''
        '''
        self.handle.addonsprefixes = None
        with open(os.path.join(TESTDIR,"test_modules_02_list_no_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = modules.listmodules(self.handle)
        flines.sort()
        self.assertListEqual(flines,tlines)

    def test_listmodules_no_core(self):
        '''
        '''
        with open(os.path.join(TESTDIR,"test_modules_03_list_nocore.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = modules.listmodules(self.handle,includecore=False)
        flines.sort()
        self.assertListEqual(flines,tlines)

    def test_listcoremodules_only(self):
        '''
        '''
        with open(os.path.join(TESTDIR,"test_modules_04_list_coreonly.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = modules.listcoremodules(self.handle)
        flines.sort()
        self.assertListEqual(flines,tlines)

    def test_listdublicates_keys(self):
        '''
        '''
        keys = ["module1","module2"]
        flines = modules.listmodules(self.handle,includecore=False)
        fdub = modules.listduplicates(flines)
        for k in fdub:
            self.assertTrue(k in keys)

    def test_listdublicates_paths(self):
        '''
        '''
        expected = {
                "module1": {"tests/testdirs/addons1/odoo-project/module1",
                            "tests/testdirs/addons1/odooext-project/module1",
                            "tests/testdirs/addons2/odoo-project/module1",
                            "tests/testdirs/addons2/odooext-project/module1"},
                "module2": {"tests/testdirs/addons1/odooext-project/module2",
                            "tests/testdirs/addons2/odooext-project/module2"},
            }
        flines = modules.listmodules(self.handle,includecore=False)
        fdub = modules.listduplicates(flines)
        for k in fdub:
            self.assertSetEqual(expected[k], fdub[k])

    def test_dirismodule_manifest_exists(self):
        '''
        '''
        path = "tests/testdirs/addons1/odoo-project/module1"
        self.assertTrue(modules.dirismodule(path))

    def test_dirismodule_manifest_missing(self):
        '''
        '''
        path = "tests/testdirs/addons1/odoo-project/non-module"
        self.assertFalse(modules.dirismodule(path))

    def test_loadmanifest_missing_field(self):
        '''
        '''
        path = "tests/testmanifests/manifest_02_no_name.py"
        self.assertRaises(ValueError, modules.loadmanifest, path)

    def test_loadmanifest_load_wellbehaving(self):
        '''
        '''
        path = "tests/testmanifests/manifest_01_good.py"
        ret = modules.loadmanifest(path)
        self.assertEqual("Expected", ret["name"])

    def test_loadmanifest_load_nondict(self):
        '''
        '''
        path = "tests/testmanifests/manifest_03_notdict.py"
        self.assertRaises(TypeError, modules.loadmanifest, path)

    def test_modulesdependencies_exists(self):
        '''
        '''
        path = "tests/graphmanifests/a"
        ret = modules.moduledependencies(path)
        self.assertListEqual(["base"], ret)
        path = "tests/graphmanifests/c"
        ret = modules.moduledependencies(path)
        self.assertListEqual(["b","a"], ret)

    def test_modulesdependencies_empty(self):
        '''
        '''
        path = "tests/graphmanifests/d-no-dependency"
        ret = modules.moduledependencies(path)
        self.assertListEqual([], ret)
        path = "tests/graphmanifests/e-no-depends-key"
        ret = modules.moduledependencies(path)
        self.assertListEqual([], ret)

    def test_dependency_dictgraph_known(self):
        '''
        '''
        paths = [
            "tests/graphmanifests/a",
            "tests/graphmanifests/b",
            "tests/graphmanifests/c",
            "tests/graphmanifests/d-no-dependency",
            "tests/graphmanifests/e-no-depends-key"
        ]
        ret = modules.dependency_dictgraph(paths)
        expected = {'a':{"base"},'b':{'a'},'c':{'b','a'},
                    'd-no-dependency':set(),
                    'e-no-depends-key':set()}
        self.assertDictEqual(expected, ret)
    def test_dependency_dictgraph_strict_no_missing(self):
        '''
        '''
        paths = [
            "tests/graphmanifests/a",
        ]
        ret = modules.dependency_dictgraph(paths,strict=True)
        expected = {'a':{"base"}}
        self.assertDictEqual(expected, ret)

    def test_dependency_dictgraph_strict_missing(self):
        paths = [
            "tests/graphmanifests/a",
            "this-path-is-missing/b"
        ]
        self.assertRaises(FileNotFoundError, modules.dependency_dictgraph,
                          paths, {'strict':True})
