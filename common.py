import json

def includeAuxiliary(sequence, path):
    """
        Include the auxiliary files 
    """

    sequence["auxiliary"] = {}
    if "auxiliaryFileList" in sequence:
        #must open the files one by one here. I don't like, but lets do it like that first.
        
        for auxiliaryFile in sequence["auxiliaryFileList"]:
            with open(path + auxiliaryFile) as af: #af af ;)
                auxiliary = json.loads(af.read())
                sequence["auxiliary"].update(auxiliary)


def substibuteAuxiliaryField(sequence, sub, k):
    v = sub[k]
    if isinstance(v, str):
        if v.startswith("__aux__"):
            if v in sequence["auxiliary"]:
                sub[k] = sequence["auxiliary"][v]
            #Is it an error otherwise? 

    elif isinstance(v, dict):
        substituteAuxiliaryDict(sequence, v)

    elif isinstance(v, list):
        substituteAuxiliaryList(sequence, v)


def substituteAuxiliaryDict(sequence, d):
    for k in d:
        substibuteAuxiliaryField(sequence, d, k)


def substituteAuxiliaryList(sequence, l):
    for v in l:
        if isinstance(v, dict):
            substituteAuxiliaryDict(sequence, v)
        

def substibuteAuxiliary(sequence):
    if len(sequence["auxiliary"]) > 0:
        for k in sequence:
            substibuteAuxiliaryField(sequence, sequence, k)
            

def handleAuxiliary(sequence, path):
    """
        Load in the auxiliary files,
        and do the substitutions
    """
    includeAuxiliary(sequence, path)
    substibuteAuxiliary(sequence)


