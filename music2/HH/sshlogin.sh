#! /usr/bin/env bash
set -euo pipefail

./sshlogin.exp "$@" &&
echo "$@" >> "$0.log"

