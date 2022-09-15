#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 14:01:50 2022

@author: Simon Rundstedt
"""
#%% 
import unittest

import os
import sys

import networkx as nx
# Note non-relative import. The unittest module will take care of import from
# project root
from odootools import config
from odootools import modules

from graph import graph

#%%
TESTDIR = os.path.dirname(__file__)

class TestGraph(unittest.TestCase):
    '''
    '''
    def assertDiGraphEquals(self,g1,g2,msg=None):
        '''
            Test if nodes and egdes differs.
        '''
        # TODO : Add type test.
        nodes_1 = g1.nodes - g2.nodes
        edges_1 = g1.edges - g2.edges
        nodes_2 = g2.nodes - g1.nodes
        edges_2 = g2.edges - g1.edges
        standardMsg = "Graphs not equal. "\
        "Unique to G1; Nodes: {} Edges: {} "\
        "Unique to G2; Nodes: {} Edges: {}"
        if nodes_1 or nodes_2 or edges_1 or edges_2:
            s = standardMsg.format(nodes_1, edges_1, nodes_2, edges_2)
            self.fail(self._formatMessage(msg, s))
    def setUp(self):
        '''
        '''
        self.handle = config.load(os.path.join(TESTDIR,
                                               'test_handle_graph.ini'))      
    def init_dummy_graph_01_no_core(self):
        '''
        Dummy graph as represented by the graphmanifest test files.
        Excluding core
        '''
        dg = nx.DiGraph()
        dg = nx.DiGraph()
        dg.add_node("a")
        dg.add_edge("b","a")
        dg.add_edge("c","a")
        dg.add_edge("c","b")
        dg.add_edge("c","a")
        dg.add_node("d-no-dependency")
        dg.add_node("e-no-depends-key")
        return dg

    def init_dummy_graph_02_core(self):
        '''
        Dummy graph as represented by the graphmanifest test files.
        Including core
        '''
        dg = self.init_dummy_graph_01_no_core()
        dg.add_edge("a","base")
        return dg

    def init_dummy_graph_03_flatten_core(self):
        '''
        Dummy graph as represented by the graphmanifest test files.
        Including core
        '''
        dg = self.init_dummy_graph_01_no_core()
        dg.add_edge("a","core")
        return dg    

    def init_dummy_graph_04_flatten_exclude_list(self):
        '''
        Dummy graph as represented by the graphmanifest test files.
        Including core
        '''
        dg = self.init_dummy_graph_01_no_core()
        dg.add_edge("a","other")
        return dg
    
    def init_dummy_graph_05_addon_exclude_list(self):
        '''
        Dummy graph as represented by the graphmanifest test files.
        Including core
        '''
        dg = self.init_dummy_graph_01_no_core()
        dg.add_edge("a","addons") # Core module base sit in addons folder addons
        return dg    
    
    def test_graph_known_exclude_core(self):
        '''
        '''
        expected = self.init_dummy_graph_01_no_core()
        ret = graph.module_digraph(self.handle,core="exclude")
        self.assertDiGraphEquals(expected,ret)

    def test_graph_known_include_core(self):
        '''
        '''
        expected = self.init_dummy_graph_02_core()
        ret = graph.module_digraph(self.handle)
        self.assertDiGraphEquals(expected,ret)

    def test_graph_known_flatten_core(self):
        '''
        '''
        expected = self.init_dummy_graph_03_flatten_core()
        ret = graph.module_digraph(self.handle,core="flatten")
        self.assertDiGraphEquals(expected,ret)
        
    def test_module_digraph_from_paths_no_excludepaths(self):
        '''
        All dependencies read. Non excluded.
        '''
        paths = modules.listmodules(self.handle, includecore=False)
        expected = self.init_dummy_graph_02_core()
        ret = graph.module_digraph_from_paths(paths)
        self.assertDiGraphEquals(expected,ret)

    def test_module_digraph_from_paths_no_core_exclude(self):
        '''
        See if core-modules are removed from graph
        '''
        paths = modules.listmodules(self.handle, includecore=False)
        exclude_paths = modules.listcoremodules(self.handle)
        
        expected = self.init_dummy_graph_01_no_core()
        ret = graph.module_digraph_from_paths(paths,exclude_paths,
                                              excludepolicy="exclude")
        self.assertDiGraphEquals(expected,ret)
        
    def test_module_digraph_from_paths_no_core_flatten(self):
        '''
        See if core-modules are flattened to 'other'
        '''
        paths = modules.listmodules(self.handle, includecore=False)
        exclude_paths = modules.listcoremodules(self.handle)
        
        expected = self.init_dummy_graph_04_flatten_exclude_list()
        ret = graph.module_digraph_from_paths(paths,exclude_paths,
                                              excludepolicy="flatten")
        self.assertDiGraphEquals(expected,ret)
    
    def test_module_digraph_from_paths_no_core_addon(self):
        '''
        See if core-modules are flattened to their project name.
        '''
        paths = modules.listmodules(self.handle, includecore=False)
        exclude_paths = modules.listcoremodules(self.handle)
        
        expected = self.init_dummy_graph_05_addon_exclude_list()
        ret = graph.module_digraph_from_paths(paths,exclude_paths,
                                              excludepolicy="addon")
        self.assertDiGraphEquals(expected,ret)