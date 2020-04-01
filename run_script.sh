#!/usr/bin/env bash
Xvfb :1 & export DISPLAY=:1
python UPLOAD_TO_S3.py &
python survivelance_pi.py &

