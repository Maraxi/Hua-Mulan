#!/bin/bash

cd /pred/
exec python indexing/index.py &
exec python searchengine.py
