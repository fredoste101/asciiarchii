"""
    Debug tools to be used.
    Debug-prints and fatalError exits.
"""
import sys


#if any debuggin should be displayed
_doDebuggingPrints = False


_availableDebugTypes = {
    "CHARGETTING", #I have no idea what this means... 
    "SIZING", #Initial sizing of elements 
    "RESIZING", #resizeing of elements 
    "FUNCTION", #Debug trace for some functions BEGIN->END
    "VARIANT" #Handling of variants in sequence
}

#these are the debug types:
# CHARGETTING - The process of getting chars from the things
# SIZING      - Initial sizing of things. This might change later though, see RESIZING 
# RESIZING    - Whenever a thing needs to be resized, this will tell why and how (hopefully)
# FUNCTION    - Print function begin and end. This is not consistent... I.E not all function has this.
_debuggingTypesEnabled = set() 


def enableDebugging():
    """
        enable debugging prints
    """
    global _doDebuggingPrints
    _doDebuggingPrints = True


def disableDebugging():
    """
        disable debugging prints
    """
    global _doDebuggingPrints
    _doDebuggingPrints = False

def enableDebuggingType(debugType):
    """
        Enable one debuggin type to be enabled.
        For a list of valid debugging types see:

        _availableDebugTypes

    """
    global _availableDebugTypes
    global _debuggingTypesEnabled
    if debugType not in _availableDebugTypes:
        fatalError(f"{debugType} not a available debug type."\
                   f"Available types are {_availableDebugTypes}")

    _debuggingTypesEnabled.add(debugType)


def debugPrint(msg, t=""):
    """
        msg - what to print, I.E a string
        t   - which type of debuggin' it is. 
              can be enabled/disabled through setDebuggingTypesEnabled 
    """
    global _doDebuggingPrints
    global _debuggingTypesEnabled

    if _doDebuggingPrints:
        debugType = t 
        
        if t in _debuggingTypesEnabled: 
            print(f"{debugType}: {msg}")


def fatalError(msg):
    """
        Print error to stderr, 
        then exit with error code
    """
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


