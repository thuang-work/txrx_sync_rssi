# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:09:44 2021

@author: thuang

compares sensitivity between the data in two folders.

Two branches

RF modes
T1: min, nom, max
LF: neg, nom, pos
sensitivity: 1e-3, 1e-4

"""
import numpy as np
from termcolor import colored
import warnings

def my_log_interp(y_pt, x, y):
    """
    Performs linear interpolation of BER curves, but unlike the one in numpy,
    this one scans the x-axis and finds the closest x, then moves back one point
    and performs interpolation.  This has the advantage that even if y=f(x) is not
    monotonically decreasing at lower BER, the x can still be computed.
    
    
    y_pt: float
        The f(x) for which x is sought, in linear unit.
    
    x: float
        x-axis in dBm representing input power
    
    y: float
        BER in linear scale
    
    """

    zero_idx = y==0 #throw out all the data points where no bit errors are found so can take log
    y = y[~zero_idx]
    x = x[~zero_idx]

    #sort by input power in ascending order, which is on the x-axis
    idx_sorted = np.argsort(x)
    x = x[idx_sorted]
    y = y[idx_sorted]

    idx_1 = next(best_y_idx for best_y_idx in range(len(y)) if y[best_y_idx] <= y_pt)

    x0, x1 = x[idx_1-1], x[idx_1]
    y0, y1 = np.log10(y[idx_1-1]), np.log10(y[idx_1])
    
    m = (y1-y0)/(x1-x0)
    b = y1-m*x1
    
    return (y_pt-b)/m
    

def _sensitivity_calc(data_obj):
    '''
    Computes the 1e-3 and 1e-4 sensitivity points.
    
    parameters
    ----------
    data_obj: ber_data instance
    
    return
    ------
    
    1e-3 point
    1e-4 point where available
    
    '''

    x = []
    y = []
    
    for k, v in data_obj.ber.items():
        x += [k]; y+=[v]

    x = np.array(x); y = np.array(y)
    
    zero_idx = y==0 #throw out all the data points where no bit errors are found so can take log
    y = y[~zero_idx]
    x = x[~zero_idx]

    if not np.all(np.diff(y) > 0): warnings.warn(f'Mode {data_obj.rf_mode} BER not monotonically decreasing with increasing input signal power level')

    idx_sorted = np.argsort(x)[::-1]
    x = x[idx_sorted]
    y = np.log10(y[idx_sorted])
    
    if y[0] <= 1.e-3:
        e_3 = np.interp(-3, y, x)
    if y[0] <= 1.e-4:
        e_4 = np.interp(-4, y, x)
        return e_3, e_4
    
    return (e_3,'--')

def sensitivities(*data_obj):
    
    sens_dict = {} #dictionary with sensitivity data
    
    for each_data_obj in data_obj:
        inner_key = each_data_obj.t1_time + '_' + each_data_obj.blf_err
        sens_dict.setdefault(each_data_obj.rf_mode, {})
        sens_dict[each_data_obj.rf_mode][inner_key] = _sensitivity_calc(each_data_obj)

    return sens_dict

def sens_disp(dict1, t1=['min','nom','max'], blf=['neg','nom','pos']):
    '''
    Displays the 1e-3 and 1e-4 sensitivity points. 
    
    parameters
    ----------
    
    dict1: dictionary
        Holds (1e-3, 1e-4) sensitivity numbers in dB

    t1: list
        T1 settings of sensitivity points to display.
    
    blf: list
        BLF error settings of sensitivyt points to display.

    '''
    
    for rf_mode in dict1.keys():
        print('___________________________')
        print(f'RF Mode: {rf_mode}')
        
        for each_t1 in t1:
          for each_blf in blf:
            t1_blf_key = each_t1+'_'+each_blf

            if rf_mode in dict1.keys():
                if t1_blf_key in dict1[rf_mode].keys():
                    e3_d1, e4_d1 = dict1[rf_mode][t1_blf_key]
                else:
                    e3_d1, e4_d1 = '--', '--'
                    continue
                
            print(f'T1: {each_t1}, BLF: {each_blf}')
            print('sensitivity: '.ljust(6), '1e-3'.ljust(7), '1e-4'.ljust(7))
            
            if e4_d1 == '--':
                print(f'{e3_d1:.2f}'.rjust(19), '---'.ljust(7))
            else:
                print(f'{e3_d1:.2f}'.rjust(19), f'{e4_d1:.2f}'.ljust(7))

def sens_comp(dict1, dict2, name1='data1', name2='data2', tolerance_db=.5, t1=['min','nom','max'], blf=['neg','nom','pos']):
    '''
    Compares two sensitivity dictionaries.
    
    parameters
    ----------
    
    dict1: dictionary
        Holds (1e-3, 1e-4) sensitivity numbers in dB
    
    dict2: dictionary
        Holds (1e-3, 1e-4) sensitivity numbers in dB
    
    name1: str
        Name of the first data set
    
    name2: str
        Name of the second data set
    
    tolerance_db: float
        Difference in sensitivity in dB beyond which an anomaly indicator would appear
    
    t1: list
        T1 settings for which comparisons are made
    
    blf: list
        BLF error settings for which comparisons are made
        
    '''
    
    t1_blf_semaphore = True
    
    all_rf_modes = set.union(set(dict1.keys()), set(dict2.keys())) #all the unique RF modes
    data_dict = {'names':[name1, name2]}
    
    for rf_mode in all_rf_modes:
        print('___________________________')
        print(f'RF Mode: {rf_mode}')
        
        for each_t1 in t1:
          for each_blf in blf:
            t1_blf_key = each_t1+'_'+each_blf

            if rf_mode in dict1.keys():
                if t1_blf_key in dict1[rf_mode].keys():
                    t1_blf_semaphore = True
                    e3_d1, e4_d1 = dict1[rf_mode][t1_blf_key]
                else:
                    t1_blf_semaphore = False
            else:
                t1_blf_semaphore = False
                e3_d1, e4_d1 = '--', '--'
                
            if rf_mode in dict2.keys():
                if t1_blf_key in dict2[rf_mode].keys():
                    t1_blf_semaphore = t1_blf_semaphore and True
                    e3_d2, e4_d2 = dict2[rf_mode][t1_blf_key]
                else:
                    t1_blf_semaphore = False
            else:
                t1_blf_semaphore = False
                e3_d2, e4_d2 = '--', '--'             
                
            if t1_blf_semaphore: #if both data sets have this combination of T1 and BLF fields for this RF mode
                print(f'T1: {each_t1}, BLF: {each_blf}')
                print('sensitivity: '.ljust(6), '1e-3'.ljust(7), '1e-4'.ljust(7))

                delta_e3 = e3_d1 - e3_d2
                delta_e3_color = 'green' if delta_e3 >= -tolerance_db else 'red'
                
                if e4_d1 == '--' or e4_d2 == '--':
                    print(f'{name1}: '.ljust(12), f'{e3_d1:.2f}'.ljust(7), '---'.ljust(7))
                    print(f'{name2}: '.ljust(12), f'{e3_d2:.2f}'.ljust(7), '---'.ljust(7))                    
                    print('delta: '.ljust(12), colored(f'{delta_e3:.2f}'.ljust(7), delta_e3_color), '---'.ljust(7))
                else:
                    delta_e4 = e4_d1 - e4_d2
                    delta_e4_color = 'green' if delta_e4 >= -tolerance_db else 'red'
                    print(f'{name1}: '.ljust(12), f'{e3_d1:.2f}'.ljust(7), f'{e4_d1:.2f}'.ljust(7))
                    print(f'{name2}: '.ljust(12), f'{e3_d2:.2f}'.ljust(7), f'{e4_d2:.2f}'.ljust(7))    
                    print('delta: '.ljust(12), colored(f'{delta_e3:.2f}'.ljust(7), delta_e3_color), colored(f'{delta_e4:.2f}'.ljust(7), delta_e4_color))

                data_dict.setdefault(rf_mode, {})
                data_dict[rf_mode].setdefault(t1_blf_key, {'T1': each_t1, 
                                                           'BLF':each_blf, 
                                                           'name1':[e3_d1, e4_d1], 
                                                           'name2':[e3_d2, e4_d2],
                                                           'delta':[delta_e3, delta_e4]})
    return data_dict

if __name__ == '__main__':
    from summarize_data import ber_data_reader
    from plot_ber_delta import delta_bars
    from matplotlib import pyplot as plt
    # from write_excel import write_excel as we
    my_branch_dict = sensitivities(*ber_data_reader('test_data_all').read())
    master_branch_dict = sensitivities(*ber_data_reader('test_data').read())
    data_dict=sens_comp(master_branch_dict, my_branch_dict, name1='master', name2='mine', tolerance_db=.5)
    # write_workbook = we('comparisons', data_dict)
    # write_workbook.write_modes()
    #plt.close('all')
    #my_branch_dict = sensitivities(*ber_data_reader('test_data').read())
    #master_branch_dict = sensitivities(*ber_data_reader('test_data_master_mode_13').read())
    # data_dict=sens_comp(master_branch_dict, my_branch_dict, name1='master', name2='mine', tolerance_db=.5)
    # bars_inst=delta_bars(data_dict, tolerance=1.)
    # bars_inst.plot_delta()
    #plt.tight_layout()
    #sens_disp(my_branch_dict, t1=['min'], blf=['nom'])