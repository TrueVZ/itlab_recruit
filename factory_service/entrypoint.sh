#!/usr/bin/env bash
while !</dev/tcp/factory-db/5432; do sleep 1; done;
flask db migrate
flask db upgrade
flask run --host=0.0.0.0 --port=5002;

