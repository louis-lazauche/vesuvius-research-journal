#!/bin/bash
# HerculeX on a central band of PHerc1545 (9.362 um, 113 keV), GTX 1650 settings (fp32 reader).
export PATH="$HOME/.local/bin:$PATH"
cd ~/vesuvius-project/external/HerculeX
mkdir -p logs
export HERCULEX_READER_FP32=1
export HERCULEX_UNIT_ROWS=6
export HERCULEX_LIST_CT_BRICKS=1
L=logs/pherc1545_band.log
echo "start $(date '+%F %T') free=$(df -h / | awk 'NR==2{print $4}')" | tee -a $L
./run.sh runner.pipeline run all PHerc1545 --band 2>&1 | tee -a $L
echo "EXIT rc=${PIPESTATUS[0]} $(date '+%F %T')" | tee -a $L
