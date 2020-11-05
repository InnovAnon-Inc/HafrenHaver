#! /usr/bin/env bash
set -euxo pipefail

cd "$(dirname "$(readlink -f "$0")")"

if [[ -f ../VERSION ]] ; then
	[[ -s ../VERSION ]]
	cat ../VERSION
	exit 0
fi

[[ -f VERSION.in ]]
majmin="`cat VERSION.in`"

[[ ! -z "`git tag`" ]]                                 || git tag "v$majmin"
git describe --tags --long | grep -q '^v[^.]*\.[^.-]*' || git tag "v$majmin"

revisioncount=`git log --oneline | wc -l`
#projectversion=`git describe --tags --long`
#cleanversion=${projectversion%%-*}
cleanversion="`git describe --tags --long | grep -o '^v[^.]*\.[^.-]*' | sed s/^v//`"
VERSION="$cleanversion.$revisioncount"
echo -n $VERSION
#echo -n $VERSION | tee ../VERSION
if [[ -z "$VERSION" ]] ; then
	print version is empty 1>&2
	exit 2
fi
[[ -n "$VERSION" ]] || {
	print version is empty 1>&2 ;
	exit 4                      ;
}
exit 0

VERIFY="`cat ../VERSION`"
if [[ "$VERSION" != "$VERIFY" ]] ; then
	print version mismatch 1>&2
	exit 3
fi
[[ "$VERSION" == "$VERIFY" ]] || {
	print version mismatch 1>&2 ;
	exit 5                      ;
}

