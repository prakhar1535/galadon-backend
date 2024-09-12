#!/bin/bash
python -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install --no-cache-dir --use-pep517 -r  ./requirements.txt --force-reinstall

gunicorn -c gunicorn.conf.py