'''
Created on Nov 23, 2010
author: gbowman

Adapted for msmbuilder.io by Robert McGibbon
September 15, 2012
'''

import numpy.testing as npt
import os
import os.path
import tables
import tempfile
import unittest

from msmbuilder import io

import numpy as np

class test_io(unittest.TestCase):
    def setUp(self):
        """setup() is called before very test and just creates a temporary work space for reading/writing files."""
        fid, self.filename1 = tempfile.mkstemp()
        fid, self.filename2 = tempfile.mkstemp()
        self.data = np.arange(10000, dtype=np.float32)

        #Write Data to an HDF5 file as a compressed CArray.
        hdfFile = tables.File(self.filename1, 'a')
        #The filter is the same used to save MSMB2 data
        hdfFile.createCArray("/", "arr_0", tables.Float32Atom(), self.data.shape, filters=io.COMPRESSION)
        hdfFile.root.arr_0[:] = self.data[:]
        hdfFile.flush()
        hdfFile.close()
        
    def test_load_1(self):
        "Load by specifying array name"
        TestData = io.loadh(self.filename1, 'arr_0')
        npt.assert_array_equal(TestData, self.data)
        
    def test_load_2(self):
        "load using deferred=False"
        TestData = io.loadh(self.filename1, deferred=False)['arr_0']
        npt.assert_array_equal(TestData, self.data)
    
    def test_load_2(self):
        "load using deferred=True"
        deferred = io.loadh(self.filename1, deferred=True)
        npt.assert_array_equal(deferred['arr_0'], self.data)
        deferred.close()
            
    def test_save(self):
        """Save HDF5 to disk and load it back up"""
        io.saveh(self.filename2, self.data)
        TestData = io.loadh(self.filename2, 'arr_0')
        npt.assert_array_equal(TestData, self.data)

    def teardown(self):
        os.remove(self.filename1)
        os.remove(self.filename2)


class test_io_int(test_io):
    "Run the same test as the class above, but using int64 data"
    def setUp(self):
        """setup() is called before very test and just creates a temporary work space for reading/writing files."""
        fid, self.filename1 = tempfile.mkstemp()
        fid, self.filename2 = tempfile.mkstemp()
        self.data = np.arange(10000, dtype=np.int64)

        #Write Data to an HDF5 file as a compressed CArray.
        hdfFile = tables.File(self.filename1, 'a')
        #The filter is the same used to save MSMB2 data
        hdfFile.createCArray("/", "arr_0", tables.Int64Atom(), self.data.shape, filters=io.COMPRESSION)
        hdfFile.root.arr_0[:] = self.data[:]
        hdfFile.flush()
        hdfFile.close()
    
if __name__ == "__main__":
    unittest.main()
