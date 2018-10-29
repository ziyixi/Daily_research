#!/usr/bin/env sh
SaveDir="./data/fdsn$1"
ReadCatalog="./xml/$1.xml"
ParallelFlag="--req_parallel --req_np 16 --parallel_process --process_np 2"
DataSource="all"
Cha="BH*"
TimeFlag="--preset 120 --offset 2400"
StationRegion="70.0/+180.0/0.0/+70.0"

ulimit -Sn 10000
obspyDMT --datapath $SaveDir --waveform_format="sac" --sampling_rate=100 --instrument_correction --read_catalog $ReadCatalog $ParallelFlag --data_source $DataSource --cha $Cha $TimeFlag --station_rect=$StationRegion