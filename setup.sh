#!/bin/sh

PYTHON_SCRIPTS_DIRECTORY=/home/nmathieu/Development/python-scripts

upgradeVenvPip () {
    $PYTHON_SCRIPTS_DIRECTORY/venv/bin/python -m pip install --upgrade pip
}

initialSetup () {
    git submodule update --init && virtualenv venv && . $PYTHON_SCRIPTS_DIRECTORY/venv/bin/activate && upgradeVenvPip && pip install -e $PYTHON_SCRIPTS_DIRECTORY/submodules/pybaseball && pip install -r requirements.txt
}

activate () {
    . $PYTHON_SCRIPTS_DIRECTORY/venv/bin/activate && pip install -r requirements.txt
}