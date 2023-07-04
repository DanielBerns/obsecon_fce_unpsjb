#!/usr/bin/env bash

git add .
echo "add ."
echo $1
git commit -m "$1"
git push
