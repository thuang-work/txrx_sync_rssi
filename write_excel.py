# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 16:47:16 2021

@author: thuang

Writes the results of a comparison to Excel.
"""

import openpyxl
import copy

class write_excel:
    
    def __init__(self, name_of_excel_file_without_xlsx, data_dict):
        """
        Parameters
        ----------
        name_of_excel_file : string
            Name of Excel file to write to.
        data_dict : dictionary
            A dictionary containing the data to write to the Excel file.
            Dictionary shall contain: {'names':[name1, name2], mode_id:{t1_blf:{'T1': t1, 'BLF': blf, 'name1':[1e3, 1e4], 'name2':[1e3, 1e4], 'delta':[1e3, 1e4]}}}
            
        Returns
        -------
        None.

        """
        self.name_of_excel_file = name_of_excel_file_without_xlsx+'.xlsx' #adds extension for you
        self.wb = openpyxl.Workbook()
        self.data_dict = data_dict.copy()

    def write_modes(self):
        """
        Writes the current sheet with data of all modes in data_dict
        """

        name1, name2 = self.data_dict['names']
        self.data_dict.pop('names', None)
        
        for mode_id in self.data_dict.keys():
        
            # create a sheet
            self.wb.create_sheet(title='mode '+str(mode_id))
            sheet = self.wb.get_sheet_by_name('mode '+str(mode_id))
            
            first_row = 1

            for t1_blf in self.data_dict[mode_id].keys():
                sheet['A'+str(first_row)] = 'T1'; sheet['B'+str(first_row)] = self.data_dict[mode_id][t1_blf]['T1']
                
                sheet['A'+str(first_row+1)] = 'BLF'; sheet['B'+str(first_row+1)] = self.data_dict[mode_id][t1_blf]['BLF']
                
                sheet['A'+str(first_row+2)] = 'sensitivity'; sheet['B'+str(first_row+2)] = '1.e-3'; sheet['C'+str(first_row+2)] = '1.e-4'
                
                sheet['A'+str(first_row+3)] = name1
                sheet['B'+str(first_row+3)] = self.data_dict[mode_id][t1_blf]['name1'][0]
                sheet['C'+str(first_row+3)] = self.data_dict[mode_id][t1_blf]['name1'][1]
    
                sheet['A'+str(first_row+4)] = name2
                sheet['B'+str(first_row+4)] = self.data_dict[mode_id][t1_blf]['name2'][0]
                sheet['C'+str(first_row+4)] = self.data_dict[mode_id][t1_blf]['name2'][1]        
    
                sheet['A'+str(first_row+5)] = 'delta'
                sheet['B'+str(first_row+5)] = self.data_dict[mode_id][t1_blf]['delta'][0]
                sheet['C'+str(first_row+5)] = self.data_dict[mode_id][t1_blf]['delta'][1]
                first_row += 7 
        
        self.wb.remove_sheet(self.wb.get_sheet_by_name('Sheet')) #remove the first sheet, as it's blank
        self.write_file()
        
    def write_file(self):
        """
        Write the Excel file.
        """
        self.wb.save(self.name_of_excel_file)