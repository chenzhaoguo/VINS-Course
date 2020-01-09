#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

echo "Configuring and building ..."
if [ ! -d "build" ]; then
  mkdir build
fi

if [ -d "bin" ]; then
  cd bin
  rm -rf *
  cd ..
fi

cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4