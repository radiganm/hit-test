#!/usr/bin/make -f
## create-data-files.sh
## Copyright 2012 Mac Radigan
## All Rights Reserved

#dd if=/dev/zero of=1g.bin bs=1G count=1
dout=./data
bs=10000; blocks=1; size=1M;  dd if=/dev/zero of=$dout/test-$size-bs=$bs-nb=$blocks=.zero bs=$bs count=$blocks
bs=10000; blocks=1; size=10M; dd if=/dev/zero of=$dout/test-$size-bs=$bs-nb=$blocks=.zero bs=$bs count=$blocks
size=1M;   fallocate -l $size  $dout/test-$size.bin
size=10M;  fallocate -l $size $dout/test-$size.bin
size=100M; fallocate -l $size $dout/test-$size.bin
size=1G;   fallocate -l $size $dout/test-$size.bin
size=2G;   fallocate -l $size $dout/test-$size.bin
size=3G;   fallocate -l $size $dout/test-$size.bin
size=4G;   fallocate -l $size $dout/test-$size.bin
size=5G;   fallocate -l $size $dout/test-$size.bin
