# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 12:00:31 2021

@author: thuang

Run this to show comparison between master branch and my branch
"""

from summarize_data import ber_data_reader
from plot_ber_delta import delta_bars
from sensitivity_comp import sensitivities, sens_comp
from matplotlib import pyplot as plt

master_branch_dict = sensitivities(*ber_data_reader('test_data_7_good').read())
my_branch_dict = sensitivities(*ber_data_reader('test_data').read())
data_dict=sens_comp(master_branch_dict, my_branch_dict, name1='master', name2='mine', tolerance_db=.5)
plt.close('all')
bars_inst=delta_bars(data_dict, tolerance=1.)
bars_inst.plot_delta()
#plt.tight_layout()