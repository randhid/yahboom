#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Create a virtual Python environment
cd `dirname $0`

# Create a virtual environment to run our code
VENV_NAME="venv"
PYTHON="$VENV_NAME/bin/python"
ENV_ERROR="This module requires Python >=3.8, pip, and virtualenv to be installed."

if ! python3 -m venv --system-site-packages $VENV_NAME >/dev/null 2>&1; then
    echo "Failed to create virtualenv."
    if command -v apt-get >/dev/null; then
        echo "Detected Debian/Ubuntu, attempting to install python3-venv automatically."
        SUDO="sudo"
        if ! command -v $SUDO >/dev/null; then
            SUDO=""
        fi
		if ! apt info python3-venv >/dev/null 2>&1; then
			echo "Package info not found, trying apt update"
			$SUDO apt -qq update >/dev/null
		fi
        $SUDO apt install -qqy python3-venv >/dev/null 2>&1
        if ! python3 -m venv $VENV_NAME >/dev/null 2>&1; then
            echo $ENV_ERROR >&2
            exit 1
        fi
    else
        echo $ENV_ERROR >&2
        exit 1
    fi
fi

echo "Virtualenv found/created. Installing/upgrading Python packages..."
if ! $PYTHON -m pip install -r requirements.txt -Uqq; then
    exit 1
fi

echo "Starting module..."
# Be sure to use `exec` so that termination signals reach the Python process,
# or handle forwarding termination signals manually
exec ${SCRIPT_DIR}/venv/bin/python3 ${SCRIPT_DIR}/src/main.py $@








# #!/usr/bin/env bash

# # bash safe mode. look at `set --help` to see what these are doing
# set -euxo pipefail 

# cd $(dirname $0)
# source .env

# set -euo pipefail

# SUDO=sudo
# if ! command -v $SUDO; then
# 	echo no sudo on this system, proceeding as current user
# 	SUDO=""
# fi

# if command -v apt-get; then
# 	if dpkg -l python3-venv; then
# 		echo "python3-venv is installed, skipping setup"
# 	else
# 		if ! apt info python3-venv; then
# 			echo package info not found, trying apt update
# 			$SUDO apt-get -qq update
# 		fi
# 		$SUDO apt-get install -qqy python3-venv
# 	fi
# else
# 	echo Skipping tool installation because your platform is missing apt-get.
# 	echo If you see failures below, install the equivalent of python3-venv for your system.
# fi

# source .env
# echo creating virtualenv at $VIRTUAL_ENV
# python3 -m venv $VIRTUAL_ENV
# echo installing dependencies from requirements.txt
# $VIRTUAL_ENV/bin/pip install -r requirements.txt

# # Be sure to use `exec` so that termination signals reach the python process,
# # or handle forwarding termination signals manually
# exec $PYTHON -m src.main $@
