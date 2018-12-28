#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 23:41:03 2018

@author: sviolante
"""
import os
import re
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import criteo

sns.set(style="ticks")


fil ='data/input/train.txt'
fil_short = 'data/input/train_4000000.txt'
fil_short_vw = 'data/train/train_4000000.vw'
vw_path = 'data'
criteo.gen_vw(fil_short, fil_short_vw, True)

nint=13
ncat=26
dat = pd.read_csv(fil_short,sep='\t', nrows=1000000,
                  header=None,
                  names = ['click'] + [f'I{i:02d}' for i in range(nint)]
                  + [f'C{i:02d}' for i in range(ncat)])


plt.subplot(3,5,1)
dat['I01'].hist(by=dat.click,bins=20)
dat[['click','I01']].assign(ln01=lambda x:np.log(x['I01'])).boxplot(by='click',sharex=False)


categs = ['C{:02d}'.format(c) for c in range(ncat)]
ints = ['I{:02d}'.format(c) for c in range(nint)]

def calc_cats(ser_cat):
    v = ser_cat.value_counts().rename('counts').to_frame()
    v['cumsum'] = v.counts.cumsum()
    v['cumfreq'] = v['cumsum']/v['cumsum'].iloc[-1]
    return v

b = {}
freqs = [.50,.75,.9,.95, 1]
for c in categs:
    v = calc_cats(dat[c])

    b[c] = pd.Series(v.cumfreq.searchsorted(freqs),index=freqs,name=c)
res = pd.concat(b, axis=1)


dat[ints].describe()
import matplotlib.pyplot as plt
f, axes = plt.subplots(4, 4)
axes_flat = [a for ax in axes for a in ax]
for i, col in enumerate(ints):
    (dat[[col]]
     .apply(lambda x: np.log(x+3) )
     .boxplot(ax=axes_flat[i]))

    axes_flat[i].set_title('log(' + col + ' + 3)')


def create_vw_metrics_res():
    metric_res = [
            'passes used = (\d+)',
            'number of examples per pass = (\d+)',
            'average loss = ([-.0-9]+)',
            'best constant = ([-.0-9]+)',
            "best constant's loss = ([-.0-9]+)",
            'total feature number = (\d+)'
    ]

    df = pd.DataFrame({'re_s': metric_res})
    df['re'] = df.re_s.apply(lambda x: re.compile(x))
    df['col'] = df.re_s.str.split(' =', 1).str[0]
    df = df.set_index('col')
    return df


df_metric_res = create_vw_metrics_res()


def extract_vw_results(df, results_col='results'):
    ext = get_results_ext(results_col)
    for i in df.index:
        for i_re in df_metric_res.index:
            res = df_metric_res.loc[i_re, 're'].search(df.loc[i, results_col])
            if res:
                df.loc[i, i_re + ext] = np.float(res.group(1))



def create_cmd(dic):
    vw_cmd = 'vw ' + ' '.join(['--{} {}'.format(k, v) for k, v in vw_params.items()])
    return vw_cmd

op = subprocess.check_output(vw_cmd,shell=True, cwd=vw_path,
                                 stderr=subprocess.STDOUT).decode('utf-8')

vw_params={
    'data': fil_short_vw,
    'cache': ' ',
    'holdout_after': 3000000,
    'passes': 1000,
    'early_terminate': 15,
    'l2': 0,
    'l1': 0,
    'loss_function': 'logistic'
    }


results=[]
l2s = [0, 1e-2, 1e-4, 1e-6, 1e-8]
for var in l2s:

    vw_params={
        'data': fil_short_vw,
        'cache': ' ',
        'holdout_after': 3000000,
        'passes': 1000,
        'early_terminate': 15,
        'stage_poly': ' ',
        'l2': var,
        'l1': 0,
        'loss_function': 'logistic'

        }
    vw_cmd = create_cmd(vw_params)
    op = subprocess.check_output(vw_cmd,shell=True, cwd=vw_path,
                                 stderr=subprocess.STDOUT).decode('utf-8')
    res = vw_params.copy()
    res['results'] = op
    for r in df_metric_res.index:
        res[r] = float(df_metric_res.loc[r, 're'].search(op).group(1))
    print(var, res['average loss'])
    results.append(res)


