#!/bin/bash

find . | grep -E "(__pycache__|\.pyc$|\.pytest_cache)" | xargs rm -rf
cd webapp
rm -rf .venv
rm -rf data