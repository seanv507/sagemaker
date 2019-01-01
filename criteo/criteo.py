#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import numpy as np
import pandas as pd


def gen_vw(input_file, output_file, ln_transform=False):
    with open(output_file, 'w') as o_f:
        for i, l in enumerate(open(input_file)):
            if not i % 10000:
                print('line {}'.format(i))
            l_vw = gen_vw_line(l, ln_transform)
            o_f.write(l_vw)


def gen_vw_line(dat, ln_transform=False):
    scaling = [1.3862943611,
               2.277267285,
               1.7346010554,
               1.2039728043,
               2.9603517963,
               2.4277482359,
               1.7047480922,
               1.9459101491,
               2.2655438213,
               0.6931471806,
               1.0986122887,
               0.6931471806,
               1.2992829841]

    z = dat.rstrip('\n').split('\t')
    tgt = int(z[0]) * 2 - 1
    ints = z[1:14]
    if ln_transform:
        offset = np.ones((13,)) * 2
        offset[1] = 4
        ints = np.log(pd.to_numeric(pd.Series(ints), errors='coerce')
                      + offset) / scaling
        ints = ints.astype(str).replace('nan', '')
        # TODO format as
        # preserve sparsity, don't subtract mean
        # missing -> 0 [in vw] and 0-> ln(2 or 4)/scaling

    cats = z[14:]

    ints = ' '.join(['|{} I{:02d}:{:.6f}'.format(
                     chr(ord('a') + i), i, ints[i])
                     for i in range(len(ints)) if ints[i]])
    cats = ' '.join(['|{} C{:02d}=={}'.format(
                     chr(ord('A') + i), i, cats[i])
                     for i in range(len(cats)) if cats[i]])

    new_l = (str(tgt) + ' ' + ints + cats + '\n')
    return new_l


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
