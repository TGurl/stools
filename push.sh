#!/usr/bin/env bash

set -e

echo 'Please enter a message for this commit'
read -p 'Commit: ' commit

git add .
git commit -m "${commit}"
git push
