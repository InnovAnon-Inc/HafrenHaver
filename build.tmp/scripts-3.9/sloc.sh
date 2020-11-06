#! /usr/bin/env bash
set -euo pipefail

SF='...,old,.git,__pycache__'
SN='...,*.png,*.key,*.cache,.gitignore,LICENSE,README.md'
pygount \
	--folders-to-skip "$SF" \
	--names-to-skip   "$SN" \
	--format=summary        \
	.
