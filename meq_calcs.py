# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:50:06 2021

@author: Michael J. Murphy
"""
# Calculate meq/L for Stiff diagrams

import pandas as pd

class MeqCalc:
    
    def __init__(self, data):
        self.data = data
        self.df1 = pd.read_excel(self.data, engine='openpyxl') # All data
        self.df2 = self.df1[["LocCode", "Field_ID", "Sampled_Date-Time", "ChemName", "Conc_num"]] # Required columns
        self.chems = sorted(self.df2.ChemName.unique().tolist()) # Expected analytes and sorting: ['Alkalinity (Bicarbonate)','Calcium','Chloride','Magnesium','Potassium','Sodium','Sulfate']
        
    def calc_meq(self, ions = ["HCO3-", "Ca++", "Cl-", "Mg++", "Na+ + K+", "Na+ + K+", "SO4--"], charges = [-1, 2, -1, 2, 1, 1, -2],
                 molar_masses = [61.0168, 40.078, 35.453, 24.305, 39.0983, 22.99, 96.06]):
        chems = self.chems
        chem_zip = zip(chems, charges, molar_masses, ions)
        # Write mass charge to dataframe for conversion to meq/L
        self.df2["mass_charge"] = 0
        self.df2["meq/L"] = 0
        self.df2["ion"] = ''
        for chem, charge, mass, ion in chem_zip:
            self.df2.loc[self.df2.ChemName==chem, 'mass_charge'] = mass / charge
            self.df2.loc[self.df2.ChemName==chem, "meq/L"] = self.df2.Conc_num / self.df2.mass_charge
            self.df2.loc[self.df2.ChemName==chem, "ion"] = ion
        self.df2["key"] = self.df2["LocCode"] + "_" + self.df2["ChemName"]
        return self.df2
    
    def compare_samples(self, data_pre):
        self.data_pre = data_pre 
        _df_new = self.calc_meq() # New data to compare to previous
        _meq_pre = MeqCalc(self.data_pre)
        _meq_pre.calc_meq()
        _df_pre = _meq_pre.df2 # Previous data
        # Test to make sure data is called in correct order
        if not _df_pre["Sampled_Date-Time"].max() < _df_new["Sampled_Date-Time"].max():
        
            raise Exception("Data frames are not in correct order; call 'new' data first, old data in compare_samples()")
            
        df_joined = _df_new.merge(_df_pre, on="key", how ="inner", suffixes=('_new', '_old'))
        df_joined["percent_change"] = ((df_joined["meq/L_new"].abs() - df_joined["meq/L_old"].abs()) / df_joined["meq/L_old"].abs())*100
        return df_joined
    
    def report(self, data_pre, project="test"):
        _df_rpt = self.compare_samples(data_pre)
        _df_rpt = _df_rpt[["LocCode_new", "ChemName_new", "ion_new", "Sampled_Date-Time_new", "meq/L_new", "Sampled_Date-Time_old", "meq/L_old", "percent_change"]]
        _date_from = _df_rpt["Sampled_Date-Time_old"].min().strftime('%b_%y')
        _date_to = _df_rpt["Sampled_Date-Time_new"].max().strftime('%b_%y')
        _df_rpt.columns = ["Location", "Chemical Name", "Ion", "Sampled Date, Current Quarter", "Ionic Charge Concentration, Current Quarter (meq/L)", "Sampled Date, Previous Quarter",
                           "Ionic Charge Concentration, Previous Quarter (meq/L)", "Percent Change in Charge Concentration"]       
        _writer = pd.ExcelWriter(project + "_ion_summary_" + _date_from + "_to_"+ _date_to + ".xls")
        _df_rpt.to_excel(_writer)
        _writer.save()
        
        return _df_rpt
        
        
        
        
        
        
        
        

    