#!/bin/bash

find . -name "*.py" -type f -exec python3 -m pylint {} +
