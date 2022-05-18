# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:12:03 2021

@author: thuang

Plots the sensitivity delta = master_branch - my_branch
for 1e3 and 1e4.
"""

from matplotlib import pyplot as plt
import numpy as np

class delta_bars:
    
    def __init__(self, data_dict, tolerance):
        """
        Parameters
        ----------

        data_dict : dictionary
            A dictionary containing the data to write to the Excel file.
            Dictionary shall contain: {'names':[name1, name2], mode_id:{t1_blf:{'T1': t1, 'BLF': blf, 'name1':[1e3, 1e4], 'name2':[1e3, 1e4], 'delta':[1e3, 1e4]}}}
            
        Returns
        -------
        None.

        """
        self.data_dict = data_dict.copy()
        self.tolerance = tolerance
        
    def plot_delta(self):
        """
        Plots the delta for each scenario of each mode as a bar graph.
        """

        self.data_dict.pop('names', None)
        
        num_modes = len(self.data_dict) #number of modes
        num_cols = int(np.ceil(np.sqrt(num_modes))) #make the plot grid as square as possible to save space
        num_rows = num_cols
        fig1, *ax = plt.subplots(num_rows, num_cols)
        fig1.tight_layout()
        
        if num_cols*num_rows>1: #if only one axis, then can't flatten
            ax = ax[0].flatten('F')
        
        if num_modes < len(ax): #remove excess axes exceeding the number of plots
            for this_ax in ax[num_modes:]:
                this_ax.remove()
        
        for n, mode_id in enumerate(self.data_dict.keys()):
            labels = []
            delta_e3 = []
            delta_e4 = []
            for t1_blf in self.data_dict[mode_id].keys():
                labels += [self.data_dict[mode_id][t1_blf]['T1'] + ',' + self.data_dict[mode_id][t1_blf]['BLF']]
                delta_e3 += [self.data_dict[mode_id][t1_blf]['delta'][0]]
                delta_e4 += [self.data_dict[mode_id][t1_blf]['delta'][1]]
            ax[n].bar(np.arange(len(labels)), delta_e3, tick_label=labels, color='tab:blue', width=.25)
            ax[n].bar(np.arange(len(labels))+.25, delta_e4, tick_label=labels, color='tab:red', width=.25)
            ax[n].legend(['1e-3', '1e-4'], fontsize='xx-large')
            ax[n].grid(True, which='both', axis='both')
            ax[n].set_xlabel('T1, BLF', fontsize='xx-large')
            ax[n].set_ylabel(chr(916)+'sensitivity (dBm)', fontsize='xx-large')
            if (np.array(delta_e3) < -self.tolerance).any():
                ax[n].set_title(f'Mode {mode_id}', fontsize='xx-large', color='red')
            else:
                ax[n].set_title(f'Mode {mode_id}', fontsize='xx-large', color='green')
            ax[n].tick_params(axis='both', labelsize='xx-large')
            ax[n].minorticks_on()
