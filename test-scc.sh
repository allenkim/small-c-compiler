#!/bin/bash
SCC='python3 compiler/scc.py'
RUN='python3 compiler/scc_sm.py'
FILE='c-samples/test.c'
$SCC $FILE
$RUN "a.out"
