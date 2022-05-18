# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:44:37 2021

@author: thuang

Script to summarize and visualize data collected for TXRX sync work.
"""
import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
from termcolor import colored

class ber_data:
    
    def __init__(self, name_of_data):
        '''
        Data object storing data collected in a BER test as read from a CSV file.
        The BER for each power level is stored in the ber dictionary, with
        the power level in dB as key and the BER as value.
        '''
        self.name_of_file = name_of_data
        self.rf_mode = 11
        self.t1_time = 'nom'
        self.freq_mhz = 902.75
        self.blf_err = 'neg'
        self.tx_power_dbm = 30
        self.region = 'fcc'
        self.end_to_end_loss = 78.18
        self.ber = dict()
        self.per = dict()
        self.rssi = dict()
        self.t1_rssi = dict()
    
class ber_data_reader:
    '''
    Produces data objects holding information about a BER test.
    '''
    def __init__(self, folder_name):
        '''
        Name of folder where data is stored.  All CSV files within will be read.
        '''
        
        self.folder_name = folder_name
        
    def read(self):
        '''
        Reads all the CSV files in folder and returns data objects. 
        '''
        files = next(os.walk(self.folder_name))[2]
        all_data = []
        
        for file_name in files:
            if '.csv' in file_name:
                all_data += [self._read_pandas(file_name)]
        
        return all_data
        
    def _read_pandas(self, file_name):
        '''
        Read a CSV file in as Pandas.
        '''
        dtype_dict = {'test_comment': str,
                      'rf_mode': float,
                      'freq_mhz': float,
                      't1_time': str,
                      'blf_err': str,
                      'tx_power': int,
                      'region': str,
                      'bits/packet': int,
                      'packets': int,
                      'end_to_end_loss': float,
                      'delayed': bool,
                      'delayed_reply': bool,
                      'delimiter_only': bool,
                      'timestamp': int,
                      'attenuation': float,
                      'residue_i': int,
                      'residue_q': int,
                      'cdac_i': int,
                      'cdac_q': int,
                      'packet_num': int,
                      'rssi': int,
                      'rf_phase': int,
                      'n_bit_err': int,
                      'rx_bits': str,
                      'tx_bits': str,
                      'xor_bits': str,
                      'dft_peak': bool,
                      'dft_preamble_detected': bool,
                      'agc_y_expo': int,
                      'agc_y_mant': int,
                      'dft_peak_bin': int,
                      'pmf_eop_idx': int,
                      'slot_num': int,
                      'bd_pm_max': int,
                      'bd_pm_min': int,
                      't1_rssi': int,
                      'pmf_eop_val': int,
                      'dft_peak_mag': int,
                      'dft_preamble_detect_idx': int,
                      'tx_start': int,
                      'rx_stop': int}
        
        data_obj = ber_data(file_name)
        data_pd = pd.read_csv(self.folder_name+"/"+ file_name, header=0, dtype=dtype_dict) #read CSV into Pandas DF, with first row as field names
        data_obj.rf_mode = int(data_pd['rf_mode'].iloc[0])
        data_obj.t1_time = data_pd['t1_time'].iloc[0]
        data_obj.freq_mhz = data_pd['freq_mhz'].iloc[0]
        data_obj.tx_power_dbm = data_pd['tx_power_dbm'].iloc[0]
        data_obj.region = data_pd['region'].iloc[0]
        data_obj.end_to_end_loss = data_pd['end_to_end_loss'].iloc[0]
        data_obj.blf_err = data_pd['blf_err'].iloc[0]
        
        for atten in data_pd['attenuation'].unique():
            rx_pow = data_obj.tx_power_dbm - data_obj.end_to_end_loss - atten*2. #atten is applied twice in a roundtrip
            filter_ = data_pd['attenuation']==atten
            data_obj.ber[rx_pow] = data_pd[filter_]['n_bit_err'].sum()/data_pd[filter_]['bits/packet'].sum()
            data_obj.per[rx_pow] = len(data_pd[filter_].query('n_bit_err>0'))/len(data_pd[filter_])
            data_obj.rssi[rx_pow] = data_pd[filter_]['rssi']
            data_obj.t1_rssi[rx_pow] = data_pd[filter_]['t1_rssi']
        return data_obj

def visualize_ber_curves(*data):
    
    all_data_dict = dict()
    
    for each_data in data:
        all_data_dict.setdefault(each_data.rf_mode, [])
        all_data_dict[each_data.rf_mode]+=[each_data]
    
    for each_data_dict in all_data_dict.values():
        _visualize_ber_curves_plotter(*each_data_dict)
        plt.show()
def _visualize_ber_curves_plotter(*data_obj):
    plt.figure(f'RF mode: {data_obj[0].rf_mode}')
    plt.title(f'RF mode: {data_obj[0].rf_mode}')
    plt.grid(True, which='both', axis='both')
    legend = []
    
    for each_data in data_obj:
        rx_pow = each_data.ber.keys()
        ber = [each_data.ber[k] for k in rx_pow]
        plt.semilogy(rx_pow, ber)
        legend += ['t1: '+each_data.t1_time+' '+'LF err: '+each_data.blf_err]

    plt.legend(legend, fontsize='xx-large')
    plt.xlabel('power at antenna input (dBm)',fontsize='xx-large')
    plt.ylabel('BER (dB)',fontsize='xx-large')
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')

def visualize_rssi_one(*data_obj, rf_mode, t1_time, blf_err):
    '''
    Visualizes one RF mode.
    
    rf_mode : int
        RF mode
    
    t1_time : str
        'min', 'nom' or 'max'
    
    blf_err : str
        'neg', 'nom or 'pos''
    '''
    
    all_data_dict = dict()
    
    for each_data in data_obj:
        all_data_dict.setdefault(each_data.rf_mode, [])
        all_data_dict[each_data.rf_mode]+=[each_data]
    
    for each_data in all_data_dict[rf_mode]:
        if each_data.blf_err == blf_err and each_data.t1_time == t1_time:
            visualize_rssi(each_data)

def visualize_rssi(*data_obj):
    '''
    Produces the RSSI histograms of data_obj.  Each data_obj in *data_obj
    is used to produce one set of histogram.  
    
    data_obj: ber_data
    '''
    for each_data in data_obj:
        rx_pow = each_data.rssi.keys()
        
        max_rows = 3 # not more than 5 plots per column
        max_cols = 5
        n_cols = int(np.ceil(len(rx_pow)/max_rows))
        #n_rows = len(rx_pow) if len(rx_pow) < max_rows else max_rows
        if len(rx_pow) < max_rows:
            n_rows = len(rx_pow)
        else:
            n_rows = len(rx_pow) if len(rx_pow) < max_rows else max_rows

        if n_cols > max_cols:
            n_cols = max_cols

        fig, *ax = plt.subplots(n_rows, n_cols)
        fig.canvas.manager.set_window_title(f'Mode {each_data.rf_mode} T1: {each_data.t1_time}, LF : {each_data.blf_err}') 
        fig.tight_layout()
        #fig.subtitle(f'Mode {each_data.rf_mode} T1: {each_data.t1_time}, LF : {each_data.blf_err}', fontsize=16)
        
        if len(ax[0]) > 1:
            ax = ax[0].flatten('F')
        
        for this_ax in ax[len(rx_pow):]:
            this_ax.remove()
            
        for n, each_pow in enumerate(sorted(rx_pow)[:n_cols*n_rows]):
            ax[n].grid(True, which='both', axis='both')
            ax[n].hist(each_data.rssi[each_pow], alpha=.7,color='blue') #post-T1 RSSI (RSSI0)
            ax[n].hist(each_data.t1_rssi[each_pow], alpha=.7,color='red') #pre-T1 RSSI (RSSI1)
            ax[n].set_xlabel('RSSI value', fontsize='xx-large')
            ax[n].set_ylabel('count', fontsize='xx-large')
            ax[n].tick_params(axis='both', which='both', labelsize=15)
            ax[n].set_title(f'{each_pow} dB input power', fontsize='xx-large')
            ax[n].legend(['post-T1 rssi', 'pre-T1 rssi'], fontsize='xx-large')
            ax[n].minorticks_on()
            if n > 25: # limit the maximum number of plots to 25 or else will crowd out the canvas
                break
        
        plt.show()

def _check_rssi_one(data_obj):
    '''
    Processes one single data_obj only.
    Checks the point estimate of each pre-T1 RSSI reading per input power, and checks that it does not
    move with changing input power.

    delta_n is an indicator of how well the pre-T1 RSSI fits to the regression line.

    delta is the difference between the first and final values of the pre-T1 regression line.  
    This use used to gauge whether the line is sloped.  This is used instead of m, the slope of the fitted line
    because this value corresponds to the movement of the first and final pre-T1 RSSI histograms.
    The pre-T1 RSSI should not move with input power as it measures noise power only.

    pre_post_delta is the difference in RSSI values between the pre- and post-T1 RSSI.  The post-T1 RSSI should always 
    be higher as the pre-T1 RSSI is noise only while the post-T1 RSSI is noise + packet signal.
    '''

    pre_t1_rssi_mean = []
    post_t1_rssi_mean = []
    rx_pow = data_obj.rssi.keys()
    sorted_pow = sorted(rx_pow)
    pre_t1_rssi_mean = np.array([np.mean(data_obj.t1_rssi[this_pow]) for this_pow in sorted_pow])
    post_t1_rssi_mean = np.array([np.mean(data_obj.rssi[this_pow]) for this_pow in sorted_pow])

    n = np.arange(len(pre_t1_rssi_mean))
    m, b = np.polyfit(n, pre_t1_rssi_mean, 1) #fitted line
    ref_line = n*m+b #y of fitted line
    delta_n = pre_t1_rssi_mean - ref_line #each individual versus the fitted line
    delta = m*n[-1] # end of fitted line - start of fitted line
    pre_post_delta = pre_t1_rssi_mean - post_t1_rssi_mean #check if the pre-T1 RSSI has ever exceded the post-T1 RSSI
    return sorted_pow, delta, delta_n, pre_post_delta
        
def check_rssi(*data_obj, t1=['min','nom','max'], blf=['neg','nom','pos'],tolerance = 50.):
    '''
    Checks one RF mode for RSSI anomalies.
    
    rf_mode : int
        RF mode
    
    '''
    
    all_data_dict = dict()
    
    for each_data in data_obj:
        all_data_dict.setdefault(each_data.rf_mode, [])
        all_data_dict[each_data.rf_mode]+=[each_data]
    
    for rf_mode in all_data_dict.keys():
        print('___________________________')
        print(f'RF mode: {rf_mode}')
        for each_data in all_data_dict[rf_mode]:
            if each_data.blf_err in blf and each_data.t1_time in t1: #show only the T1 and BLF error settings requested
                rx_pow, delta, delta_n, pre_post_delta=_check_rssi_one(each_data)
                print(f'T1: {each_data.t1_time}, BLF: {each_data.blf_err}')
                print('Pow (dBm)'.ljust(12), 'delta_n'.ljust(12), 'pre-post delta'.ljust(12))
                for each_rx_pow, each_delta_n, each_pre_post in zip(rx_pow, delta_n, pre_post_delta):
                    delta_n_color = 'red' if abs(each_delta_n) > tolerance else 'green'
                    pre_post_color = 'red' if each_pre_post > 0 else 'green'
                    print(f'{each_rx_pow:.2f}'.ljust(12), colored(f'{each_delta_n:.2f}'.ljust(12), delta_n_color), colored(f'{each_pre_post:.2f}'.ljust(12), pre_post_color))
                delta_color = 'red' if abs(delta) > tolerance else 'green'
                print('delta:'.ljust(12), colored(f'{delta:.2f}'.ljust(12),delta_color))

def check_rssi_brief(*data_obj, tolerance = 50):
    '''
    Checks all the data_obj and briefly shows the results for pass/fail status.
    '''
    all_data_dict = dict()
    
    for each_data in data_obj:
        all_data_dict.setdefault(each_data.rf_mode, [])
        all_data_dict[each_data.rf_mode]+=[each_data]
    
    for rf_mode in all_data_dict.keys():
        print('___________________________')
        print(f'RF mode: {rf_mode}')
        for each_data in all_data_dict[rf_mode]:
            rx_pow, delta, delta_n, pre_post_delta=_check_rssi_one(each_data)
            print(f'T1: {each_data.t1_time}, BLF: {each_data.blf_err}')
    
            delta_n_pf = colored('fail'.ljust(12), 'red') if any(abs(delta_n) > tolerance) else colored('pass'.ljust(12), 'green')
            print('delta_n:'.ljust(12), delta_n_pf)
            
            delta_pre_post_pf = colored('fail'.ljust(12), 'red') if any(pre_post_delta > 0) else colored('pass'.ljust(12), 'green')
            print('pre-post:'.ljust(12), delta_pre_post_pf)
            
            delta_color = 'red' if abs(delta) > tolerance else 'green'
            print('delta:'.ljust(12), colored(f'{delta:.2f}'.ljust(12),delta_color))

if __name__ == '__main__':
    #plt.close('all')
    DUT = ber_data_reader('test_data')
    all_data = DUT.read()
    # check_rssi(*all_data)
    # visualize_ber_curves(*all_data)
    #visualize_rssi_one(*all_data,  rf_mode = 120, t1_time = 'max', blf_err = 'pos')
    #visualize_rssi_one(*all_data,  rf_mode = 120, t1_time = 'min', blf_err = 'nom')
    #visualize_rssi_one(*all_data,  rf_mode = 224, t1_time = 'max', blf_err = 'nom')
    #visualize_rssi(*all_data)
    check_rssi_brief(*all_data, tolerance=50)
  