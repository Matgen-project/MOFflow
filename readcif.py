#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : readcif.py
import math

def read_cif_file(cifname):
    ''' copy the cif information to a list'''
    cif_data = []
    with open(cifname) as f:
        try:
            for info_line in f:
                if len(info_line.strip()) != 0:
                        cif_data.append(info_line.strip())
        except:
            print('Error to open file:' + cifname)
            exit(0)
    return cif_data

def correct_value(value):
    global cvalue
    value = "".join(value)
    #print(value)
    if "(" in value:
        cvalue = float(value.split("(")[0])
    else:
        cvalue = float(value)
    #print(cvalue)
    return cvalue

def get_lattice(cif_data):
    ''' calculate the lattice constant'''
    for item in cif_data:
        if "_cell_length_a" in item:
            a = correct_value(item.split()[1])
            #a = item.split()[1]
        if "_cell_length_b" in item:
            b = correct_value(item.split()[1])
        if "_cell_length_c" in item:
            c = correct_value(item.split()[1])
        if "_cell_angle_alpha" in item:
            alpha = correct_value(item.split()[1]) / 180 * math.pi
        if "_cell_angle_beta" in item:
                beta = correct_value(item.split()[1]) / 180 * math.pi
        if "_cell_angle_gamma" in item:
            gamma = correct_value(item.split()[1]) / 180 * math.pi

    bc2 = b ** 2 + c ** 2 - 2 * b * c * math.cos(alpha)

    h1 = a
    h2 = b * math.cos(gamma)
    h3 = b * math.sin(gamma)
    h4 = c * math.cos(beta)
    h5 = ((h2 - h4) ** 2 + h3 ** 2 + c ** 2 - h4 ** 2 - bc2) / (2 * h3)
    h6 = math.sqrt(c ** 2 - h4 ** 2 - h5 ** 2)
    lattice = [[h1, 0., 0.], [h2, h3, 0.], [h4, h5, h6]]

    return lattice

if __name__ == '__main__':
    import sys
    args = sys.argv
    filename = args[1]
    data = read_cif_file(filename)
    print(get_lattice(data))