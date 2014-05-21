#!/usr/bin/python
from __future__ import print_function, division
import unittest
from os.path import join
from .testingtools import data_dir
from nilmtk import Electricity, ElectricityMeter, HDFDataStore

class TestElectricity(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        filename = join(data_dir(), 'energy.h5')
        cls.datastore = HDFDataStore(filename)

    def test_wiring_graph(self):
        meter1 = ElectricityMeter(
            {'site_meter': True, 'dataset': 'REDD', 'building': 1, 'instance' :1})
        meter2 = ElectricityMeter(
            {'submeter_of': 1, 'instance': 2, 'dataset': 'REDD', 'building': 1})
        meter3 = ElectricityMeter(
            {'submeter_of': 2, 'instance': 3, 'dataset': 'REDD', 'building': 1})
        elec = Electricity([meter1, meter2, meter3])
        wiring_graph = elec.wiring_graph()
        
        self.assertIs(elec.mains(), meter1)
        self.assertEqual(elec.meters_directly_downstream_of_mains(), [meter2])
        

    def test_proportion_of_energy_submetered(self):
        meters = []
        for i in [1,2,3]:
            meter = ElectricityMeter()
            meter.load(self.datastore, key='/building1/electric/meter{:d}'.format(i))
            meters.append(meter)

        mains = meters[0]
        elec = Electricity(meters)
        self.assertEqual(elec.proportion_of_energy_submetered(), 1.0) 
    

if __name__ == '__main__':
    unittest.main()
