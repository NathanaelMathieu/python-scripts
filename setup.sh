#!/bin/sh

PYTHON_SCRIPTS_DIRECTORY=/home/nmathieu/Development/python-scripts

upgradeVenvPip () {
    $PYTHON_SCRIPTS_DIRECTORY/venv/bin/python -m pip install --upgrade pip
}

initialSetup () {
    virtualenv venv && . $PYTHON_SCRIPTS_DIRECTORY/venv/bin/activate && upgradeVenvPip -m pip install --upgrade pip && pip install -r requirements.txt
}

enter () {
    . $PYTHON_SCRIPTS_DIRECTORY/venv/bin/activate && pip install -r requirements.txt
}