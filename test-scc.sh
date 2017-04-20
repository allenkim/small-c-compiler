#!/bin/bash
SCC='python3 compiler/scc.py'
RUN='python3 compiler/scc_sm.py -v'
C_SAMPLES="c-samples/test.c"
#for filename in $C_SAMPLES; do
#    $SCC "$filename"
#done
$SCC $C_SAMPLES
$RUN "a.out"
