#! /usr/bin/env bash
set -euxo pipefail

V=-v

# this is a hack, but we have to make sure we're only ever running this from
# the top level of the package and not in the subdirectory...
if [[ ! -f src/HafrenHaver/__init__.py ]]; then
    echo 'This must be run from the gh_doc_automation project directory'
    exit 3
fi

# get the running branch
branch=$(git symbolic-ref --short HEAD)

# cd into docs, make them
cd doc
make clean html EXAMPLES_PATTERN=ex_*
cd ..

# move the docs to the top-level directory, stash for checkout
mv $V doc/_build/html ./

# html/ will stay there actually...
git config user.email "$GH_EMAIL"
git config user.name  "$GITHUB_API_USERNAME"
git stash

# checkout gh-pages, remove everything but .git, pop the stash
# switch into the gh-pages branch
git checkout    gh-pages
git pull origin gh-pages

# Make sure to set the credentials!
git config --global user.email "$GH_EMAIL"            > /dev/null 2>&1
git config --global user.name  "$GITHUB_API_USERNAME" > /dev/null 2>&1

# remove all files that are not in the .git dir
# TODO use a working command
find . -not -name '.git/*' -type f -maxdepth 1 -delete
#find . -maxdepth 1 \( \( -name .git -o -name .venv \) -prune \) -o -delete

# Remove the remaining directories. Some of these are artifacts of the LAST
# gh-pages build, and others are remnants of the package itself
declare -a leftover=('.cache/'
                     '.idea/'
                     'build/'
                     'build_tools/'
                     'doc/'
                     'examples/'
                     'src/'
                     #'HafrenHaver.egg-info/'
                     '_downloads/'
                     '_images/'
                     '_modules/'
                     '_sources/'
                     '_static/'
                     'auto_examples/'
                     'includes'
                     'modules/'
	             '_autosummary'
	             'tests/'
	             'old/'
	             #'.circleci/'
		     #'.venv/'
)

set +x
# check for each left over file/dir and remove it
for left in "${leftover[@]}" ; do
    #rm -r "$left" || echo "$left does not exist; will not remove"
    [[ -e "$left" ]] || continue
    echo "removing $left"
    rm -r "$left"
done
set -x

# we need this empty file for git not to try to build a jekyll project
touch .nojekyll
mv $V html/* ./
rm -r html/

find . \( \( -name .git -o -name .venv \) -prune \) -o -print

# Add everything, get ready for commit. But only do it if we're on master
if [[ "$CIRCLE_BRANCH" =~ ^master$|^[0-9]+\.[0-9]+\.X$ ]]; then
    git add --all
    git commit -m '[ci skip] publishing updated documentation...' || : # TODO

    # We have to re-add the origin with the GH_TOKEN credentials
    git remote rm origin
    git remote add origin https://"$GITHUB_API_USERNAME":"$GITHUB_API_KEY"@github.com/InnovAnon-Inc/HafrenHaver.git

    # NOW we should be able to push it
    #git push origin gh-pages
    git push --force origin gh-pages
else
    echo "Not on master, so won't push doc"
fi

