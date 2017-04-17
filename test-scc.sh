#!/bin/bash
SCC='python3 compiler/scc.py'
C_SAMPLES="c-samples/*.c"
for filename in $C_SAMPLES; do
    $SCC "$filename"
done
