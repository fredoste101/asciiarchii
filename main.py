"""
    Main file for running CLI
"""


import argparse
import json
import sequence as seq


def prepareCLIArguments():
    """
        using argparse prepare the arguments to the CLI
        command.
    """
    argParser = argparse.ArgumentParser(description="Create a sequence diagram in ASCII. " \
                                                    "Configuration is done with json. glhf",
                                        epilog="PRE BETA VERSION. use at own discretion. contact: fredrik.ostdahl@gmail.com")

    argParser.add_argument("--file", 
                           help="The configuration file. Should be json")

    argParser.add_argument("--display", 
                           action="store_true",
                           help="If the graph should be displayed to stdout", 
                           default=False)

    argParser.add_argument("--sequenceOut", 
                           metavar="<filename.txt>", 
                           help="File to write sequence to")

    argParser.add_argument("--jsonOut", 
                           metavar="<filename.json>",
                           help="The generated json will be saved into this file")
    
    return argParser


def main():
    """
        The main CLI entry point
    """

    argParser = prepareCLIArguments()

    cliArgs = argParser.parse_args()

    if not cliArgs.file:
        #Per default use the test.json-file :)
        cliArgs.file = "test.json"

    with open(cliArgs.file, "r") as inputfile:
        config = json.loads(inputfile.read())

    sequence = seq.generateSequence(config)

    if cliArgs.jsonOut:
        with open(cliArgs.jsonOut, "w") as jsonFile:
            jsonFile.write(json.dumps(sequence, indent=1))

    if cliArgs.display:
        displayGraph(sequence)

    if cliArgs.sequenceOut:
        with open(cliArgs.sequenceOut, "w") as sequenceFile:
            sequenceFile.write(seq.getSequenceGraph(sequence))


def displayGraph(sequence):
    """
        Print the graph to stdout
    """

    graphString = seq.getSequenceGraph(sequence) 

    print(graphString)


if __name__ == "__main__":
    main()

