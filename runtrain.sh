#!/usr/bin/env bash

clear
echo
echo "Water-NNP"
echo "============================="

if [ $1 -gt 0 ]
  then
    sh 01_create_dataset.sh
    sh 02_train_nnp.sh
fi

for i in $(seq 1 1 1)
do
    echo "-------------- ($i) ---------------"
    cp lmp/restart.{$i}000.data lmp/restart.data
    sh 03_extend_dataset.sh
    sh 02_train_nnp.sh
done
