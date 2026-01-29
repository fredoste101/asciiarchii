"""
    Testing

    Run with:
        python3.6 -m asciiarchii.test.test

    Or single test case
        python3.6 -m asciiarchii.test.test Test.<myCase>
        
"""

import unittest
import os
import json
import sys
import yaml
import argparse

#Import the functionality to test.
from ..sequence import generateSequence 
from ..sequence import getSequenceGraph 
from ..sequence import getEntityCC 

#_verbose = False

def testPrint(msg):
    global _verbose
    if _verbose:
        print(msg)

class Test(unittest.TestCase):

    #Where test files are present
    testFilePath = os.path.dirname(os.path.realpath(__file__)) + "/files"
    testFileDir  = testFilePath + "/sequence"

    def test_getEntityCC(self):
        """
            Test the function:
                getEntityCC
            Since that one was apparently pretty hard to get right...
            I know this because of empiric research done over a number of hours.
            A final conclusion was reached, and is as follows: I'm stupid.
        """

        testPrint("test_getEntityCC START")
        

        with open(self.testFilePath + "/ccTest.json", "r") as testFile:
            inputData = json.loads(testFile.read())
            sequence = generateSequence(inputData) 

    #alice  bob  claire  david erin  fred  gina  hank iris jon karen  lars
    #     12   10      12     9    15    11    11    9    9   7     11  
              
            expectedValueListList = [
                                     [0, 12, 23, 36, 46, 62, 74, 86, 96, 106, 114, 126],
                                     [0, 10, 23, 33, 49, 61, 73, 83, 93, 101, 113],
                                     [0, 12, 22, 38, 50, 62, 72, 82, 90, 102],
                                     [0,  9, 25, 37, 49, 59, 69, 77, 89],
                                     [0, 15, 27, 39, 49, 59, 67, 79],
                                     [0, 11, 23, 33, 43, 51, 63],
                                     [0, 11, 21, 31, 39, 51],
                                     [0,  9, 19, 27, 39],
                                     [0,  9, 17, 29],
                                     [0,  7, 19],
                                     [0, 11],
                                     [0]
                                    ]

            for i, e1 in enumerate(sequence["entityList"]):
                for j, e2 in enumerate(sequence["entityList"][i:]):
                    cc = getEntityCC(sequence, e1, e2)
                    self.assertEqual(expectedValueListList[i][j], cc)

        testPrint("test_getEntityCC END")


    def test_full_sequence_output(self):
        """
            Run a full sequence Generation and string-getting,
            and then compare to expected output.

            Only test the displayed graph. 
            No attributes like color and such.
            Will implicitly check padding and margin and such though.

            Note that these test are build by:
                1. generating a graph from an input file
                2. inspecting manually that everything looks proper in the output
                3. putting that input file -> output in the test framework
                4. we now compare the test-output to the previous test-output (I.E it is regressions test)

            Thus, if the inspection missed errors in the graph,
            the test will be incorrectly made. Does that make sense? 

            If not, the test will protect against new features breaking old ones.
            Nota Bene: I have not tested every edge case scenario. Might be bugs here and there.
            Correction: There is guaranteed bugs here and there.
        """
        testPrint("test_full_sequence_output START")

        for (path, dirList, fileList) in os.walk(self.testFileDir):
            for f in fileList:
                if f.endswith(".json") or f.endswith(".yaml"):
                    testPrint(f"Testing {path} {f}")
                
                    with open(path + "/" + f, "r") as testFile:
                        fileExtension = f.split(".")[1]

                        if fileExtension == "json":
                            inputData = json.loads(testFile.read())

                        elif fileExtension == "yaml":
                            inputData = yaml.safe_load(testFile) 

                        else:
                            print("ERROR IN TEST-CODE: file extension not known", 
                                  file=sys.stderr) 

                    sequence = generateSequence(inputData) 

                    actualString = getSequenceGraph(sequence)

                    with open(path + "/" + f[:-5] + "Out.txt", "r") as expectedFile:

                        #remove last shit. I think it is an extra \n for unknown reasons
                        expectedString = expectedFile.read()[:-1] 

                        result = (expectedString == actualString)

                        if not result:
                            testPrint("FAILED")
                            testPrint("EXPECTED:")
                            testPrint(expectedString)
                            testPrint("ACTUAL:")
                            testPrint(actualString)

                        else:
                            testPrint("PASSED")
                        
                        self.assertTrue(result, f"See earlier messages for error.\n" \
                                                f"TEST NAME: {sequence['name']}\n"\
                                                f"TEST DESCRIPTION: {sequence['description']}")

            self.assertTrue(True)

        testPrint("test_full_sequence_output END")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="hej") 
    
    argParser.add_argument("--verbose", action="store_true")

    argParser.add_argument("unittest_args", nargs="*")

    parsedArgs = argParser.parse_args()

    global _verbose
    _verbose = False

    if parsedArgs.verbose:
        _verbose = True

    sys.argv[1:] = parsedArgs.unittest_args 
    unittest.main()


