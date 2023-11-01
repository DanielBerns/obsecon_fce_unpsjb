#!/usr/bin/env bash

cd ~/Code/github/DanielBerns/observatorio_fce_unpsjb/
git add .
echo "add"
git commit -m "$1"
echo "commit"
git push
echo "push"
date
cd ~/Apps/observatorio_fce_unpsjb/
git pull
date
cd -
