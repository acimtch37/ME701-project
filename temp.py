# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import csv

with open('output.csv', mode='w') as file:
    employee_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(['name', 'left slope', 'right slope', 'area', 'depth'])