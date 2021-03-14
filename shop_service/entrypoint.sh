#!/usr/bin/env bash
while !</dev/tcp/shop-db/5432; do sleep 1; done;
flask db migrate
flask db upgrade
gunicorn -b 0.0.0.0:5001 "app:create_app()"