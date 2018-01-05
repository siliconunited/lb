#!/bin/sh

#
# Little Benchmark
# /benchmarks/setup.sh
# This script handles setting up all of the benchmarks required for Little Benchmark to function.
#

echo "Setting up Little Benchmark..."

# Start the processes in parallel...
echo "Starting installation scripts... "
./benchmarks/encode-flac/install.sh 1>&1 2>&1 & pid1=$!
# ./benchmarks/encode-flac/install.sh 1>/dev/null 2>&1 & pid1=$!
# ./benchmarks/himeno/install.sh 1>&1 2>&1 & pid2=$!
# ./benchmarks/iozone/install.sh 1>&1 2>&1 & pid3=$!
# ./benchmarks/ramspeed/install.sh 1>&1 2>&1 & pid4=$!

# Wait for processes to finish...
echo "Installation started... "
wait $pid1
err1=$?
wait $pid2
err2=$?
wait $pid3
err3=$?
wait $pid4
err4=$?

if [ $err1 -eq 0 -a $err2 -eq 0 -a $err3 -eq 0 -a $err4 -eq 0 ]
then
    echo "Little Benchmark installed successfully."
else
    echo "Little Benchmark failed to installed."
fi
