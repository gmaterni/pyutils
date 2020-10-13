#!/bin/bash

rm -r build
rm *.spec
# pyinstaller --onefile  $1
pyinstaller2 --onefile  --clean $1
