#!/bin/bash


#PBS -q q1h

#PBS -N water-vasp

#PBS -l walltime=01:00:00

#PBS -l nodes=1:ppn=20

#PBS -l mem=50GB

#PBS -o stdout

#PBS -e stderr


cd $PBS_O_WORKDIR

echo "Job started:" '/bin/date's


#module purge
module load VASP

cd $PBS_O_WORKDIR

mpd > mpd.out &

sleep 5s

mpirun -np 20 vasp_gam #>> log.vasp.out
sh cleanup.sh

echo .Job finished: . `/bin/date`
