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

    def test_list_non_found(self):
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

    def test_list_prefix_nbr_of_entries(self):
        '''
        '''
        with open(os.path.join(TESTDIR,"test_modules_01_list_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            t_nbr_lines = len(list(filter(None,tlines)))
        self.assertEqual(len(modules.listmodules(self.handle)),t_nbr_lines)


    def test_list_prefix(self):
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
        
    def test_list_no_prefix(self):
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

    def test_list_no_core(self):
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
    
    def test_list_only(self):
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
        
    def test_list_dublicates_keys(self):
        '''
        '''
        keys = ["module1","module2"]
        flines = modules.listmodules(self.handle,includecore=False)
        fdub = modules.listduplicates(flines)
        for k in fdub:
            self.assertTrue(k in keys)

    def test_list_dublicates_paths(self):
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