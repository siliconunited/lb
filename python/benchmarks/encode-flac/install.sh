#!/bin/sh

cd $HOME
mkdir $HOME/flac_
tar -xJf flac-1.3.1.tar.xz

cd flac-1.3.1/
./configure --prefix=$HOME/flac_
make -j $NUM_CPU_JOBS
echo $? > $HOME/install-exit-status
make install
cd $HOME
rm -rf flac-1.3.1/
rm -rf flac_/share/

echo "#!/bin/sh
cd $HOME
./flac_/bin/flac --best \$TEST_DEPS/trondheim.wav -f -o /dev/null 2>&1
./flac_/bin/flac --best \$TEST_DEPS/trondheim.wav -f -o /dev/null 2>&1
./flac_/bin/flac --best \$TEST_DEPS/trondheim.wav -f -o /dev/null 2>&1
echo \$? > $HOME/test-exit-status" > encode-flac
chmod +x encode-flac
