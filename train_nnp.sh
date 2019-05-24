#!/usr/bin/env bash

REF="reax"

clear
echo
echo "Water-NNP"
echo "============================="

if [ $1 -gt 0 ]
  then
    echo "Generating initial dataset..."
    rm -f lmp/*.out lmp/*.data
    lmp_serial < md.${REF}.in #> lmp/md.${REF}.out
    cp lmp/${REF}.data lmp/${REF}0.data
    cp lmp/restart.data lmp/restart0.data
    python lammps_to_runner.py lmp/${REF}.data lmp/input.data

    echo "RuNNer..."
    cd nnp
    #rm -f *.out *.data
    mv ../lmp/input.data .
    sh runscript.sh #> runscript.out
    cd ..
fi

for i in $(seq 1 1 0)
do
    echo "-----------------------------"
	echo "Extending dataset... ($i)"

    echo "Running MD using NNP..."
	rm -f lmp/nnp.data
	lmp_serial < md.nnp.in #> lmp/md.nnp.$i.out

	echo "Rerunning using ${REF}..."
	lmp_serial < rerun.${REF}.in #> lmp/rerun.${REF}.$i.out
	python lammps_to_runner.py lmp/${REF}.data lmp/input.data

	echo "RuNNer..."
	cd nnp
	#rm -f *.out *.data
	mv ../lmp/input.data .
	sh runscript.sh #> runscript.out
	cd ..
  
done



