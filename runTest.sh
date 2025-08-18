#!/bin/bash


#
# Runs all unit tests for asciiarchii
#


#Move to the correct dir to run tests as a module
CURR_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pushd $CURR_DIR

cd .. 

#Run the tests (3.6 is choosen arbitrarily)
python3.6 -m asciiarchii.test.test

#Go back to where we where when command was run
popd





