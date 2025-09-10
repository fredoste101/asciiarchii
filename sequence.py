"""
    Sequence creation/generation
"""

import sys
import copy


doDebuggingPrints = False


def fatalError(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def debugPrint(msg):
    if doDebuggingPrints:
        print(f"DEBUG: {msg}")


def setStyle(e):
    """
        Checks style (margin, border, padding)
        And if they are not set, sets default values for them.
    """
    if "margin" not in e:
        e["margin"] = [0,0,0,0]

    if "border" not in e:
        e["border"] = [1,1,1,1]

    if "padding" not in e:
        e["padding"] = [0,0,0,0]


def determineHeightsOfHeader(itemList):
    """
        Aight, then this will determine the heights of the top row.
        I.E actors and such. madderfakking. 

        So nice. very good.
    """

    heightestMf = 0

    for item in itemList:
        h = 0

        if item["type"] == "container":
            h = item["height"]

        elif item["type"] == "entity":
            h = item["height"]

        if heightestMf <= h:
            heightestMf = h
    
        
    return heightestMf 


def determineWidthOfSequence(sequence):
    """
        The header (entities) will after resizing due to actions,
        determine the total width of the sequence :)
    """

    w = 0

    for i in sequence["itemList"]:
        w += i["width"]

    sequence["width"] = w


def getOrderedEntityList(itemList):
    """
        Get a list of entities in order of appearance,
        so we can perform operation on them uckas in order.

        I.E we must know the order in order to order them to do ordinary actions. sorry.
    """
    pass 


def setEntityPos(entity, pos):
    """
        Set the position of an entity.

        Sizes have already been set.

        pos ::= [X, Y]

        So, with pos as start position, 
        determine for the entity:

            startPos (top left corner, margin included)
            endPos   (bottom right corner, margin included)

            borderStartPos
            borderEndPos

            contentStartPos
            contentEndPos

        Return the size of the entity as:

            [width, height]
    """

    #Total sizing (with margin):
    entity["startPos"] = pos 

    endX = pos[0] + entity["size"][0] - 1

    endY = pos[1] + entity["size"][1] - 1

    entity["endPos"] = [endX, endY]


    #Border

    entity["borderStartPos"] = [-1, -1]

    entity["borderStartPos"][0] = pos[0] + entity["margin"][3]

    entity["borderStartPos"][1] = pos[1] + entity["margin"][0]

    entity["borderEndPos"] = [-1, -1]

    entity["borderEndPos"][0] = endX - entity["margin"][1]

    entity["borderEndPos"][1] = endY - entity["margin"][2]


    #Content 

    entity["contentStartPos"] = [-1, -1]

    entity["contentStartPos"][0] = entity["borderStartPos"][0] + entity["border"][3] + entity["padding"][3] 

    entity["contentStartPos"][1] = entity["borderStartPos"][1] + entity["border"][0] + entity["padding"][0]

    entity["contentEndPos"] = [-1, -1]

    entity["contentEndPos"][0] = entity["contentStartPos"][0] + len(entity["name"]) - 1

    #Only allow one line names now
    entity["contentEndPos"][1] = entity["contentStartPos"][1] 

    #A bit unclear how to jump ahead here though....
    #pos = [pos[0] + entity["totalSize"][0], pos[1] + entity["totalSize"][1]]
    #pos = [pos[0] + entity["totalSize"][0], pos[1] + entity["totalSize"][1]]

    return [entity["size"][0], entity["size"][1]]


def setContainerPos(container, pos):
    #Total sizing (with margin):
    container["startPos"] = pos 

    endX = pos[0] + container["size"][0] - 1

    endY = pos[1] + container["size"][1] - 1

    container["endPos"] = [endX, endY]


    #Border

    container["borderStartPos"] = [-1, -1]

    container["borderStartPos"][0] = pos[0] + container["margin"][3]

    container["borderStartPos"][1] = pos[1] + container["margin"][0]

    container["borderEndPos"] = [-1, -1]

    container["borderEndPos"][0] = endX - container["margin"][1]

    container["borderEndPos"][1] = endY - container["margin"][2]


    #Content 

    container["contentStartPos"] = [-1, -1]

    container["contentStartPos"][0] = container["borderStartPos"][0] + container["border"][3] + container["padding"][3] 

    container["contentStartPos"][1] = container["borderStartPos"][1] + container["border"][0] + container["padding"][0]

    container["contentEndPos"] = [-1, -1]

    container["contentEndPos"][0] = container["contentStartPos"][0] + len(container["name"]) - 1

    #Only allow one line names now
    container["contentEndPos"][1] = container["contentStartPos"][1] 


    contentXPos = pos[0] + container["margin"][3] + container["border"][3] + container["padding"][3]

    #Add the content height. NOTE: if content becomes more than one line, need change
    contentYPos = pos[1] + container["margin"][0] + container["border"][3] + container["padding"][0] + 1

    contentPos = [contentXPos, contentYPos]


    for item in container["itemList"]:
        if item["type"] == "entity":
            [width, height] = setEntityPos(item, contentPos)
            contentPos[0] += width

        elif item["type"] == "container":
            [width, height] = setContainerPos(item, contentPos)
            contentPos[0] += width

        else:
            fatalError(f"Unknown type: {item['type']}")


    return [container["size"][0], container["size"][1]]

def determineRelativePositionOfItems(sequence, pos):

    #Build the relative positions for each element in header (I.E entities)
    for item in sequence["itemList"]:
        if item["type"] == "entity":
            [width, height] = setEntityPos(item, pos)

            #Move along only x-axis the width of the entity
            pos[0] += width

        elif item["type"] == "container":
            [width, height] = setContainerPos(item, pos)
            pos[0] += width

        else:
            fatalError(f"Unknown type: {item['type']}")


def determineRelativePositionOfOnAction(sequence, onAction, row):
    entity = getEntityWithId(sequence, onAction["entityId"])

    middleCol = entity["timeLineCol"] 

    startCol = middleCol - int(onAction["width"] / 2) 


    #OUTER POS
    onAction["startPos"]            = [startCol, row]
    onAction["endPos"]              = [startCol + onAction["width"], 
                                       row + onAction["height"] - 1] 

    #Border
    onAction["borderStartPos"]      = [startCol + onAction["margin"][3], 
                                       row + onAction["margin"][0]]

    onAction["borderEndPos"]        = [startCol + onAction["width"] - onAction["border"][1] - onAction["margin"][1], 
                                       row + onAction["height"] - onAction["border"][2] - onAction["margin"][2]] 


    #Content. 'member, content is only allowed to be 1 line in height as of now.... 
    onAction["contentStartPos"]     = [startCol + onAction["padding"][3] + \
                                                  onAction["border"][3] + \
                                                  onAction["margin"][3], 
                                       row + onAction["border"][0] + \
                                             onAction["padding"][0] + \
                                             onAction["margin"][0]]

    onAction["contentEndPos"]       = [startCol - 1 + len(onAction["content"]) + onAction["padding"][3] + \
                                                                                 onAction["border"][3] + \
                                                                                 onAction["margin"][3], 
                                       row + onAction["border"][0] + \
                                             onAction["padding"][0] + \
                                             onAction["margin"][0]]


def determineRelativePositionOfCommunicationAction(sequence, communication, row):
    """
        Determine where to place a specific communication.
        
        row is the row that the communication should start at.
    """
    fromEntity  = getEntityWithId(sequence, communication["fromEntityId"])    
    toEntity    = getEntityWithId(sequence, communication["toEntityId"])    

    fromCol = fromEntity["timeLineCol"]
    toCol   = toEntity["timeLineCol"]

    arrowChar = ">"


    

    if fromCol < toCol:
        communicationMiddle = fromCol + int((toCol - fromCol - 1) / 2)

        communication["arrowPos"] = [toCol - 1, row + 1]
        communication["arrowChar"] = ">"

        communication["lineStartPos"] = [fromCol + 1, row + 1]

        communication["lineEndPos"] = [toCol - 2, row + 1]
        
    else:
        communicationMiddle = toCol + int((fromCol - toCol - 1) / 2)

        communication["arrowPos"] = [toCol + 1, row + 1]
        communication["arrowChar"] = "<"

        communication["lineStartPos"] = [toCol + 2, row + 1]
        communication["lineEndPos"] = [fromCol - 1, row + 1]

    communication["contentStartPos"] = [communicationMiddle - int((len(communication["content"]) - 1)/2), row]
    communication["contentEndPos"]   = [communicationMiddle + int(len(communication["content"])/2), row]
    
    [e1, e2] = getFromAndToEntities(sequence, fromEntity["id"], toEntity["id"]) 

    #print(f"cc {getEntityCC(sequence, e1, e2)}")
    #print(f"comm: {communication['content']} width: {communication['size'][0]} starts at {communication['lineStartPos']} - {communication['lineEndPos']}")



def determineRelativePositionOfVariantAction(sequence, variant, row):
    """
        Determine the relative position of variant type action.
    """
    action = variant
    startCol = action["fromEntity"]["timeLineCol"] - action["left"] + 1 - \
                                                     action["padding"][3] -\
                                                     action["border"][3] -\
                                                     action["margin"][3]
                                                    
    action["startPos"]          = [startCol, row]
    action["endPos"]            = [startCol + action["size"][0], row + action["size"][1] - 1] 
    
    #FIXME: this is wrong. no margin allowed?
    action["borderStartPos"]    = [startCol, row]

    action["borderEndPos"]      = [startCol + action["size"][0] - 1, \
                                   row + action["size"][1] - 1 - action["margin"][2]] 

    branchPos = copy.copy(action["startPos"])

    isFirstBranch = True #The first one no horizontal stuff. The next, yes.

    branchContentRow = action["startPos"][1] + action["margin"][0] + \
                                               action["border"][0] + \
                                               action["padding"][0] + \
                                               2 #2 is name + border bottom i guess...

    for branch in action["branchList"]:
        
        if not isFirstBranch:
            branchContentRow += 3
            branch["branchBorderStart"] = copy.copy(branchPos) 
            branch["branchBorderEnd"]   = [branchPos[0] + action["size"][0] - 1, 
                                           branchPos[1]] 

        branch["startPos"] = branchPos
        contentStartPos    = [branchPos[0] + 1, branchPos[1] + 1]

        #FIXME: this does not take into account margin n' shit
        branch["contentStartPos"]   = copy.copy(contentStartPos)
        branch["contentEndPos"]     = [contentStartPos[0] + len(branch["name"]) - 1, 
                                       contentStartPos[1]]

        branch["borderStartPos"] = copy.copy(branchPos)
        branch["borderEndPos"]   = [branchPos[0] + len(branch["name"]) + 1, 
                                    branchPos[1] + 2]
        
        for branchAction in branch["actionList"]:
            if branchAction["type"] == "on":      
                determineRelativePositionOfOnAction(sequence, branchAction, branchContentRow)
                branchContentRow += branchAction["height"]

            elif branchAction["type"] == "variant":
                determineRelativePositionOfVariantAction(sequence, branchAction, branchContentRow)
                branchContentRow += branchAction["size"][1]
                #fatalError(f"Type {branchAction['type']} what to do??")

            else:
                fatalError(f"Type {branchAction['type']} not supported now")


        branchPos = copy.copy(branchPos) 
    
        #I don't know why this works, but it does...
        if isFirstBranch:
            branchPos[1] += branch["size"][1] + 1

        else:
            branchPos[1] += branch["size"][1]

        isFirstBranch = False


def determineRelativePositionOfActions(sequence, startRow):
    """
        Determine the relative positions of action in the sequence.

        That is:
            Where should the item and its building blocks start and end,
            so that we can get the correct char in the correct place later
    """

    currentActionRow = startRow

    for action in sequence["actionList"]:
        if action["type"] == "on":
            determineRelativePositionOfOnAction(sequence, action, currentActionRow)
            currentActionRow += action["height"]

        elif action["type"] == "communication":
            determineRelativePositionOfCommunicationAction(sequence, action, currentActionRow)
            currentActionRow += action["height"]

        elif action["type"] == "variant":
            determineRelativePositionOfVariantAction(sequence, action, currentActionRow)
            currentActionRow += action["size"][1]

        else:
            fatalError(f"unknown action type {action['type']}")


def determineRelativePositions(sequence):
    """
        Determine the relative positions of all entities and actions.

        This means determine the following:
            startPos

            borderStartPos
            borderEndPos

            contentStartPos
            contentEndPos
            

        This must be done after the relevant sizing has been done

        Must also determine where content should start somewhere....


        TODO: add relative offset to both x and y
        
    """

    pos = [0,0]

    determineRelativePositionOfItems(sequence, pos)
            
    #Now header has been placed, place the timeLines for each entity
    addTimeLines(sequence)

    #Now place the actions. Their x-coordinates are calculated from
    #which entities they touch[sic]
    currentActionRow = sequence["headerHeight"] + sequence["marginToFirstAction"] 

    determineRelativePositionOfActions(sequence, currentActionRow)


def getCharFromOnAction(action, x, y):
    if action["startPos"][1] <= y <= action["endPos"][1] and \
       action["startPos"][0] <= x < action["endPos"][0]:
        if y <= action["contentStartPos"][1] and y >= action["contentEndPos"][1]:
            if x >= action["contentStartPos"][0] and x <= action["contentEndPos"][0]:
                debugPrint(f"{action['contentStartPos']} {action['contentEndPos']}")
                c = action["content"][x - action["contentStartPos"][0]]
                return [True, c]      

        #Border:
        r = getBorderChar(action, x, y)

        if r[0]:
            return r 

    #This is a hack to overwrite the | from the middleCol when padding is used
    # IE everything within borders that is not content, is " "
    if action["borderStartPos"][1] < y < action["borderEndPos"][1] and \
       action["borderStartPos"][0] < x < action["borderEndPos"][0]:
        return [True, " "]

        

    return [False, False]


def getCharFromCommunicationAction(action, x, y):
    if [x, y] == action["arrowPos"]:
        return [True, action["arrowChar"]]
    
    if y == action["lineStartPos"][1] and x >= action["lineStartPos"][0] and x <= action["lineEndPos"][0]:
        return [True, "-"]

    if y <= action["contentStartPos"][1] and y >= action["contentEndPos"][1]:
        if x >= action["contentStartPos"][0] and x <= action["contentEndPos"][0]:
            debugPrint(f"DEBUG: {action['contentStartPos']} {action['contentEndPos']}")
            c = action["content"][x - action["contentStartPos"][0]]
            return [True, c]      

    return [False, False]


def getCharFromVariantAction(action, x, y):
    if (action["startPos"][0] <= x <= action["endPos"][0]) and (action["startPos"][1] <= y <= action["endPos"][1]):

        #First check the inner stuff
        for branch in action["branchList"]:
            r = getContentChar(branch, x, y)
            if r[0]:
                return r
            
            r = getBorderChar(branch, x, y)
            if r[0]:
                return r

            for branch in action["branchList"]:
                for branchAction in branch["actionList"]: 
                    if branchAction["type"] == "on":
                        r = getCharFromOnAction(branchAction, x, y)
                        if r[0]:
                            return r

                    elif branchAction["type"] == "communication":
                        r = getCharFromCommunicationAction(branchAction, x, y)
                        if r[0]:
                            return r

                    elif branchAction["type"] == "variant":
                        r = getCharFromVariantAction(branchAction, x, y)
                        if r[0]:
                            return r
                    else:
                        fatalError("this should have been caught earlier... type {branchAction['type']} is illegal")

                if "branchBorderStart" in branch:
                    if y == branch["branchBorderStart"][1]:
                        if branch["branchBorderStart"][0] < x < branch["branchBorderEnd"][0]:
                            return [True, "-"] 

                        if x == branch["branchBorderEnd"][0]:
                            return [True, "+"]


        #Then get the borders
        r = getBorderChar(action, x, y)

        if r[0]:
            return r

    return [False, False]


def getCharFromAction(action, x, y):
    """
        Get a char from an action
    """

    if action["type"] == "on":
        r = getCharFromOnAction(action, x, y)
        if r[0]:
            return r

    elif action["type"] == "communication":
        r = getCharFromCommunicationAction(action, x, y)
        if r[0]:
            return r

    elif action["type"] == "variant":
        r = getCharFromVariantAction(action, x, y)
        if r[0]:
            return r

    else:
        fatalError(f"Not handled action {action['type']}")

    return [False, False]


def getSequenceGraph(sequence):
    """
        Get the sequence graph as a string
    """

    graphStringListList = []
    
    for rowNumber in range(sequence["height"]):
        graphStringList = []

        for colNumber in range(sequence["width"]):

            isCharFound = False

            if rowNumber < sequence["headerHeight"]:

                #timeLine can be in header as well, if there are containers
                #but timeLine takes precedence over container
                for timeLine in sequence["timeLineList"]:   
                    if rowNumber >= timeLine["rowStart"]: 
                        if colNumber == timeLine["column"]:
                            isCharFound = True
                            graphStringList.append("|") 
                            break
                    
                if isCharFound:
                    continue

                for i in sequence["itemList"]:
                    if rowNumber in range(i["startPos"][1], i["size"][1]):
                        [rc, c] = getCharFromItem(i, colNumber, rowNumber)
                        if rc:
                            debugPrint(f"{c} on {rowNumber} {colNumber}")
                            graphStringList.append(c) 
                            isCharFound = True
                            break
                    
                if isCharFound:
                    continue

            else:
                #Check for action

                for action in sequence["actionList"]:
                    [rc, c] = getCharFromAction(action, colNumber, rowNumber)
                    if rc:
                        graphStringList.append(c) 
                        isCharFound = True
                        break
                    pass

                if isCharFound:
                    continue

                #TimeLines
                for timeLine in sequence["timeLineList"]:   
                    if rowNumber >= timeLine["rowStart"]: 
                        if colNumber == timeLine["column"]:
                            isCharFound = True
                            graphStringList.append("|") 
                            break

                if isCharFound:
                    continue


            graphStringList.append(" ") 

        
        graphString = "".join(graphStringList)

        graphStringListList.append(graphString)

    return "\n".join(graphStringListList)


GLOBAL_BORDER_CORNER     = "+"
GLOBAL_BORDER_VERTICAL   = "|"
GLOBAL_BORDER_HORIZONTAL = "-"


def getContentChar(item, x, y):
    if y <= item["contentStartPos"][1] and y >= item["contentEndPos"][1]:
        if x >= item["contentStartPos"][0] and x <= item["contentEndPos"][0]:
            debugPrint(f"{item['contentStartPos']} {item['contentEndPos']}")

            charIndex = x - item["contentStartPos"][0]

            c = item["name"][charIndex]
            return [True, c]      

    return [False, False]


def getBorderChar(item, x, y):
    """
        Get a border char from an item (or an action...)
    """

    if y == item["borderStartPos"][1] and x == item["borderStartPos"][0]:
        return [True, GLOBAL_BORDER_CORNER]

    if y == item["borderEndPos"][1] and x == item["borderEndPos"][0]:
        return [True, GLOBAL_BORDER_CORNER]

    if y == item["borderEndPos"][1] and x == item["borderStartPos"][0]:
        return [True, GLOBAL_BORDER_CORNER]

    if y == item["borderStartPos"][1] and x == item["borderEndPos"][0]:
        return [True, GLOBAL_BORDER_CORNER]


    #then the top wall
    if y == item["borderStartPos"][1]:
        if x >= item["borderStartPos"][0] and x <= item["borderEndPos"][0]:
            return [True, GLOBAL_BORDER_HORIZONTAL]

    #The Bottom wall
    if y == item["borderEndPos"][1]:
        if x >= item["borderStartPos"][0] and x <= item["borderEndPos"][0]:
            return [True, GLOBAL_BORDER_HORIZONTAL]

    #The left wall
    if x == item["borderStartPos"][0]:
        if y >= item["borderStartPos"][1] and y <= item["borderEndPos"][1]:
            return [True, GLOBAL_BORDER_VERTICAL]

    #The right wall
    if x == item["borderEndPos"][0]:
        if y >= item["borderStartPos"][1] and y <= item["borderEndPos"][1]:
            return [True, GLOBAL_BORDER_VERTICAL]

    return [False, False]


def getCharFromItem(item, x, y):
    """
        Get a char from an item.

        If a char is found, will return:
        [True, <char>]

        else it returns:
        [False, False]


        I.E, if the item has a char that it wants to display on coords:

        [x, y]

        then it will return this char, otherwise it will return False :)
    """

    if item["type"] == "entity":
        r = getContentChar(item, x, y)
        if r[0]:
            return r

        r = getBorderChar(item, x, y)

        if r[0]:
            return r 
    
    elif item["type"] == "container":
        r = getContentChar(item, x, y)
        if r[0]:
            return r

        r = getBorderChar(item, x, y)

        if r[0]:
            return r 

        for subItem in item["itemList"]:
            r = getCharFromItem(subItem, x, y)
            if r[0]:
                return r

    else:
        fatalError(f"Unknown type: {item['type']}")

    return [False, False]



def addTimeLines(sequence):
    """
        Add the timeLines for each entity.

        That is, decide which col it should be at, 
        and where it should start in y-length.
    """

    timeLineList = []

    for i in sequence["entityList"]:
        if i["type"] == "entity":
            #Middle of the entity in terms of border, I.E size without margin
            middleOfEntity = i["borderStartPos"][0] + int((i["borderEndPos"][0] - i["borderStartPos"][0]) / 2) 
            oneBelowEntity = i["borderEndPos"][1] + 1

            timeLineList.append({"column":middleOfEntity, "rowStart":oneBelowEntity})

            i["timeLineCol"] = middleOfEntity
            
    sequence["timeLineList"] = timeLineList 
        

def getEntityWidth(entity):
    """
        Get the width of an entity.
        The margin can be altered later.

        The width is given by the 
            * content length
            * padding
            * border
            * margin
    """
    contentLength = len(entity["name"]) 

    return contentLength + \
           entity["padding"][1] + entity["padding"][3] +\
           entity["border"][1] + entity["border"][3] +\
           entity["margin"][1] + entity["margin"][3] 


def getInitialEntityHeight(entity):
    """
        Get the initial height of an entity.
        I wonder if this can change later though...?

        The width is given by the 
            * content height - this is always 1 as of now. but if we allow multiline content, must change this
            * padding
            * border
            * margin
    """
    contentHeight = 1 #As of now, content is only 1 line, NOTE: this might not be true in the future if allow multiline content

    return contentHeight +\
           entity["padding"][0] + entity["padding"][2] +\
           entity["border"][0] + entity["border"][2] +\
           entity["margin"][0] + entity["margin"][2]


def determineSizeOfEntity(entity):
    """
        Determines both the height and width of an entity.
        This is done by adding up content, padding, border, and margin
    """

    entity["size"] = [0, 0] 

    entity["size"][0] = getEntityWidth(entity)

    entity["size"][1] = getInitialEntityHeight(entity) 
            
    entity["width"]  = entity["size"][0]
    entity["height"] = entity["size"][1]

    entity["widthNoMargin"] = entity["width"] - entity["margin"][1] - entity["margin"][3]


def determineSizeOfActions(sequence):
    """
        Determine both the height and width of actions.

        The width can later be used to resize the width of entities.
        This can be a little bit tricky, but is doable.
        
    """
    for action in sequence["rawActionList"]:

        if action["type"] == "on":
            determineSizeOfOnAction(action)

        elif action["type"] == "communication":
            determineSizeOfCommunicationAction(action)
            
        else:
            fatalError("error only 'on', and 'communication' supported now") 



def determineSizeOfOnAction(action):
    """
        Get the size (width, height) of an "on"-action.

        Return the size calculated as:
        [width, height]
    """

    if "border" not in action:
        action["border"] = [1, 1, 1, 1]

    if "padding" not in action:
        action["padding"] = [0, 0, 0, 0]

    if "margin" not in action:
        action["margin"] = [0, 0, 0, 0]

    width = len(action["content"]) + action["border"][3] + \
                                     action["border"][1] + \
                                     action["padding"][1] + \
                                     action["padding"][3] + \
                                     action["margin"][1] + \
                                     action["margin"][3]

    #Now, content is only allowed to be 1 high :/
    contentHeight = 1

    height = contentHeight + action["border"][0] + action["border"][2] + \
                             action["padding"][0] + action["padding"][2] + \
                             action["margin"][0] + action["margin"][2]

    action["size"] = [width, height]

    action["width"] = width

    action["height"] = height

    return [width, height]


def determineSizeOfCommunicationAction(action):
    """
        Get the size of a "communication" action

        return the size as:
        [width, height]
    """

    action["width"] = len(action["content"]) + 2  #This is a travesty :( should be padding instead

    if "margin" not in action:
        action["margin"] = [0,0,1,0]

    action["height"] = 2 + action["margin"][2] + action["margin"][0]

    action["size"] = [action["width"], action["height"]]

    return action["size"] 


def determineSizeOfVariantAction(action):
    """
        Get the size of a variant

        TODO: this will involve going through the branchList
        calculating the sizes of the induvidual items 
        and take sums and max of certain values
    """

    if "border" not in action:
        action["border"] = [1, 1, 1, 1]

    if "padding" not in action:
        action["padding"] = [0, 0, 0, 0]

    if "margin" not in action:
        action["margin"] = [0, 0, 0, 0]


    width = 0

    #Go through all branches in variant
    for branch in action["branchList"]:
        nameLen = len(branch["name"]) 

        actionWidth = 0
        for action in branch["actionList"]:
            if action["type"] == "on":
                [width, height] = determineSizeOfOnAction(action)
            
            elif action["type"] == "communication":
                [width, height] = determineSizeOfCommunicationAction(action)
    
            elif action["type"] == "variant":
                [width, height] = determineSizeOfVariantAction(action)
        
            else:
                fatalError(f"Unknown action type: {action['type']}")

            actionWidth += width


def getEntityWithId(sequence, id):
    for i in sequence["entityList"]:
        if i["type"] == "entity":
            if i["id"] == id:
                return i

        else:
            fatalError("still only entities allowed")
    
    fatalError(f"entity with id {id} does not exist")


def getItemsBetween(sequence, entityAId, entityBId):
    """
        Get all identities between entityA and entityB.

        both entityA and entityB can lie within containers,
        and there can be containers between them as well.
        
        Thus return the items between (including A and B),
        in the order of appearance from left to right

        Example: 

        +---------+  +---+  +---+  +---------+
        | entityA |  | K |  | P |  | entityB |
        +---------+  +---+  +---+  +---------+
             |         |      |         |
             |         |      |         |
             |         |      |         |

        Returns [entityA, K, P, entityB]

        Also the order of the entities doesn't matter
    """

    #Get first entity in order of A and B.

    entityList = []

    for entity in sequence["entityList"]:
        if (entity["id"] == entityAId) or (entity["id"] == entityBId):
            entityList.append(entity)

    if len(entityList) != 2:
        fatalError("must have at least 2 entities between each other")

    if entityList[0] == entityList[1]:
        fatalError("Both entities cannot be the same though...")

    familyTreeListList = [getFamiliyTreeList(entityList[0]), getFamiliyTreeList(entityList[1])]

    commonAncestor = getCommonAncestor(familyTreeListList[0], familyTreeListList[1])

    #print(f"commonAncestor {commonAncestor}")

    startItem = entityList[0]

    endItem = entityList[1]

    if familyTreeListList[0] != familyTreeListList[1]:

        if len(familyTreeListList[0]) > 1:
            startItem = familyTreeListList[0][familyTreeListList[0].index(commonAncestor)-1]

        if len(familyTreeListList[1]) > 1:
            endItem = familyTreeListList[1][familyTreeListList[1].index(commonAncestor)-1]
        

    itemList = []

    itemList.append(startItem) 

    nextItem = startItem["nextSibling"]

    while nextItem != endItem:
        itemList.append(nextItem)
        nextItem = nextItem["nextSibling"]

    itemList.append(endItem)

    return itemList


def getFamiliyTreeList(item):
    """
        Get a list of parent, grand parent, great grandparent, and so on ...    

        The last element in the list will always be None, 
        since that is the top element (root)
    """

    p = item["parent"]

    familyTreeList = []

    while p != None:
        familyTreeList.append(p)

        p = p["parent"]

    familyTreeList.append(p)


    return familyTreeList
        

def getCommonAncestor(familyTreeAList, familyTreeBList):
    """
        Given two family trees,
        return the first common parent to both families
    """

    for ancestor in familyTreeAList:
        if ancestor in familyTreeBList:
            return ancestor

    fatalError("two entites without common ancestor... how defuq is that possible :(")


def getRightTraversalDistance(item, stopItem):
    """
        Traverse Right and get the distance from item (excluding),
        until we reach a point where the stopItem is our parent
    """

    if item["parent"] == stopItem:
        return 0

    
    nextItem = item["nextSibling"] 

    if nextItem != None:
        #There is a next sibling. Add this in full
        return nextItem["width"] + getRightTraversalDistance(nextItem, stopItem)

    else:
        nextItem = item["parent"]

        if nextItem == None:
            #We reached the ceiling.
            return 0 
    

        #nextItem must be a container... right?

        if nextItem["type"] != "container":
            fatalError("must be a container, or something is terribly broken :(")


        #Add the right side of this container
        toAdd = nextItem["padding"][1] + nextItem["border"][1] + nextItem["margin"][1]

        return toAdd + getRightTraversalDistance(nextItem, stopItem)


def getLeftTraversalDistance(item, stopItem):

    """
        Traverse Left and get the distance from item (excluding),
        until we reach a point where the stopItem is our parent

        That is:

        +---+   +---+   +---+   +---+
        | A |   | B |   | C |   | D |
        +---+   +---+   +---+   +---+
                                  ^
                                  |
                <-- Traverse -- START

                Adding all the left side margins
                From D out.

    """

    if item["parent"] == stopItem:
        return 0

    nextItem = item["previousSibling"] 

    if nextItem != None:
        #There is a next sibling. Add this in full 
        #(doesn't matter if it be a entity or container)
        return nextItem["width"] + getLeftTraversalDistance(nextItem, stopItem)

    else:
        nextItem = item["parent"]

        if nextItem == None:
            #We reached the ceiling.
            return 0 
    
        #nextItem must be a container... right?

        if nextItem["type"] != "container":
            fatalError("must be a container, or something is terribly broken :(")


        #Add the left side of this container
        toAdd = nextItem["padding"][3] + nextItem["border"][3] + nextItem["margin"][3]

        return toAdd + getLeftTraversalDistance(nextItem, stopItem)
    

def getEntityCC(sequence, firstEntity, secondEntity):
    """
        Get the Centrum-Centrum distance between two entities...
        Also, it is the distance between NOT INCLUDING 

        +-----+      +-----+
        |  A  |      |  B  |
        +-----+      +-----+
           |     CC     |
           |<---------->|
           |            |

        NB: this is done BEFORE relative positions have been established...
        This means that we are working on temporary data,
        and widths can change depending on how this process goes.

        I.E if a communication does not fit, we must make room for it...
        That means increasing one or more entities margins.

        Thus this function gives the CC as it is right at this moment in the process

        Added unit test for this one since I messed it up first... :(
    """

    if firstEntity == secondEntity:
        #There is no distance between the same entity :)
        return 0

    entitiesToCC = [firstEntity, secondEntity]

    cc = 0

    #Must always add the halfes:

    #Add the second half of A:
    [_, rightSide] = getEntitySides(entitiesToCC[0])
    toAdd = rightSide
    cc += toAdd 

    #Add the first half of B:
    [leftSide, _] = getEntitySides(entitiesToCC[1])
    toAdd = leftSide 
    cc += toAdd

    #Then we must find the common ancestor of both entities.
    #Then, we add "inbetweeners" within that common ancestor... 
    #
    #Example:
    #
    # Lets saye we are looking for CC between a and b, that are
    # within container A and B respectively (or one is just plain: A == a or B == b):
    # And A K W and B are within the same ancestor here (have the same parent)

    #    +---+   +---+   +---+   +---+
    #    | A |   | K |   | W |   | B |
    #    +---+   +---+   +---+   +---+
    #      |<---------[CC]-------->|
    #
    #  The inbetweeners here are K and W  
    #  (that can be either containers or entities, doesn't matter)

    #Then we also need the distance "out" from A into the common ancestor.
    #Let's say A is build like this:
    #
    #       +--------------+
    #       | +---+  +---+ |
    #       | | a |  | k | |
    #       | +---+  +---+ |
    #       +--------------+ 
    #        
    # The distance from a out, is 
    # width of k + the right side of its parent (padding, border, margin)

    # The same concept occurs for b (if it is in a container), 
    # but the left side of parent(s)

    entityAFamilyTreeList = getFamiliyTreeList(entitiesToCC[0])
    entityBFamilyTreeList = getFamiliyTreeList(entitiesToCC[1])

    commonAncestor = getCommonAncestor(entityAFamilyTreeList, entityBFamilyTreeList)

    #First, find where A is relative to the common ancestor

    startBetween = None

    i = entityAFamilyTreeList.index(commonAncestor)

    if i == 0:
        #This lies plain, start from it
        startBetween = entitiesToCC[0]

    else:
        #We need to traverse like a good boi. 
        #"To the right to the right,
        # Everything is in a box to the right"
        startBetween = entityAFamilyTreeList[i-1] 


    #Now find where B is relative to the common ancestor
    i = entityBFamilyTreeList.index(commonAncestor)

    endBetween = None

    if i == 0:
        #This lies plain, end on it
        endBetween = entitiesToCC[1]

    else:
        #We need to traverse like a good boi. backwards
        endBetween = entityBFamilyTreeList[i-1] 

    nextItem = startBetween["nextSibling"]

    #Add all inbetweeners
    while nextItem != endBetween:
        toAdd = nextItem["width"]
        cc += toAdd
        nextItem = nextItem["nextSibling"]

    #The distance out from
    toAdd = getRightTraversalDistance(entitiesToCC[0], commonAncestor) 
    cc += toAdd

    #The distance out to
    toAdd = getLeftTraversalDistance(entitiesToCC[1], commonAncestor) 
    cc += toAdd

    return cc


def getFromAndToEntities(sequence, fromEntityId, toEntityId):
    """
        Get two entities, in order of appearance in the entityList.
        That means that the from/to order could be "swapped"

        Returns:
            [firstEntity, secondEntity]
    """
    entityList = []

    for entity in sequence["entityList"]:
        if entity["id"] in [fromEntityId, toEntityId]:
            entityList.append(entity)

    if len(entityList) != 2:
        fatalError(f"Could not find entites for ID from: {fromEntityId} and to: {toEntityId}")

    if entityList[0]["id"] == entityList[1]["id"]:
        fatalError(f"two entities share the same ID: {entityList[0]['id']}")

    return entityList


def getEntitiesSpanned(sequence, communication):
    """
        Return the number of entites this communication spans.
        
        I.E if it travels between A and B and between them is C, D and K,
        it spans 3 entities
    """
    isStarted = False
    numSpanned = 0

    for entity in sequence["entityList"]:
        if isStarted:
            numSpanned += 1 

        if entity in [communication["fromEntityId"], communication["toEntityId"]]:
            if isStarted:
                numSpanned -= 1
                break

            else:
                isStarted = True

    return numSpanned


def commSorter(i):
    """
        If only I knew how to make lambdas...
        oh, well
    """
    return i["numSpanned"]


def sortCommunications(sequence):
    """
        This will sort on the side of the actual,
        in order to minimize the width-expansion due to communications being to big to fit.

        So in essence,
        When we scale things, we start with the communications that span as few elements as possible,
        which should decrease the width that needs to be added to accomodate them...
        
        But hey, this is just a theory. A code theory
    """
    communicationsList = []

    for action in sequence["rawActionList"]:
        if action["type"] == "communication":
            numEntitiesSpanned = getEntitiesSpanned(sequence, action) 
            action["numSpanned"] = numEntitiesSpanned
            communicationsList.append(action)

    communicationsList.sort(key=commSorter)
    return communicationsList 


def getVariantContentWidth(variant):
    """
        Gets the content width of an variant.
        
        Content width is the largest branch-name in branchList
        No padding, no margin, no nothing...
        Maybe that is needed for full functionality... who knows.
    """
    contentWidth = 0
    for branch in variant["branchList"]:
        if len(branch["name"]) > contentWidth:
            contentWidth = len(branch["name"])

    return contentWidth


def resizeByVariantSingleEntity(sequence, variant):
    """
        This is a special case.
        
        The variant is only over a single entity

            +---+ 
            | e |
            +---+
           L  |  R
        <---->|<--->
        +----------+
        | B | |    |
        +---+ |    |
        |+--------+|
        || action ||
        |+--------+|
        |     |    |
        +----------+
              |
              M
    
        Depending on if L (left) and R (right) from M (middleCol)
        falls within e's (entity's) size (margin+border+padding+content),
        we need to resize e. 
    
        If L is outside of e, then we increase left-padding for e.
        If R is outside of e, then we increase right-padding for e. 
    """

    entity = variant["toEntity"]

    #Check if variant content can fit at all

    variantElementWidth = variant["border"][1]  + \
                          variant["border"][3]  + \
                          variant["padding"][1] + \
                          variant["padding"][3] + \
                          variant["margin"][1]  + \
                          variant["margin"][3]

    widthBySides = variant["left"] + 1 + variant["right"] - 2 #+1 for middle col, -2 for "start"

    contentWidth = getVariantContentWidth(variant)

    variantWidth = widthBySides 

    if contentWidth > widthBySides:
        #Change left and right
        variantWidth = contentWidth
        toAdd = contentWidth - widthBySides 
        #print(f"{variant['branchList'][0]['name']} contentWidth is bigg {contentWidth}")
        variant["right"] += int((toAdd + 1) / 2)
        variant["left"]  += int(toAdd / 2)
        #print(f"{variant['left']} {variant['right']}")
        
    entitySizeNoCol = entity["size"][0] - 1 #Remove the middle col from the equation


    #now check if we need to add anything to the entity because of sides

    [entityLeft, entityRight] = getEntitySides(entity)

    rightEntitySide = entityRight 
    leftEntitySide  = entityLeft 

    fullLeftSide = variant["left"] + variant["border"][3] + variant["padding"][3] + variant["margin"][3] - 1

    if fullLeftSide > leftEntitySide: 
        #Increase margin to make room for the variant
        entity["margin"][3] += (fullLeftSide - leftEntitySide)
        
    fullRightSide = variant["right"] + variant["border"][1] + variant["padding"][1] + variant["margin"][1] - 1
    
    if fullRightSide > rightEntitySide:
        #Increase margin to make room for the variant
        entity["margin"][1] += (fullRightSide - rightEntitySide) 

    #Change the entity size
    determineSizeOfEntity(entity)

    variant["size"][0] = variantWidth + variantElementWidth 
    #print(f"variantSize: {variant['size']}")
    #print(f"entitySize: {variant['fromEntity']['size']}")


def getEntityRight(entity):
    """
        Return entity right
    """
    contentLenRight = int(len(entity["name"]) / 2)


    return contentLenRight + entity["border"][1] + entity["padding"][1] + entity["margin"][1]


def getEntityLeft(entity):
    """
        Return entity left
    """
    contentLenLeft = int(len(entity["name"]) / 2)

    if len(entity["name"]) % 2 == 0:
        contentLenLeft -= 1

    #Since we (or I) decided (well, it sort of happend),
    #that the middle column should be weighted towards the left
    #an even content length will lead to middle column being 1 step closer to left
    #if len(entity["name"]) % 2 == 0:
    #    contentLenLeft -= 1

    return contentLenLeft + entity["border"][3] + entity["padding"][3] + entity["margin"][3]


def getEntitySides(entity):
    """
        M  B P    C   P B  M
       <-->*<-><----><->*<--> 
           +------------+
           |   entity   |
           +------------+
                 |
       <-------->m<--------->
            L          R

        M - Margin
        m - middleCol
        B - Border
        P - Padding
        C - Content

        L - left
        R - Right
        
        This returns [L, R]
    """
    return [getEntityLeft(entity), getEntityRight(entity)]


def getVariantLeft(variant):
    return variant["left"] + variant["border"][3] + variant["padding"][3] + variant["margin"][3] - 1

def getVariantRight(variant):
    return variant["right"] + variant["border"][1] + variant["padding"][1] + variant["margin"][1] - 1


def resizeByVariantManyEntitites(sequence, variant):
    """
        Aight. What are we trying to accomplish here...?
    """

    #fatalError("resize variant many entities")

    #Check if we need to add anything to the entity because of 
    #sides

    fromEntity = variant["fromEntity"]
    toEntity = variant["toEntity"]

    [entityLeft, _] = getEntitySides(fromEntity)
    [_, entityRight] = getEntitySides(toEntity)

    fullVariantLeft  = getVariantLeft(variant) 
    fullVariantRight = getVariantRight(variant) 


    if fullVariantLeft > entityLeft:
        #Increase margin to make room for the variant
        fromEntity["margin"][3] += fullVariantLeft - entityLeft

        determineSizeOfEntity(fromEntity)
        #Get the new entityLeft
        [entityLeft, _] = getEntitySides(fromEntity)
    

    if fullVariantRight > entityRight:
        #Increase margin to make room for the variant
        toEntity["margin"][1] += fullVariantLeft - entityRight 

        determineSizeOfEntity(toEntity)
        #Get the new entityRight
        [_, entityRight] = getEntitySides(toEntity)


    #Now we also need to take into account the variant content

    cc = getEntityCC(sequence, 
                     fromEntity, 
                     toEntity)    

    totalWidthToFitInto = cc + 1 + 1 + entityLeft + entityRight

    contentWidth = getVariantContentWidth(variant)

    variantStyleWidth = variant["border"][1] + \
                        variant["border"][3] + \
                        variant["padding"][1] + \
                        variant["padding"][3] + \
                        variant["margin"][1] + \
                        variant["margin"][3]

    totalVariantWidth = contentWidth + variantStyleWidth + variant["left"] + variant["right"] - 1 - 1

    if totalVariantWidth > totalWidthToFitInto:
        #ok increase CC:
        distanceToAdd = totalVariantWidth - totalWidthToFitInto 
        addCC(sequence, fromEntity, toEntity, distanceToAdd)

    cc = getEntityCC(sequence, 
                     fromEntity, 
                     toEntity)    

    #print(f"{variant['left']} {cc} {variant['right']}")
    #Ok, this looks extremly retarded. but that's only because it mirrors the author thought-pattern.
    #add 1 for fromEntity middleCol, 1 for toEntity middleCol, but then remove 1 for each side (left, right)...
    variant["size"][0] = variant["left"] + cc + variant["right"] + 1 + 1 + variantStyleWidth - 1 - 1 

    
def resizeByVariant(sequence, variant):
    """
        Resize entities by variants.

        We have already set the height of the variants,
        the sides of every variant (recursively),
        and we have already taken into account CC-increasage due to "atomic actions"...

        Thus, all that is left is to check if variants fits on, or between entityies,
        given the content length of the variant (the largest branch name),
        and the sides (left, right), since we can end up starting variant quite 
        far away from middle column if we have big "on"-actions,
        or many recursive variants within one another.

        If left or right ends up being to far out (outside of entityes width),
        we will increase that entities margin to accomodate the variant.
        Now, that is arbitrary, but probably the simplest solution.


        There are 2 distinct cases:
            1. The variant is over one single entity
            2. The variant is over more than one entity

        They are handled separetly for convenience :)

        Hope this works. Hope leaves us last

    """
    #Every action resized their respective stuff already.
    for branch in variant["branchList"]:
        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":
                resizeByVariant(sequence, branchAction)

    if variant["fromEntity"] == variant["toEntity"]:
        resizeByVariantSingleEntity(sequence, variant)

    else:
        resizeByVariantManyEntitites(sequence, variant)


def addCC(sequence, fromEntity, toEntity, distanceToAdd):
    """
        Add distance (centrum-centrum) between two entities.

        TODO: explain how this is done, and why...
    """

    #Aigh then. We gonna need all involved mfs here.
    #Also a good chance I'm off by one (or two here)
    itemList = getItemsBetween(sequence, 
                               fromEntity["id"], 
                               toEntity["id"])

    distanceNeeded = action["width"] - cc 

    if distanceToAdd % 2 == 1:
        #Ok. Need one more if uneven to get 1 margin in both directions on signal-content
        distanceToAdd += 1

    #Ok. We can be really clever here, and sort of get the proportional increase per item,
    #or we can go with the easy route and just distribute them evenly.
    #easy route, I choose you

    distanceToAddEachItem = int(distanceToAdd / len(itemList))

    isFirstEntity = True

    for item in itemList[:-1]:
        if isFirstEntity:
            debugPrint(f"Adding {distanceToAddEachItem} to {item['name']}")
            item["margin"][1] += distanceToAddEachItem + distanceToAddEachItem % 2

        else:
            #Distribute evently beteween left and right margin. 
            #if uneven. right will get the extra.
            item["margin"][1] += int(distanceToAddEachItem / 2) + distanceToAddEachItem % 2
            item["margin"][3] += int(distanceToAddEachItem / 2)

        
        if item["type"] == "entity":
            determineSizeOfEntity(item)

        else:
            determineSizeOfContainer(item)

        isFirstEntity = False

    debugPrint(f"Adding {distanceToAddEachItem + distanceToAddEachItem % 2} to {itemList[-1]['name']}")

    itemList[-1]["margin"][3] += distanceToAddEachItem + distanceToAddEachItem % 2


    if itemList[-1]["type"] == "entity":
        determineSizeOfEntity(itemList[-1])

    else:
        determineSizeOfContainer(itemList[-1])

    entityList = []

    for entity in sequence["entityList"]:
        if (entity["id"] == action["fromEntityId"]) or (entity["id"] == action["toEntityId"]):
            entityList.append(entity)
    
    #This is a travesty... should really nicen'[tm] things up...
    #I mean, in the CC-calc the family trees are already there. Should mayhaps add familyTrees to
    #the elements themselfs at the start, since it is a static feature.
    familyTreeListList = [getFamiliyTreeList(entityList[0]), getFamiliyTreeList(entityList[1])]

    commonAncestor = getCommonAncestor(familyTreeListList[0], familyTreeListList[1])

    #This is a bit of a hack I feel like :(
    #But it works, so don't touch :|
    if commonAncestor != None:
        determineSizeOfContainer(commonAncestor)
        p = commonAncestor["parent"]
        while p:
            determineSizeOfContainer(p)
            p = p["parent"]


def resizeItemWidth(sequence):
    """
        Go through all actions and see if any entities needs to be resized.

        And if they do need to be resized, resize them :)
        Light weight.
    """

    #First. go with the on-actions
    #These will resize their respective entity
    for action in sequence["rawActionList"]:
        if action["type"] == "on":
            entity = getEntityWithId(sequence, action["entityId"])

            if action["width"] > entity["width"]:
                entity["margin"][1] = entity["margin"][1] + int((action["width"] - entity["widthNoMargin"]) / 2)
           
                #Ok. I'm a bit unsure if I should add here or above, but I'll try here :)
                entity["margin"][3] = entity["margin"][3] + int((action["width"] - entity["widthNoMargin"] + 1) / 2)

                if entity["parent"] != None:
                    familyTreeList = getFamiliyTreeList(entity)
                    determineSizeOfContainer(familyTreeList[-2])

                else:
                    determineSizeOfEntity(entity)

    #Now for the communications

    #Sort to minimize width introduction
    communicationList = sortCommunications(sequence)

    for action in communicationList:
        if action["type"] == "communication":

            [firstEntity, secondEntity] = getFromAndToEntities(sequence, 
                                                               action["fromEntityId"], 
                                                               action["toEntityId"])

            cc = getEntityCC(sequence, firstEntity, secondEntity)  

            if action["width"] > cc:
                
                distanceToAdd = action["width"] - cc 

                addCC(sequence, firstEntity, secondEntity, distanceToAdd)


    for action in sequence["actionList"]:
        if action["type"] == "variant":
            resizeByVariant(sequence, action)


    #Resize all communications now that items in header are resized
    #The header is always the one making the calls
    for action in sequence["rawActionList"]:
        if action["type"] == "communication":
            
            [firstEntity, secondEntity] = getFromAndToEntities(sequence, 
                                                               action["fromEntityId"], 
                                                               action["toEntityId"])

            cc = getEntityCC(sequence, firstEntity, secondEntity)    
            #print(f"action {action['content']} width {cc}")
    
            action["width"] = cc 
            action["size"][0] = cc

    


def determineSizeOfContainer(container):
    """
        Determine the size of a container,

        Should this be used to resize later? maybe :)
    """
    determineSizeOfItemList(container["itemList"])

    #Get the total height (largest height in itemList) in itemLsit,
    #Get the total width (the sum of all items in itemList (+margin)) in itemList

    height = 0
    width  = 0

    for item in container["itemList"]:
        if item["height"] > height:
            height = item["height"] 

        width += item["width"]

    height += 1 + \
              container["border"][0] + container["border"][2] + \
              container["padding"][0] + container["padding"][2] + \
              container["margin"][0] + container["margin"][2] 

    if width < len(container["name"]):
        width = len(container["name"])

    width += container["border"][1] + container["border"][3] + \
             container["padding"][1] + container["padding"][3]

    container["widthNoMargin"] = width 

    container["width"] =  container["widthNoMargin"] + \
                          container["margin"][1] + container["margin"][3]

    container["height"] = height

    container["size"] = [container["width"], container["height"]]

    debugPrint(f"height: {height} width: {width}")


def determineSizeOfItemList(itemList):
    for item in itemList:
        
        #Set default padding, margin and border if nothing is specified.
        #This is done on every item-type
        if "padding" not in item:
            item["padding"] = [0, 0, 0, 0]

        if "margin" not in item:
            item["margin"] = [0, 0, 0, 0]

        if "border" not in item:
            item["border"] = [1, 1, 1, 1] 
        
        if item["type"] == "entity":
            #Here we will set the item height, which will persist throughout.
            #We also set the item width, but that might change later.
            determineSizeOfEntity(item)

        elif item["type"] == "container":
            determineSizeOfContainer(item)


def initializeItemPositions(itemList):
    """
        Set all items positions to -1.
        This will be changed later when the layout is calculated.
    """

    for item in itemList:
        #Positions will be determined later
        item["startPos"]  = [-1, -1]
        item["endPos"]    = [-1, -1]

        if item["type"] == "container":
            initializeItemPositions(item["itemList"])


def initializeHierarchy(itemList, parent=None):
    """
        Initialize the parent<->child relationship
        between items. 

        Also initializes the sibling relationships within each container.
    
        For example:
        A container is a parent to one/many containers and/or entities
    """
    #Parent hierarchy
    for item in itemList:
        item["parent"] = parent 

        item["nextSibling"]         = None
        item["previousSibling"]     = None

        if item["type"] == "container":
            initializeHierarchy(item["itemList"], item)

    #sibling relations ship
    for item, nextItem in zip(itemList, itemList[1:]):
        item["nextSibling"]         = nextItem
        nextItem["previousSibling"] = item


def getItemsInContainer(container):
    """
        Return the items in a container in the order of apperance
    """
    entityList = []

    for item in container["itemList"]:
        if item["type"] == "entity":
            entityList.append(item)

        elif item["type"] == "container":
            entityList.extend(getItemsInContainer(item))

    return entityList


def initializeEntityList(sequence):
    """
        Puts all entities in a sequential list.
        
        This makes it easier to work with later on.

        Each entity gets a reference to the next and previous entity.
        This is retarded, since you should be able to just traverse the list... anyways...
    """
    entityList = []

    for item in sequence["itemList"]:
        if item["type"] == "entity":
            entityList.append(item)

        elif item["type"] == "container":
            entityList.extend(getItemsInContainer(item))

    for entity, nextEntity in zip(entityList, entityList[1:]): 
        entity["nextEntitySibling"]         = None
        entity["preiousEntitySibling"]      = None
        nextEntity["nextEntitySibling"]     = None
        nextEntity["previousEntitySibling"] = None

        if entity["parent"] == nextEntity["parent"]:
            entity["nextEntitySibling"] = nextEntity 
            nextEntity["previousEntitySibling"] = entity 

        debugPrint(entity)

    sequence["entityList"] = entityList


def initializeEntities(sequence):
    """
        Given an input json-file,
        set all default sizes of entities.

        This might change later when we recalculate the widths 

        However, the height (of the header) will be calculated here,
        and will not change later. 
    
        Thus the header-size will be determined here and never changed later.

        Also sets positions to a default value [-1, -1]
    """

    determineSizeOfItemList(sequence["itemList"])

    initializeItemPositions(sequence["itemList"])

    initializeHierarchy(sequence["itemList"])

    initializeEntityList(sequence)


def getFirstEntityInSet(sequence, s):
    """
        Given s is a set of entityIds,
        gives the id from that set that is first found in entityList
    """
    for i in sequence["entityList"]:
        if i["id"] in s:
            return i

    fatalError(f"Could not get any entity with id in set: {s}")


def getLastEntityInSet(sequence, s):
    """
        Given s is a set of entityIds,
        gives the id from that set that is last found in entityList
    """
    for i in sequence["entityList"][::-1]:
        if i["id"] in s:
            return i

    fatalError(f"Could not get any entity with id in set: {s}")


def setStartAndEndEntityForVariant(sequence, variant):
    """
        Ok. Get the first and last entity (in the order of header)
        that this variant covers. Does it recursively throughout it,
        so all subvariants will also be set.

        After this, variants here will have attributes:

            fromEntityId
            toEntityId

        set, and ready to go!
    """

    variant["size"] = [0, 0]

    entityIdSet = set() 
        
    for branch in variant["branchList"]:

        branch["size"] = [0, 0]

        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":
                setStartAndEndEntityForVariant(sequence, branchAction)
    
                entityIdSet.add(branchAction["fromEntity"]["id"])
                entityIdSet.add(branchAction["toEntity"]["id"])

            elif branchAction["type"] == "on":
                entityIdSet.add(branchAction["entityId"])

            elif branchAction["type"] == "communication":
                entityIdSet.add(branchAction["fromEntityId"])
                entityIdSet.add(branchAction["toEntityId"])

            else:
                fatalError(f"type {branchAction['type']}")
    
    variant["fromEntity"] = getFirstEntityInSet(sequence, entityIdSet)
    variant["toEntity"]   = getLastEntityInSet(sequence, entityIdSet)

    #print(f"from: {variant['fromEntity']['name']} <-> {variant['toEntity']['name']}")


def getOnActionSides(onAction):
    """
        Return how much this entity sticks out each side from middle column.
        
        This is including margin, border, padding.

                 |                  |
                 |                  |
              +----+             +-----+
              |    |             |     |
              +----+             +-----+
                 |                  |

      returns [3, 2]             [3, 3]
    """

    sizeToSplit = onAction["size"][0] - 1 #Remove the middleCol from the equation

    left    = int((sizeToSplit) / 2)
    right   = int((sizeToSplit) / 2)

    #print(f"On Action: left: {left} right: {right}")

    if onAction["size"][0] % 2 == 0:
        left += 1

    return [left, right]



def setVariantSides(sequence, variant):
    """
        Set variant left and right addage.
        I.E how far away of middle column of entity this variant have to start.
    
        Protip: I don't know what I'm doing
    """


    height = variant["margin"][0] + variant["margin"][2] +\
             variant["border"][0] + variant["border"][2] +\
             variant["padding"][0] + variant["padding"][2]

    left  = 0
    right = 0

    isFirstBranch = True

    for branch in variant["branchList"]:

        branchHeight = 0

        if isFirstBranch:
            branchHeight = 2

        else:
            #Next branches also has a top border to separate them.
            branchHeight = 3

        isFirstBranch = False

        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":

                [vLeft, vRight, leftEntity, rightEntity] = setVariantSides(sequence, branchAction)

                if leftEntity == variant["fromEntity"]:
                    if vLeft > left:
                        left = vLeft

                if rightEntity == variant["toEntity"]:
                    if vRight > right:
                        right = vRight

                branchHeight += branchAction["size"][1]

                #If we are on single entity, need to expand our left and right when we go hard or go home
                #with the name of branches b long
                if variant["fromEntity"] == variant["toEntity"]:
                    for subBranch in branchAction["branchList"]:
                        #FIXME: account for margin n' stuff here right? or there is none on each branch
                        subBranchContentWidth = len(subBranch["name"])
                        if (left + 1 + right - 2) < subBranchContentWidth:
                            toAdd = subBranchContentWidth - (left + 1 + right - 2)

                            left  += int(toAdd / 2)
                            right += int((toAdd + 1) / 2)


            elif branchAction["type"] == "on":
                branchHeight += branchAction["size"][1]

                [onLeft, onRight] = getOnActionSides(branchAction)

                if variant["fromEntity"] == variant["toEntity"]:
                    if branchAction["entityId"] == variant["fromEntity"]["id"]:

                        if onLeft > left:
                            left = onLeft

                        if onRight > right:
                            right = onRight

                elif branchAction["entityId"] == variant["fromEntity"]["id"]:
                    if onLeft > left:
                        left = onLeft

                elif branchAction["entityId"] == variant["toEntity"]["id"]:
                    if onRight > right:
                        right = onRight

                else:
                    #This on is in middle somwhere, no action needed :)
                    pass
                    

            elif branchAction["type"] == "communication":
                #A communication take no room on sides
                branchHeight += branchAction["size"][1]

            else:
                fatalError(f"ERROR: type {branchAction['type']}")

            branch["size"][1] = branchHeight

        height += branchHeight

    variant["size"][1] = height

            
    #So in essence, left is where this should start left side, 
    #and right where it shall start right side.
    #and by start I mean where the inner element ends + 1
    variant["left"]    = left + 1
    variant["right"]   = right + 1


    #print(f"left: {variant['left']} | | | {variant['right']} ")
    #print(f"{variant['margin']} {variant['border']} {variant['padding']}")

    return [variant["left"], variant["right"], variant["fromEntity"], variant["toEntity"]]


def setVariantStyle(variant):
    setStyle(variant)
    for branch in variant["branchList"]:
        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":
                setVariantStyle(branchAction)


def initializeVariant(sequence, variant):
    """
        Initialize a particular variant
    """
    setVariantStyle(variant)

    setStartAndEndEntityForVariant(sequence, variant)

    setVariantSides(sequence, variant)


def initializeVariants(sequence):
    """
        Initialize every variant

        Will figure out which entity is the first and last
        of each variant.

        I think this is the only way of doing things.
        And then in the end we can adjust entity width depending on the
        variant configuration
    """
    
    
    for a in sequence["actionList"]:
        if a["type"] == "variant":
            initializeVariant(sequence, a)


def getActionsInVariant(variant):
    """
        Go through the actions within the variant in order
        and put them in a list that is returned.
    """
    aList = []

    for branch in variant["branchList"]:
        for branchAction in branch["actionList"]: 
            if branchAction["type"] in ["on", "communication"]:
                aList.append(branchAction)

            elif branchAction["type"] == "variant":
                aList.extend(getActionsInVariant(branchAction))

            else:
                fatalError("NEJ")

    return aList


def buildRawActionList(sequence):
    """
        the naming is not perfect... But rawActionList are all non-container-type actions...
        easy right :D I.E all actions not of type variant right now

        So this function builds that list => sequence['rawActionList']
        with all 'atomic' actions in order of appearance
    """
    rawActionList = []

    for action in sequence["actionList"]:
        if action["type"] in ["on", "communication"]:
            rawActionList.append(action)

        elif action["type"] == "variant":
            rawActionList.extend(getActionsInVariant(action))

        else:
            fatalError(f"Unknown action tpe {type['type']}")

    sequence["rawActionList"] = rawActionList        


def initializeActions(sequence):
    """
        Initialize actions

        Put them in a continuous list (because variants...)

        Determine the size of each of them.
        Also the variants, we determine the start and end entity they cover :)
    """

    buildRawActionList(sequence)

    determineSizeOfActions(sequence)

    initializeVariants(sequence)
        


def determineHeightOfSequence(sequence):
    """
        The height of the sequence is the height of the header + some margin to first action 
        + the height of all actions.
    """
    
    totalHeight = sequence["headerHeight"] + sequence["marginToFirstAction"] + sequence["marginAfterLastAction"]

    for action in sequence["actionList"]:
        if action["type"] == "on":
            totalHeight += action["height"]

        elif action["type"] == "communication":
            totalHeight += action["height"]

        elif action["type"] == "variant":
            totalHeight += action["size"][1]

        else:
            fatalError(f"unknown action type: {action['type']}")

    sequence["height"] = totalHeight


def createContentList(sequence):
    """
        What does this do??

        It creates the vim interactive thing I think

        TODO: change name of this function to tell wtf it does

    """

    commandList = []

    for i in sequence["entityList"]:
        if "jumpCmd" in i:
            jump = {"cmd":i["jumpCmd"], "startCoord":i["contentStartPos"], "endCoord":i["contentEndPos"]}
            commandList.append(jump)

    for a in sequence["actionList"]:
        if a["type"] == "on":
            pass
        
        elif a["type"] == "communication":
            if "jumpCmd" in a:
                jump = {"cmd":a["jumpCmd"], "startCoord":a["contentStartPos"], "endCoord":a["contentEndPos"]}
                commandList.append(jump)
            

    sequence["cmdList"] = commandList


def generateSequence(config):
    """
        Generate the sequence.

        1. set the initial sequence from the config 
            1.1 Initialize entities
                1.1.1 determine the header height
            1.2 Set some meta data

        2. Determine the size of the actions in the sequence

        3. resize the width of headers if needed due to action-sizes

        4. Determine the total width of the sequence

        5. Give every element its position

        6. Determine the resulting height of the sequence
    """

    sequence = config

    initializeEntities(sequence)


    sequence["headerHeight"] = determineHeightsOfHeader(sequence["itemList"]) 

    if "marginToFirstAction" not in sequence: #Is header-margin a better name?
        sequence["marginToFirstAction"] = 3

    if "marginAfterLastAction" not in sequence:
        sequence["marginAfterLastAction"] = 3

    initializeActions(sequence)

    resizeItemWidth(sequence)

    determineWidthOfSequence(sequence)

    determineRelativePositions(sequence)

    determineHeightOfSequence(sequence)

    createContentList(sequence)


    return sequence
