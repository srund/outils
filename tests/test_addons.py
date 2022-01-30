#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 22:26:00 2022

@author: Simon Rundstedt
"""
#%%

import os
import sys

import unittest

# Note non-relative import. The unittest module will take care of import from
# project root
from odootools import config
from odootools import addons

#%%

TESTDIR = os.path.dirname(__file__)

class TestFindAddons(unittest.TestCase):
    '''
    '''
    def setUp(self):
        '''
        '''
        self.handle = config.load(os.path.join(TESTDIR, 'test_handle.ini'))

    def test_list_prefix(self):
        '''
        '''
        with open(os.path.join(TESTDIR,"test_addons_01_list_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = addons.listaddons(self.handle)
        flines.sort()
        self.assertListEqual(flines,tlines)

    def test_list_no_prefix(self):
        '''
        '''
        self.handle.addonsprefixes = None
        with open(os.path.join(TESTDIR,"test_addons_02_list_no_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = addons.listaddons(self.handle)
        flines.sort()
        self.assertListEqual(flines,tlines)

    def test_list_empty_prefix(self):
        '''
        '''
        self.handle.addonsprefixes = ['']
        with open(os.path.join(TESTDIR,"test_addons_02_list_no_prefix.txt")) as tfile:
            tlines = tfile.read().split('\n')
            tlines.sort()
            tlines = list(filter(None,tlines))
            #testdirs = os.path.join(TESTDIR,'testdirs')
            #tlines = [ testdirs+t for t in tlines ]
        flines = addons.listaddons(self.handle)
        flines.sort()
        self.assertListEqual(tlines, flines)

    def test_list_no_found(self):
        '''
        Test making sure the tests work.
        '''
        self.handle.addonsdirs = ["tests/testdirs/addons3"]
        self.assertListEqual([],addons.listaddons(self.handle))
