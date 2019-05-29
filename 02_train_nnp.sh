#!/usr/bin/env bash

echo "RuNNer..."
cd nnp
#rm -f *.out *.data
mv ../lmp/input.data .
sh runscript.sh #> runscript.out
cd ..