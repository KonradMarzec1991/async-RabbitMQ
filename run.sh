#!/usr/bin/env bash
sleep 10
python /code/server/app.py &
python /code/server/receiver.py
tail -f /dev/null