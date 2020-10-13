#!/bin/bash

rm -r build
rm *.spec
pyinstaller3 --onefile  --clean $1
