#! /usr/bin/env bash
set -euxo pipefail

cd "$(dirname "$(readlink -f "$0")")"
[[ -f VERSION.in ]]
majmin="`cat VERSION.in`"

[[ ! -z "`git tag`" ]]                                 || git tag v$majmin
git describe --tags --long | grep -q '^v[^.]*\.[^.-]*' || git tag v$majmin

revisioncount=`git log --oneline | wc -l`
#projectversion=`git describe --tags --long`
#cleanversion=${projectversion%%-*}
cleanversion="`git describe --tags --long | grep -o '^v[^.]*\.[^.-]*' | sed s/^v//`"
VERSION="$cleanversion.$revisioncount"
echo -n $VERSION | tee ../VERSION
if [[ -z "$VERSION" ]] ; then
	print version is empty
	exit 2
fi
#[[ -n "$VERSION" ]]

VERIFY="`cat ../VERSION`"
if [[ "$VERSION" -ne "$VERIFY" ]] ; then
	print version mismatch
	exit 3
fi
#[[ "$VERSION" -eq "$VERIFY" ]]

