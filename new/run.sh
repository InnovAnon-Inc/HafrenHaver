#! /usr/bin/env bash
set -euxo pipefail
(( ! $#   ))
((   $UID ))

export CC=mpicc
PV=$(python3 --version|cut -d\  -f2|cut -d. -f2)

CFLAGS=$(python3-config  --cflags)
LDFLAGS=$(python3-config --ldflags)

python3 setup.py build_ext --inplace
$CC $CFLAGS                                         \
	-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION \
	-I/usr/include/python3.$PV                  \
	-o main main.c                              \
	-lpython3.$PV $LDFLAGS
mpiexec main

