#! /usr/bin/env bash
set -euxo pipefail

PREFIX=src/HafrenHaver/bjorklund
REPO=https://github.com/brianhouse/bjorklund.git
REMOTE=bjorklund

cd "$(dirname "$(readlink -f "$0")")"/..

if [[ ! -d "$PREFIX" ]] ; then # add subtree
	#git subtree add --prefix "$PREFIX" "$REPO" master --squash

	git remote add -f "$REMOTE" "$REPO"
	git subtree add --prefix "$PREFIX" "$REMOTE" master --squash
else # update subtree
	#git subtree pull --prefix "$PREFIX" "$REPO" master --squash

	git fetch "$REMOTE" master git subtree pull --prefix "$PREFIX" "$REMOTE" master --squash
fi

#git subtree push --prefix "$PREFIX" "$REMOTE" master

#git remote remove "$REPO"

