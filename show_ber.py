# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 12:06:55 2021

@author: thuang

Run this to show the BER of a branch.
"""

from summarize_data import ber_data_reader
from sensitivity_comp import sensitivities, sens_disp
from matplotlib import pyplot as plt

master_branch_dict = sensitivities(*ber_data_reader('test_data_all').read())
sens_disp(master_branch_dict)