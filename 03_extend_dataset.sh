#!/usr/bin/env bash

REF="reax"

for j in $(seq 1 1 1)
do
  for n in $(seq 5 1 5)
  do
      cp lmp/restart.${n}000.data lmp/restart.data
      python rndgen.py

      echo "Run MD using NNP..."
      rm -f lmp/nnp.data
      # lmp_serial < md.nnp.in #> lmp/md.nnp.$i.out
      mpirun -np 4 lmp_mpi < md.nnp.in #> lmp/md.nnp.$i.out

      #echo "Rerun using ${REF}..."
      #lmp_serial < rerun.${REF}.in #> lmp/rerun.${REF}.$i.out
  done
done

echo "Convert LAMMPS to RuNNer file format..."
#python lammps_to_runner.py lmp/${REF}.data lmp/input.data
python lammps_to_runner.py lmp/nnp.data lmp/input.data
