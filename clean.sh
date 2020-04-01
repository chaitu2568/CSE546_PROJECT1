#!/usr/bin/env bash
find . -type f -name myvideo\* -exec rm {} \;
find . -type f -name ourvideo\* -exec rm {} \;
python3 clean.py
pkill -f UPLOAD_TO_S3.py
pkill -f survivelance_pi.py
