# criteo kaggle data set

Data Description

click / no click (downsampled) \t I1 - I13 \t C1 - C26
integers (counts) and categorical variables

 45,840,617 rows training data

% clicks

1. histogram of integers
1. correlation of integers
1. unique/frequency of vars

`vw_train_cmd = '../../vowpalwabbit/vw  -c -f model --bfgs --passes 30 -b 22 --loss_function logistic --l2 14 --termination 0.00001 --holdout_off'`

`vw_test_cmd = '../../vowpalwabbit/vw  -t -i model -p /dev/stdout'`

0.44463 top
0.476334 h using 4 million examples
0.46902 - public leaderboard


vw --data  *.vw -c --passes 30 --loss_function logistic
Num weight bits = 18
learning rate = 0.5
initial_t = 0
power_t = 0.5
decay_learning_rate = 1
using cache_file = train_4000000.vw.cache
ignoring text input in favor of cache input
num sources = 1
average  since         example        example  current  current  current
loss     last          counter         weight    label  predict features
0.693147 0.693147            1            1.0  -1.0000   0.0000       38
0.513320 0.333493            2            2.0  -1.0000  -0.9268       38
0.418169 0.323018            4            4.0  -1.0000  -0.9394       28
0.700157 0.982144            8            8.0   1.0000  -3.3240       34
0.720041 0.739925           16           16.0   1.0000  -1.6239       37
0.698286 0.676531           32           32.0   1.0000  -0.9542       33
0.612603 0.526920           64           64.0  -1.0000  -0.6251       38
0.613895 0.615188          128          128.0   1.0000  -0.5370       39
0.547826 0.481757          256          256.0  -1.0000  -1.1636       29
0.530550 0.513273          512          512.0  -1.0000  -0.1209       34
0.506617 0.482684         1024         1024.0   1.0000  -1.3084       38
0.491786 0.476954         2048         2048.0   1.0000  -0.9369       35
0.487708 0.483631         4096         4096.0   1.0000   0.3840       34
0.491222 0.494735         8192         8192.0  -1.0000  -0.9946       33
0.492804 0.494387        16384        16384.0  -1.0000  -3.2452       30
0.482383 0.471961        32768        32768.0   1.0000   2.3378       38
0.475640 0.468897        65536        65536.0   1.0000  -2.1086       38
0.475823 0.476006       131072       131072.0  -1.0000  -2.5150       38
0.491697 0.507571       262144       262144.0  -1.0000  -2.2976       37
0.495613 0.499529       524288       524288.0  -1.0000  -1.9382       35
0.489352 0.483090      1048576      1048576.0  -1.0000  -2.4924       39
0.482864 0.476375      2097152      2097152.0   1.0000  -0.5412       33
0.480493 0.480493      4194304      4194304.0  -1.0000  -1.4099       34 h
0.478361 0.476229      8388608      8388608.0  -1.0000  -1.3699       39 h
0.477975 0.477588     16777216     16777216.0   1.0000  -2.6853       33 h

finished run
number of examples per pass = 3600000
passes used = 5
weighted example sum = 18000000.000000
weighted label sum = -8956580.000000
average loss = 0.476334 h
best constant = -1.092190
best constant's loss = 0.563656
total feature number = 620269490

using l1 regularization = 1e-05
finished run
number of examples per pass = 3600000
passes used = 4
weighted example sum = 14400000.000000
weighted label sum = -7165264.000000
average loss = 0.550380 h

examples 4000000
average loss =0.526333 h
using l1 regularization = 1e-06
0.490010 h

1e-7 0.483320 h
1e-9 0.484436 h
1e-11 0.484450
0     0.484450 h






--examples can be used to split data ... (but then test set)
