#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def gen_vw(input_file, output_file, ln_transform=False):
    with open(output_file, 'w') as o_f:
        for l in open(input_file):

            z = l.split('\t')
            tgt = int(z[0]) * 2 - 1
            if ln_transform:
                ints = np.log(pd.to_numeric(pd.Series(z[1:14]),errors='coerce')
                              + 3.0)
            else:
                ints = z[1:14]
            ints = z[1:14]

            cats = z[14:]  # newline preserved
            new_l = (str(tgt) +
                     ' |I ' + ' '.join(ints) +
                     ' |C ' + ' '.join(cats))

            ints = ' '.join(['|{} I{:02d}:{}'.format(
                             chr(ord('a') + i), i, ints[i])
                             for i in range(len(ints))])
            cats = ' '.join(['|{} C{:02d}:{}'.format(
                             chr(ord('A') + i), i, cats[i])
                             for i in range(len(cats))])

            new_l = (str(tgt) + ' ' + ints + cats)

            o_f.write(new_l)
