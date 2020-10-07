#! /usr/bin/env bash
set -euxo pipefail
watch --differences=cumulative ./sloc.sh
