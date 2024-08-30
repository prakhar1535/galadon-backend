#!/bin/bash
python -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install --use-pep517 -r  ./requirements.txt

gunicorn -c gunicorn.conf.py