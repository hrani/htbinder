c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3-config --includes) -I. -I../extern/pybind11/include -I../extern/exprtk ht.cpp htbind.cpp -o ht$(python3-config --extension-suffix)
