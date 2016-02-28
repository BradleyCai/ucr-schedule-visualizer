#!/bin/sh
cd "$(dirname "$0")/tests"
#python test.py -c test-conf.json example.test
python test.py -c test-conf.json *.test

