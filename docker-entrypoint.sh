#!/bin/sh
set -e # Will exit the script if any error occurs 
eval "exec $@" # Expand arguments passed to the entrypoint script in the shell before passing them to exec, so that it can support passing environment variable.

