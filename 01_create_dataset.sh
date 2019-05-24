#!/usr/bin/env bash

REF="reax"

echo "Generating initial dataset..."
rm -f lmp/*.out lmp/*.data
lmp_serial < md.${REF}.in #> lmp/md.${REF}.out
cp lmp/${REF}.data lmp/${REF}0.data
cp lmp/restart.data lmp/restart0.data

echo "Converting LAMMPS to RuNNer file format..."
python lammps_to_runner.py lmp/${REF}.data lmp/input.data
