"""
    Main file for running CLI
"""
import argparse
import json
import sequence as seq
import sys


def prepareCLIArguments():
    """
        using argparse prepare the arguments to the CLI
        command.
    """

    helpString = "ASCII-Architect (aa)\n\nCreate a sequence diagram in ASCII.\n" \
                 "Configuration is done with json.\nglhf" \
                 "\n\n--- generated usage ---"

    usageExamplesString = "aa --file mySequence.json --display"

    epilogString = "\n\n--- Epilog ---\n\nNB: PRE BETA VERSION.\nuse at own discretion." \
                   "\n\n--- Example usages ---\n\n" \
                   + usageExamplesString + \
                   "\n\n--- contact ---\n\nfredrik.ostdahl@gmail.com"

    argParser = argparse.ArgumentParser(description=helpString,
                                       formatter_class=argparse.RawTextHelpFormatter,
                                        epilog=epilogString)

    argParser.add_argument("--file", 
                           help="The configuration file. Should be json\n\n")

    argParser.add_argument("--getInputSyntax", 
                           action="store_true",
                           help="Get a help-text describing the input syntax,\nas well as example input->outputs.\n\nprotip: pipe this into less.\n\n", 
                           default=False)

    argParser.add_argument("--display", 
                           action="store_true",
                           help="If the graph should be displayed to stdout\n\n", 
                           default=False)

    argParser.add_argument("--sequenceOut", 
                           metavar="<filename.txt>", 
                           help="File to write sequence to.\n\n")

    argParser.add_argument("--jsonOut", 
                           metavar="<filename.json>",
                           help="The generated json will be saved into this file\n\n")
    
    return argParser


def main():
    """
        The main CLI entry point
    """

    argParser = prepareCLIArguments()

    cliArgs = argParser.parse_args()

    if cliArgs.getInputSyntax:
        with open("inputSyntax.txt", "r") as inputSyntaxFile:
            print(inputSyntaxFile.read())
        sys.exit(0)

    if not cliArgs.file:
        print("NEED A JSON FILE TO PARSE.\nPlease provide one with\n\n--file <jsonFile>\n")
        sys.exit(1)

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

