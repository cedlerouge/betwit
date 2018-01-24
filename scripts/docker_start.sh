#!/bin/bash

# Start Gunicorn processes
#cd ../
echo Starting Gunicorn.
exec gunicorn betwit.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3

