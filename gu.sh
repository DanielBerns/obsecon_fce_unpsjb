#!/usr/bin/env bash

git add .
echo "add"
git commit -m "$1"
echo "commit"
git push
echo "push"
