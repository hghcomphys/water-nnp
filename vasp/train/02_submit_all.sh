#!/usr/bin/env bash

echo "submit files..."
for n in $(seq 1 1 600)
do
    cd run$n
    cp ../cleanup.sh .
    cp ../submit_vasp.sh .
    cp ../INCAR .
    cp ../KPOINTS .
    cp ../POTCAR .
    #cp ../vdw_kernel.bindat .
    qsub submit_vasp.sh
    cd ..
done
echo "Done."
