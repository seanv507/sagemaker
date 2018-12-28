#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
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
                             for i in range(len(ints)) if ints[i]])
            cats = ' '.join(['|{} C{:02d}=={}'.format(
                             chr(ord('A') + i), i, cats[i])
                             for i in range(len(cats)) if cats[i]])

            new_l = (str(tgt) + ' ' + ints + cats)

            o_f.write(new_l)


def parse_namespace(sect):
    feats = sect.split(' ')
    ns = feats[0]
    d_feat = {}
    for f in [g for g in feats[1:] if g]:

        feat_val = f.split(':')
        feat = feat_val[0]
        if len(feat_val) == 2:
            val = float(feat_val[1])
        else:
            val = True

        d_feat[feat] = val
    if ns:
        return {ns: d_feat}
    else:
        return d_feat


def vw_to_json(input_file, output_file, n_lines=None):
    with open(output_file, 'w') as o_f:
        for i_l, l in enumerate(open(input_file)):
            if n_lines and i_l > n_lines:
                return
            z = l.rstrip().split('|')
            labels = z[0].split(' ')
            tgt = int(z[0])
            _label = {}
            _label['Label'] = tgt
            if labels[-1]:
                _label['Tag'] = labels[-1]

            if len(labels) > 2:
                    _label['Weight'] = float(labels[2])

            if len(labels) > 3:
                _label['Base'] = float(labels[3])
            obj = {}
            obj['_label'] = _label

            for ns in z[1:]:
                dat = parse_namespace(ns)
                obj.update(dat)
            new_l = json.dumps(obj)
            o_f.write(new_l + '\n')
