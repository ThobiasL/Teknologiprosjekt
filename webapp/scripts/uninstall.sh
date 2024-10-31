#!/bin/bash

find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
cd webapp
rm -rf .venv
rm -rf data