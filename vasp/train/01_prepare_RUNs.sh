#!/usr/bin/env bash

echo "NNP-Convert..."
nnp-convert poscar H O > /dev/null

echo "Script files..."
for n in $(seq 1 1 600)
do
    rm -rf run$n
    mkdir run$n
    cd run$n
    # cp ../cleanup.sh .
    # cp ../submit_vasp.sh .
    # cp ../INCAR .
    # cp ../KPOINTS .
    # cp ../POTCAR .
    mv ../POSCAR_$n POSCAR
    cd ..
done
rm -f POSCAR_*
rm -f RUN.zip
zip -r RUN.zip run*
rm -rf run*

echo "Done."
