#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 01:06:13 2022

@author: Simon Rundstedt
"""
#%%

import os
import unittest

# Note non-relative import. The unittest module will take care of import from
# project root
from odootools import config

#%%

TESTDIR = os.path.dirname(__file__)

#%%
class TestConfig(unittest.TestCase):
    '''
    '''
    def test_test_handle_core(self):
        '''
        Test the test handle used for other tests.
        '''
        handle = config.load(os.path.join(TESTDIR, 'test_handle.ini'))
        self.assertEqual(handle.user, "odoo")
        self.assertEqual(handle.group, "odoo")
        self.assertEqual(handle.filestore, "/var/lib/odoo/.local/share/Odoo/filestore/")
        self.assertEqual(handle.conf, "/etc/odoo/odoo.conf")
        self.assertEqual(handle.coredir, "tests/testdirs/core")

    def test_test_handle_addons(self):
        '''
        Test the test handle used for other tests.
        '''
        handle = config.load(os.path.join(TESTDIR, 'test_handle.ini'))
        alist = "tests/testdirs/addons1,tests/testdirs/addons2,tests/testdirs/addons3".split(",")
        self.assertListEqual(handle.addonsdirs,alist)
        plist = "odoo-,odooext-".split(",")
        self.assertListEqual(handle.addonsprefixes,plist)
        