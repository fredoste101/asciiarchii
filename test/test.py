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

    testFilePath = os.path.dirname(os.path.realpath(__file__)) + "/files"

    #A list of sequences to test and what to compare with
    fullSequenceFileTestList = [
        {
            "file"          :"basicEntity.json", 
            "output"        :"basicEntityOut.txt",
            "description"   :"Just a simple entity, no margin no padding."
        }     
    ]


    def test_full_sequence_output(self):
        """
            Run a full sequence Generation and string-getting,
            and then compare to expected output.

            Only test the dislplayed graph. No attributes like color and such.
            Will implicitly check padding and margin and such though.
        """

        for fullFileTest in self.fullSequenceFileTestList:
            testFileName = self.testFilePath + "/" + fullFileTest["file"]
            
            with open(testFileName, "r") as testFile:
                inputData = json.loads(testFile.read())

            sequence = generateSequence(inputData) 

            actualString = getSequenceGraph(sequence)

            testSequenceFileExpectedFile = self.testFilePath + "/" + fullFileTest["output"]

            with open(testSequenceFileExpectedFile, "r") as expectedFile:
                
                expectedString = expectedFile.read().strip() #remove last shit. I think it is EOF or an extra \n

                result = (expectedString == actualString)

                if not result:
                    print("EXPECTED:")
                    print(expectedString)
                    print("ACTUAL:")
                    print(actualString)
                
                self.assertTrue(result, f"TEST DESCRIPTION: {fullFileTest['description']}")

                    

            self.assertTrue(True)



if __name__ == "__main__":
    unittest.main()


