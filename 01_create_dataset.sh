#!/usr/bin/env bash

REF="reax"

echo "Generat initial dataset..."
rm -f lmp/*.out lmp/*.data

# lmp_serial < md.${REF}.in #> lmp/md.${REF}.out
mpirun -np 4 lmp_mpi < md.${REF}.in #> lmp/md.${REF}.out

cp lmp/${REF}.data lmp/${REF}.back.data
cp lmp/restart.data lmp/restart.back.data

echo "Convert LAMMPS to RuNNer file format..."
python lammps_to_runner.py lmp/${REF}.data lmp/input.data
