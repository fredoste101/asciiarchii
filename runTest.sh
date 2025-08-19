#!/bin/bash


#
# Runs all unit tests for asciiarchii
#
# Run with:
#	./runTest.sh


#Move to the correct dir to run tests as a module
CURR_DIR=$(dirname $(realpath ${BASH_SOURCE[0]}))

pushd $CURR_DIR &> /dev/null

TEST_RESULT=1

if [ $? ]; then

	cd .. 

	#Run the tests (3.6 is choosen arbitrarily)
	python3.6 -m asciiarchii.test.test

	TEST_RESULT=$?

	#Go back to where we where when command was run
	popd &> /dev/null

fi


exit $TEST_RESULT





