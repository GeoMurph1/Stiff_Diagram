# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:25:56 2021

@author: Michael
"""
from meq_calcs import MeqCalc

data = 'Q4_stiff_data.xlsx'
data1 = 'Q3_stiff_data.xlsx'

# Test 1; basic functionality
test1 = MeqCalc(data)
test1.calc_meq()
print(test1.df2.head())
df_joined_test = test1.compare_samples(data1)
print(df_joined_test.head())

#Test 2; error catching (order error)
test2 = MeqCalc(data1)
test2.calc_meq()
print(test2.df2.head())
df_joined_test1 = test2.compare_samples(data)
print(df_joined_test.head())

# Test 3; test reporting
test3 = test1
test3.report(data1)