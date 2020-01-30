#!/bin/bash
# start building the package
rm -rf build
rm -rf bin
mkdir -p bin/
mkdir -p build
cp -r bin build/.
cp lambda_function.py build/.
# first write lambda function and call other functions needed (Abstraction)
