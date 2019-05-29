#!/usr/bin/env bash

REF="reax"

echo "Running MD using NNP..."
rm -f lmp/nnp.data
lmp_serial < md.nnp.in #> lmp/md.nnp.$i.out

echo "Rerunning using ${REF}..."
lmp_serial < rerun.${REF}.in #> lmp/rerun.${REF}.$i.out

echo "Converting LAMMPS to RuNNer file format..."
python lammps_to_runner.py lmp/${REF}.data lmp/input.data