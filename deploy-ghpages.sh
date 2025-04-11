#!/bin/bash
#
# This script automates the deployment of project documentation to the
# `gh-pages` branch.
#
# Usage:
#   1. Ensure the documentation is built and available in the specified build
#      directory.
#   2. Run this script from the root of the Git repository.
#
# Features:
#   - Automatically switches to the `gh-pages` branch (creates it if it doesn't
#     exist).
#   - Clears the existing content in the `gh-pages` branch.
#   - Copies the built documentation from the specified build directory to the
#     branch.
#   - Commits and pushes the changes to the remote repository.
#   - Switches back to the original branch after deployment.
#
# Requirements:
#   - The script assumes the documentation is built using Sphinx and is
#     located in the `doc/build/html` directory.
#   - Git must be installed and configured.
#
# Configurations:
#   - BUILD_DIR: Path to the directory containing the built documentation
#     (default: `doc/build/html`).
#   - DEPLOY_BRANCH: Name of the branch to deploy the documentation to
#     (default: `gh-pages`).
#   - MESSAGE: Commit message for the deployment (default: includes the current
#     date and time).
#
# Notes:
#   - The script uses a temporary directory to store the built documentation 
#     during the deployment process.
#   - If the `gh-pages` branch does not exist, it will be created as an orphan
#     branch.
#   - The script will exit immediately if any command fails (set -e).
#
# Example:
#   ./deploy-ghpages.sh
#
# Name: deploy-ghpages.sh
# Author: ChatGPT
# Version: 0.0.1.1
# Date: 2025-04-09
# License: MIT License Copyright 2025 GitHubonline1396529

set -e  # Exit if there's Error

# Optional configurations.
BUILD_DIR="doc/build/html"
EXAMPLE_DIR="example"
DEPLOY_BRANCH="gh-pages"
TEMP_DIR="$(mktemp -d)"
TEMP_DIR_FOR_EXAMPLE_FILES="$(mktemp -d)"
MESSAGE=":package: Deploy website $(date '+%Y-%m-%d %H:%M:%S')"

echo "
It will switch back to branch $DEPLOY_BRANCH after the deployment.
"

# Remember the current branch.
CURRENT_BRANCH=$(git branch --show-current)

# Check if the BUILD_DIR exist
if [ ! -d "$BUILD_DIR" ]; then
    echo "The build directory $BUILD_DIR doesn't exist."
    echo "Please run sphinx-build first!"
    exit 1
fi

# Create a temporary directory and copy the HTML pages into it.
cp -r "$BUILD_DIR"/* "$TEMP_DIR"/
cp -r "$EXAMPLE_DIR"/* "$TEMP_DIR_FOR_EXAMPLE_FILES"/

# Check if the gh-pages branch exists, and create it if it doesn't.
if ! git show-ref --verify --quiet refs/heads/$DEPLOY_BRANCH; then
    echo "Branch $DEPLOY_BRANCH does not exist. Creating it..."
    git checkout --orphan $DEPLOY_BRANCH
    git rm -rf . > /dev/null 2>&1 || true
else
    echo Switch to the $DEPLOY_BRANCH branch.
    git checkout $DEPLOY_BRANCH
fi

# Remove everything in gh-pages.
git rm -rf . > /dev/null 2>&1 || true
rm -rf *

# Remove files and directories start with `.*` execept for `.git`.
for item in .[^.]*; do
    if [ "$item" != ".git" ]; then
        rm -rf "$item"
    fi
done

# Copy new files.
cp -r "$TEMP_DIR"/* .

if [ ! -d "$EXAMPLE_DIR" ]; then
  echo "The example directory $EXAMPLE_DIR doesn't exist."
  echo "Create it now..."
  mkdir "$EXAMPLE_DIR"
else
  echo "The example directory $EXAMPLE_DIR exist."
  echo "We're going to copy the files."
fi

cp -r "$TEMP_DIR_FOR_EXAMPLE_FILES"/* ./"$EXAMPLE_DIR"/

# Ignore nojekyll
touch ./.nojekyll

# Add and commit.
git add .
git commit -m "$MESSAGE" || echo "Nothing to commit. (Remain unchanged.)"
git push origin $DEPLOY_BRANCH

# Switch back to the original branch.
git checkout "$CURRENT_BRANCH"
echo "Deploy finished. Switch back to branch $CURRENT_BRANCH"

# Remove the temporary directory.
rm -rf "$TEMP_DIR"
rm -rf "$TEMP_DIR_FOR_EXAMPLE_FILES"
