PYTHON = $(shell which python3 )

ifeq (, $(shell which python3 ))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.5

PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys;\
  print(int(float("%d.%d"% sys.version_info[0:2]) >= $(PYTHON_VERSION_MIN)))' )

ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

CFLAGS = \
	-std=c++11 \
	-O3 \
	-Wall 

PYTHON3-PATH:=$(PYTHON)-config --includes
PYTHON3-EXT:=$(PYTHON)-config --extension-suffix
all: generate_pybind

generate_pybind:
	$(CXX) -shared $(CFLAGS) -fPIC `$(PYTHON)-config --includes` -I. -I ../extern/pybind11/include -I../extern/exprtk  \
		ht.cpp htbind.cpp -o ht`$(PYTHON)-config --extension-suffix`

.PHONY: all clean distclean

clean:
	rm -f *.so
	$(RM) *.so
distclean: clean
	rm -f $(EXE)
