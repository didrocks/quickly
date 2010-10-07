#!/bin/sh
# -*- Mode: sh; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

if [ ! -e $(pwd)/bin ]; then
    echo "You must run this script from the top level of the quickly source"
    exit 1
fi

run_tests() {
    testdir=$1
    for test in "$testdir"/*; do
        test/one-test.sh "$test"
    done
}

for template in data/templates/*; do
    if [ -d "$template/test" ]; then
        run_tests "$template/test"
    fi
done
