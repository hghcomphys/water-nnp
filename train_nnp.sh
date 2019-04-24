#!/usr/bin/env bash

clear
echo
echo "Water-NNP"
echo "============================="

#if [-z "$1"]
#  then
echo "Generating initial dataset..."
rm -f lmp/*.out lmp/*.data
lmp_serial < md.reax.in > lmp/md.reax.out
cp lmp/reax.data lmp/reax0.data
cp lmp/restart.data lmp/restart0.data
python lammps_to_runner.py lmp/reax.data lmp/input.data

echo "RuNNer..."
cd nnp
rm -f *.out *.data
mv ../lmp/input.data .
sh runscript.sh > runscript.out
cd ..
#fi

for i in $(seq 1 1 1)
do
    echo "-----------------------------"
	echo "Extending dataset... ($i)"

    echo "Running MD using NNP..."
	rm -f lmp/nnp.data
	lmp_serial < md.nnp.in > lmp/md.nnp.$i.out

	echo "Rerunning using Reaxff..."
	lmp_serial < rerun.nnp.in > lmp/rerun.nnp.$i.out
	python lammps_to_runner.py lmp/reax.data lmp/input.data

	echo "RuNNer..."
	cd nnp
	rm -f *.out *.data
	mv ../lmp/input.data .
	sh runscript.sh > runscript.out
	cd ..
  
done



