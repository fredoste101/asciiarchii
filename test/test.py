"""
    Testing

    Run with:
        python3.6 -m asciiarchii.test.test
"""

import unittest
import os
import json

#Import the functionality to test.
from ..sequence import generateSequence 
from ..sequence import getSequenceGraph 


class Test(unittest.TestCase):

    #Where test files are present
    testFilePath = os.path.dirname(os.path.realpath(__file__)) + "/files"


    def test_full_sequence_output(self):
        """
            Run a full sequence Generation and string-getting,
            and then compare to expected output.

            Only test the dislplayed graph. No attributes like color and such.
            Will implicitly check padding and margin and such though.
        """

        testFileDir = self.testFilePath + "/sequence/"


        for (path, dirList, fileList) in os.walk(testFileDir):
            for f in fileList:
                if f.endswith(".json"):
                    #print(f"Testing {f}")
                
                    with open(testFileDir + f, "r") as testFile:
                        inputData = json.loads(testFile.read())

                    sequence = generateSequence(inputData) 

                    actualString = getSequenceGraph(sequence)

                    with open(testFileDir + f[:-5] + "Out.txt", "r") as expectedFile:
                        
                        expectedString = expectedFile.read()[:-1] #remove last shit. I think it is an extra \n for unknown reasons

                        result = (expectedString == actualString)

                        if not result:
                            print("EXPECTED:")
                            print(expectedString)
                            print("ACTUAL:")
                            print(actualString)
                        
                        self.assertTrue(result, f"TEST DESCRIPTION: {sequence['description']}")

                        

            self.assertTrue(True)



if __name__ == "__main__":
    unittest.main()


