#!/usr/bin/env bash

DIR="nnp"

echo "RuNNer..."
cd ${DIR}
rm -f *.out *.data
cp ../lmp/input.data .
sh runscript.sh #> runscript.out
cd ..
