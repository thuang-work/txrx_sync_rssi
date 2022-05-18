# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 16:02:15 2021

@author: thuang

Does the difference in RSSI values between the signal and noise increase or decrease with less attenuation?
"""
import numpy as np

rssi_delta = 100
n_samps = 1000
rssi1_base = 960

atten = 10**(-np.arange(0, 6, .5)/20)
rssi1_amp = 960*atten
rssi0_amp = (rssi1_base + rssi_delta)*atten

for n, this_atten in enumerate(atten):
    print(f'atten: {20*np.log10(atten[n]):.2f} dB, {rssi0_amp[n]-rssi1_amp[n]:.2f}')


#delta btw. RSSI0 and RSSI1 decreases when attenuation increases because with
#higher attenuation, signal power is reduced relative to noise power, which
#remains constant.  Therefore, signal+noise is mostly noise.
