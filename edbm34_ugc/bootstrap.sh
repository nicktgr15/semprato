#!/usr/bin/env bash

python3 manage.py flush --no-input
python3 manage.py migrate
python3 manage.py loaddata fixtures/sites.json
python3 manage.py loaddata fixtures/users.json
python3 manage.py loaddata fixtures/article_manager.json
python3 manage.py loaddata fixtures/blocked_terms.json

python3 manage.py sitetreeload fixtures/sitetree.json

python3 manage.py runserver 0.0.0.0:8000
