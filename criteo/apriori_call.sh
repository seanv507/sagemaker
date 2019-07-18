#!/bin/sh -x
time ./apriori -tc -m2 -n5 -s-200 \
  /home/sviolante/projects/criteo/train_4000000.txt.frq \
  /home/sviolante/projects/criteo/train_4000000.txt.frq.res200 \
  2>&1 | tee apriori_200.log
#  "/media/sviolante/My Book/sean/projects/criteo/data/input/train_4000000.txt.frq" \
#  "/media/sviolante/My Book/sean/projects/criteo/data/input/train_4000000.txt.frq.res2" \
