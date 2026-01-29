"""
    Main file for running CLI
"""
import argparse
import json
import sequence as seq
import common as aacommon
import sys
import os

import debug 

_yamlEnabled = False

try:
    import yaml
    _yamlEnabled = True
except ImportError as e:
    print("NOTE: could not import yaml")


def prepareCLIArguments():
    """
        using argparse prepare the arguments to the CLI
        command.
    """

    helpString = "ASCII-Architect (aa)\n\nCreate a sequence diagram in ASCII.\n" \
                 "Configuration is done with json.\nglhf" \
                 "\n\n--- generated usage ---"

    usageExamplesString = "Stop it. Get some help:\n" \
                          "aa --help\n\n" \
\
                          "Simply display the graph to stdout:\n" \
                          "aa --file mySequence.json --display\n\n" \
\
                          "Save the resulting json and ascii graph in two separate file:\n" \
                          "aa --file inputSequence.json --jsonOut outputSequence.json --sequenceOut sequence.txt\n\n" \
\
                          "Get a json-syntax description with examples:\n" \
                          "aa --getInputSyntax"

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
                           help="Get a help-text describing the input syntax,\n"\
                                "as well as example input->outputs.\n\nprotip: pipe this into less.\n\n", 
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

    argParser.add_argument("--debug", 
                           action="store_true",
                           default=False,
                           help="Enable debug prints. Also set which one with --debugType")

    argParser.add_argument("--debugType", 
                           action="append",
                           help="Enable types of debug prints. Needs --debug to work.\nCan give as many as you like, eg:\n"\
                                "--debugType RESIZING --debugType FUNCTION ... etc")
    
    return argParser


def displayGraph(sequence):
    """
        Print the graph to stdout
    """

    graphString = seq.getSequenceGraph(sequence) 

    print(graphString)


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
        print("NEED A JSON FILE TO PARSE.\nPlease provide one with\n\n--file <jsonFile>\n", file=sys.stderr)
        sys.exit(1)

    with open(cliArgs.file, "r") as inputfile:

        if cliArgs.file.split(".")[1] == "yaml":
            if not _yamlEnabled:
                print("yaml could not be imported and thus is disabled. "\
                      "Try pip install yaml or something I don't know...", file=sys.stderr)
                sys.exit(1)

            config = yaml.safe_load(inputfile)

            #print(config)

        elif cliArgs.file.split(".")[1] == "json":
            config = json.loads(inputfile.read())

        else:
            print("WRONG FORMAT ON FILE. "\
                  "NEED A JSON (OR YAML) FILE TO PARSE.\n"\
                  "Please provide one with\n\n--file <jsonFile>\n", 
                  file=sys.stderr)

            sys.exit(1)
            
    
    path = os.path.dirname(cliArgs.file) 

    if path != "":
        path += "/"

    aacommon.handleAuxiliary(config, path)

    if cliArgs.debug:
        debug.enableDebugging()

        for debugType in cliArgs.debugType:
            debug.enableDebuggingType(debugType)
            print(debugType)

    if "type" in config:
        #To be able in the future to create other types of diagrams :)
        if config["type"] == "sequence":
            sequence = seq.generateSequence(config)

        else:
            print(f"ERROR: unknown asciiarchitecture-type: {sequence['type']}") 
            sys.exit(1)

    else:
        sequence = seq.generateSequence(config)

    if cliArgs.jsonOut:
        with open(cliArgs.jsonOut, "w") as jsonFile:
            #Must remove all circular dependencies before jsonify it...
            seq.removeCircularDependencies(sequence)
            jsonFile.write(json.dumps(sequence, indent=1))

    if cliArgs.display:
        displayGraph(sequence)

    if cliArgs.sequenceOut:
        with open(cliArgs.sequenceOut, "w") as sequenceFile:
            sequenceFile.write(seq.getSequenceGraph(sequence))



if __name__ == "__main__":
    main()

