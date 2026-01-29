"""
    Sequence creation/generation
"""

import sys
import copy

#Below is hack to be able to run tests as -m...
#python is great. The module-system sucks though.
try:
    from . import debug

except ImportError as e:
    try:
        import debug

    except ImportError as e:
        print("IMPORT ERROR: ", e.msg, file=sys.stderr)
        sys.exit(1)


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


def addCoord(thing, x, y, name):
    """
        Add a coordinate to be colored with name.
        So in essence: thing[name] will have x and y added.
    """
    if len(thing[name]) == 0:
        thing[name].append([[x,y], [x+1,y]])

    else:
        previousCoordinate = thing[name][-1]
        if previousCoordinate[1][0] == x:
            #Merge with previous
            previousCoordinate[1][0] = x + 1

        else:
            #Cannot merge, new entry!
            thing[name].append([[x,y], [x+1,y]])


def determineHeightsOfHeader(itemList):
    """
        Aight, then this will determine the heights of the top row.
        I.E entities and such.

        Basically takes the item (entity/container) with largest height,
        and returns that height. 
    """

    itemWithLargestHeight = 0

    for item in itemList:
        h = 0

        if item["type"] == "container":
            h = item["height"]

        elif item["type"] == "entity":
            h = item["height"]

        else:
            debug.fatalError(f"item of type {item['type']} not supported")

        if itemWithLargestHeight <= h:
            itemWithLargestHeight = h
        
    return itemWithLargestHeight 


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

    #The border coordinates are used by vim to color the borders.
    #The syntax is: [[[x0, y0], [x1, y1]], ....]
    #That is, a list of lists, with two coordinates: start coord, and end coord for coloring.
    #This is because we can color many chars on one line, but I don't think we can color columns? or can we?
    #Also, we must add 1 to ending x, since it is exclusive [startX, endX)

    borderCoordinates = [
                            [
                                entity["borderStartPos"], 
                                [entity["borderEndPos"][0] + 1, entity["borderStartPos"][1]]
                            ],
                            [
                                [entity["borderStartPos"][0], entity["borderEndPos"][1]], 
                                [entity["borderEndPos"][0]+1, entity["borderEndPos"][1]]]
                        ]


    x1 = entity["borderStartPos"][0]
    x2 = entity["borderEndPos"][0]

    for y in range(entity["borderStartPos"][1]+1, entity["borderEndPos"][1]):
        borderCoordinates.append([[x1, y], [x1+1, y]])
        borderCoordinates.append([[x2, y], [x2+1, y]])

    entity["borderCoordinateList"] = borderCoordinates


    #Content 

    entity["contentStartPos"] = [-1, -1]

    entity["contentStartPos"][0] = entity["borderStartPos"][0] + entity["border"][3] + entity["padding"][3] 

    entity["contentStartPos"][1] = entity["borderStartPos"][1] + entity["border"][0] + entity["padding"][0]

    entity["contentEndPos"] = [-1, -1]

    entity["contentEndPos"][0] = entity["contentStartPos"][0] + len(entity["name"]) - 1

    #Only allow one line names now
    entity["contentEndPos"][1] = entity["contentStartPos"][1] 


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
            [x, y] = setEntityPos(item, contentPos)
            contentPos[0] += x

        elif item["type"] == "container":
            [x, y] = setContainerPos(item, contentPos)
            contentPos[0] += x

        else:
            debug.fatalError(f"Unknown type: {item['type']}")


    return [container["size"][0], container["size"][1]]


def determineRelativePositionOfItems(sequence, pos):
    """
        Builds the relative positions for each element in header (I.E entities)
    """
    for item in sequence["itemList"]:
        if item["type"] == "entity":
            [width, height] = setEntityPos(item, pos)

            #Move along only x-axis the width of the entity
            pos[0] += width

        elif item["type"] == "container":
            [width, height] = setContainerPos(item, pos)
            pos[0] += width

        else:
            debug.fatalError(f"Unknown type: {item['type']}")


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

    contentRow = row + communication['margin'][0]

    lineRow = contentRow + 1 #content is now only one line long


    if fromCol < toCol:
        communicationMiddle = fromCol + int((toCol - fromCol) / 2)

        communication["arrowPos"] = [toCol - 1, lineRow]
        communication["arrowChar"] = ">"

        communication["lineStartPos"] = [fromCol + 1, lineRow]

        communication["lineEndPos"] = [toCol - 2, lineRow]
        
    else:
        communicationMiddle = toCol + int((fromCol - toCol) / 2)

        communication["arrowPos"] = [toCol + 1, lineRow]
        communication["arrowChar"] = "<"

        communication["lineStartPos"] = [toCol + 2, lineRow]
        communication["lineEndPos"] = [fromCol - 1, lineRow]

    contentLength = len(communication["content"])


    #Aight. in future maybe a proper padding is due... but that is future. not present.
    calculatedPadding = communication["size"][0] - contentLength 

    if calculatedPadding % 2 == 0:
        communication["contentStartPos"] = [communicationMiddle - int((contentLength - 1) / 2), contentRow]
        communication["contentEndPos"]   = [communicationMiddle + int(contentLength / 2), contentRow]

    else:
        communication["contentStartPos"] = [communicationMiddle - int((contentLength) / 2), contentRow]
        communication["contentEndPos"]   = [communicationMiddle + int((contentLength - 1) / 2), contentRow]
        
    
    [e1, e2] = getFromAndToEntities(sequence, fromEntity["id"], toEntity["id"]) 


def determineRelativePositionOfVariantAction(sequence, variant, row):
    """
        Determine the relative position of variant type action.
    """
    action = variant

    fromEntity = getEntityWithId(sequence, action["fromEntityId"])
    toEntity = getEntityWithId(sequence, action["toEntityId"])

    startCol = fromEntity["timeLineCol"] - action["left"]
    endCol   = toEntity["timeLineCol"] + action["right"]
                                                    
    action["startPos"]          = [startCol, row]
    action["endPos"]            = [startCol + action["size"][0], row + action["size"][1] - 1] 
    
    borderStartCol = startCol + action["margin"][3]
    borderEndCol   = endCol - action["margin"][1]

    action["borderStartPos"]    = [borderStartCol, row]

    action["borderEndPos"]      = [borderEndCol, \
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
            branch["branchBorderStart"][0] += action["margin"][3]
            branch["branchBorderEnd"]   = [action["borderEndPos"][0], 
                                           branchPos[1]] 

        branch["startPos"] = branchPos
        contentStartPos    = [branchPos[0] + action["border"][3], \
                              branchPos[1] + action["border"][0]]

        #FIXME: this does not take into account margin n' shit. NOW IT DOES. but NOT TESTED
        branch["contentStartPos"]   = copy.copy(contentStartPos)
        branch["contentStartPos"][0] += action["margin"][3]
        branch["contentEndPos"]     = [contentStartPos[0] + len(branch["name"]) - 1, 
                                       contentStartPos[1]]

        branch["borderStartPos"] = copy.copy(branchPos)
        branch["borderStartPos"][0] += action["margin"][3]

        branch["borderEndPos"]   = [branchPos[0] + len(branch["name"]) + 1, 
                                    branchPos[1] + 2]
        
        for branchAction in branch["actionList"]:
            if branchAction["type"] == "on":      
                determineRelativePositionOfOnAction(sequence, branchAction, branchContentRow)
                branchContentRow += branchAction["height"]

            elif branchAction["type"] == "variant":
                determineRelativePositionOfVariantAction(sequence, branchAction, branchContentRow)
                branchContentRow += branchAction["size"][1]

            else:
                determineRelativePositionOfCommunicationAction(sequence, branchAction, branchContentRow)
                branchContentRow += branchAction["size"][1]


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
            debug.fatalError(f"unknown action type {action['type']}")


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
    debug.debugPrint("determineRelativePositions BEGIN", "FUNCTION")

    pos = [0,0]

    determineRelativePositionOfItems(sequence, pos)
            
    #Now header has been placed, place the timeLines for each entity
    addTimeLines(sequence)

    #Now place the actions. Their x-coordinates are calculated from
    #which entities they touch[sic]
    currentActionRow = sequence["header"]["size"][1] + sequence["marginToFirstAction"] 

    determineRelativePositionOfActions(sequence, currentActionRow)

    debug.debugPrint("determineRelativePositions END", "FUNCTION")


def getCharFromOnAction(action, x, y):
    """
        Get char from an on-action.
        It has: borders, and content. That's it.
    """
    if action["startPos"][1] <= y <= action["endPos"][1] and \
       action["startPos"][0] <= x < action["endPos"][0]:
        if y <= action["contentStartPos"][1] and y >= action["contentEndPos"][1]:
            if x >= action["contentStartPos"][0] and x <= action["contentEndPos"][0]:
                debug.debugPrint(f"{action['contentStartPos']} {action['contentEndPos']}", "CHARGETTING")
                c = action["content"][x - action["contentStartPos"][0]]
                addCoord(action, x, y, "contentCoordinateList")
                return [True, c]      

        #Border:
        r = getBorderChar(action, x, y)

        if r[0]:
            addBorderCoordinate(action, x, y)
            return r 

    #This is a hack to overwrite the | from the middleCol when padding is used
    # IE everything within borders that is not content, is " ". I think this is a reasonable hack (Y)
    if action["borderStartPos"][1] < y < action["borderEndPos"][1] and \
       action["borderStartPos"][0] < x < action["borderEndPos"][0]:
        return [True, " "]

    return [False, False]


def getCharFromCommunicationAction(action, x, y):
    """
        Get char from communication action.
        It has content, and a line with an arrow on it. That's it :)
    """
    if [x, y] == action["arrowPos"]:
        #Put this as same color for now.
        addCoord(action, x, y, "lineCoordinateList")
        return [True, action["arrowChar"]]
    
    if y == action["lineStartPos"][1] and x >= action["lineStartPos"][0] and x <= action["lineEndPos"][0]:
        addCoord(action, x, y, "lineCoordinateList")
        return [True, "-"]

    if y <= action["contentStartPos"][1] and y >= action["contentEndPos"][1]:
        if x >= action["contentStartPos"][0] and x <= action["contentEndPos"][0]:
            debug.debugPrint(f"{action['contentStartPos']} {action['contentEndPos']}", "CHARGETTING")
            c = action["content"][x - action["contentStartPos"][0]]
            addCoord(action, x, y, "contentCoordinateList")
            return [True, c]      

    return [False, False]


def getContentChar(item, x, y):
    if y <= item["contentStartPos"][1] and y >= item["contentEndPos"][1]:
        if x >= item["contentStartPos"][0] and x <= item["contentEndPos"][0]:
            debug.debugPrint(f"{item['contentStartPos']} {item['contentEndPos']}", "CHARGETTING")

            charIndex = x - item["contentStartPos"][0]

            c = item["name"][charIndex]
            addCoord(item, x, y, "contentCoordinateList")
            return [True, c]      

    return [False, False]


def getCharFromVariantAction(action, x, y):
    """
        
    """
    if (action["startPos"][0] <= x <= action["endPos"][0]) and (action["startPos"][1] <= y <= action["endPos"][1]):

        #First check the inner stuff
        for branch in action["branchList"]:
            r = getContentChar(branch, x, y)
            if r[0]:
                return r
            
            r = getBorderChar(branch, x, y)
            if r[0]:
                addCoord(action, x, y, "borderCoordinateList")
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
                        debug.fatalError(f"this should have been caught earlier... type {branchAction['type']} is illegal")

                if "branchBorderStart" in branch:
                    if y == branch["branchBorderStart"][1]:
                        if branch["branchBorderStart"][0] < x < branch["branchBorderEnd"][0]:
                            return [True, "-"] 

                        if x == branch["branchBorderEnd"][0]:
                            return [True, "+"]


        #Then get the borders
        r = getBorderChar(action, x, y)

        if r[0]:
            addCoord(action, x, y, "borderCoordinateList")
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
        debug.fatalError(f"Not handled action {action['type']}")

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
            addBorderCoordinate(item, x, y)
            return r 

        for subItem in item["itemList"]:
            r = getCharFromItem(subItem, x, y)
            if r[0]:
                return r

    else:
        debug.fatalError(f"Unknown type: {item['type']}")

    return [False, False]


def getCharFromHeader(sequence, x, y):
    """
        Get char from header. this is nice.

        Returns [returnCode, char]

        if returnCode is True, a char has been found (on given coordinates),
        else it will be False.

    """

    char = None
    isCharFound = False

    if y < sequence["header"]["size"][1]:

        #timeLine can be in header as well, if there are containers
        #but timeLine takes precedence over container
        for timeLine in sequence["timeLineList"]:   
            if y >= timeLine["rowStart"]: 
                if x == timeLine["column"]:
                    isCharFound = True
                    char = "|"
                    entity = getEntityWithId(sequence, timeLine["entityId"])
                    entity["timeLineCoordinateList"].append([x, y])
                    break
            
        if isCharFound:
            return [True, char]

        for item in sequence["itemList"]:
            if y in range(item["startPos"][1], item["size"][1]):
                [rc, char] = getCharFromItem(item, x, y)
                if rc:
                    debug.debugPrint(f"{char} on {y} {x}", "CHARGETTING")
                    isCharFound = True
                    break
            
        if isCharFound:
            return [True, char]

    return [False, False]


def getSequenceGraph(sequence):
    """
        Get the sequence graph as a string

        Due to poor intellectual capacity,
        this must be run also in order to determine where the middle columns will be,
        and thus save these values in their corresponding entities,
        so we can color them in vim... not very nice, but it is what it is

        And also to be able to color the containers properly, since they overlap with timeLines...
    """

    graphStringListList = []
    
    for y in range(sequence["height"]):
        graphStringList = []

        for x in range(sequence["width"]):

            #Get char from header

            [rc, c] = getCharFromHeader(sequence, x, y)

            if rc:
                graphStringList.append(c)
                continue

            #Check for action

            isCharFound = False

            for action in sequence["actionList"]:
                [rc, c] = getCharFromAction(action, x, y)
                if rc:
                    graphStringList.append(c) 
                    isCharFound = True
                    break
                pass

            if isCharFound:
                continue

            #TimeLines
            for timeLine in sequence["timeLineList"]:   
                if y >= timeLine["rowStart"]: 
                    if x == timeLine["column"]:
                        #Must match this timeLine to a entity,
                        #and add the coords in the entities timeLineCoordinateList
                        isCharFound = True
                        graphStringList.append("|") 
                        entity = getEntityWithId(sequence, timeLine["entityId"])
                        entity["timeLineCoordinateList"].append([x, y])
                        
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


def addBorderCoordinate(thing, x, y):
    """
        Add x and y to borderCoordinateList in an appropriate way, Y R u geh.
    """
    addCoord(thing, x, y, "borderCoordinateList")


def addTimeLines(sequence):
    """
        Add the timeLines for each entity.

        That is, decide which col it should be at, 
        and where it should start in y-length.
    """

    timeLineList = []

    for entity in sequence["entityList"]:
        if entity["type"] == "entity":
            #Middle of the entity in terms of border, I.E size without margin
            middleOfEntity = entity["borderStartPos"][0] + int((entity["borderEndPos"][0] - entity["borderStartPos"][0]) / 2) 
            oneBelowEntity = entity["borderEndPos"][1] + 1

            timeLineList.append({"column":middleOfEntity, "rowStart":oneBelowEntity, "entityId":entity["id"]})

            entity["timeLineCol"] = middleOfEntity
            
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


def sizeEntity(entity):
    entity["size"] = [0, 0] 

    entity["size"][0] = getEntityWidth(entity)

    entity["size"][1] = getInitialEntityHeight(entity) 
            
    entity["width"]  = entity["size"][0]
    entity["height"] = entity["size"][1]

    entity["widthNoMargin"] = entity["width"] - entity["margin"][1] - entity["margin"][3]


def resizeEntity(entity):
    """
        This is the same as determineSizeOfEntity
        but with a different debugPrint
    """
    oldSize = copy.copy(entity["size"])
    sizeEntity(entity)


    if oldSize[0] != entity["size"][0] or oldSize[1] != entity["size"][1]:

        debug.debugPrint(f"entity {entity['name']} size change: {oldSize} -> {entity['size']}", "RESIZING")


def determineSizeOfEntity(entity):
    """
        Determines both the height and width of an entity.
        This is done by adding up content, padding, border, and margin
    """
    sizeEntity(entity)
    debug.debugPrint(f"entity {entity['name']} size: {entity['size']}", "SIZING")


def determineSizeOfCommunicationAction(action):
    """
        Get the (minimum) size of a "communication" action

        return the (minimum) size as:
        [width, height]
    """

    action["width"] = len(action["content"]) +\
                        action['padding'][1] + action['padding'][3] +\
                        action['margin'][1] + action['margin'][3] 

    action["height"] = 2 + \
                        action["margin"][2] + action["margin"][0] +\
                        action["padding"][0] + action["padding"][2] #Padding in height is a bit tricky on the communication...

    action["size"] = [action["width"], action["height"]]

    debug.debugPrint(f"communication-action: {action['content']} determined size: {action['size']}", 
                     "SIZING")

    return action["size"] 


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

    height = contentHeight + action["border"][0]  + action["border"][2] + \
                             action["padding"][0] + action["padding"][2] + \
                             action["margin"][0]  + action["margin"][2]

    action["size"] = [width, height]

    action["width"] = width

    action["height"] = height

    debug.debugPrint(f"on-action: {action['content']} determined size: {action['size']}", 
                     "SIZING")

    return [width, height]


def determineSizeOfActions(sequence):
    """
        Determine both the height and width of 'primitive' actions (Not variants).

        The width can later be used to resize the width of entities.
        This can be a little bit tricky, but is doable.
        
    """
    for action in sequence["rawActionList"]:

        if action["type"] == "on":
            determineSizeOfOnAction(action)

        elif action["type"] == "communication":
            determineSizeOfCommunicationAction(action)
            
        else:
            debug.fatalError(f"ERROR only 'on', and 'communication' supported now. "\
                             f"Type: {action['type']} is not supported") 


def determineSizeOfVariantAction(action):
    """
        Get the size of a variant

        TODO: this will involve going through the branchList
        calculating the sizes of the induvidual items 
        and take sums and max of certain values
    
        This is not called anywhere? TODO: REMOVE
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
                debug.fatalError(f"Unknown action type: {action['type']}")

            actionWidth += width


def getEntityWithId(sequence, id):
    for i in sequence["entityList"]:
        if i["type"] == "entity":
            if i["id"] == id:
                return i

        else:
            debug.fatalError("still only entities allowed")
    
    debug.fatalError(f"entity with id {id} does not exist")


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
        debug.fatalError("must have at least 2 entities between each other")

    if entityList[0] == entityList[1]:
        debug.fatalError("Both entities cannot be the same though...")

    familyTreeListList = [getFamiliyTreeList(entityList[0]), getFamiliyTreeList(entityList[1])]


    startItem = entityList[0]

    endItem = entityList[1]

    if familyTreeListList[0] != familyTreeListList[1]:
        commonAncestor = getCommonAncestor(familyTreeListList[0], familyTreeListList[1])

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


def getCommonAncestor(familyTreeAList, familyTreeBList):
    """
        Given two family trees,
        return the first common parent to both families
    """

    for ancestor in familyTreeAList:
        if ancestor in familyTreeBList:
            return ancestor

    debug.fatalError("two entites without common ancestor... how defuq is that possible :(")


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
            debug.fatalError("must be a container, or something is terribly broken :(")


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
            debug.fatalError("must be a container, or something is terribly broken :(")


        #Add the left side of this container
        toAdd = nextItem["padding"][3] + nextItem["border"][3] + nextItem["margin"][3]

        return toAdd + getLeftTraversalDistance(nextItem, stopItem)
    

def getFamiliyTreeList(item):
    """
        Get a list of parent, grand parent, great grandparent, and so on ...    

        The last element in the list will always be None, 
        since that is the top element (root)
    """

    p = item["parent"]

    familyTreeList = [item]

    while p != None:
        familyTreeList.append(p)

        p = p["parent"]

    familyTreeList.append(p)


    return familyTreeList
        

def getEntityCC(sequence, firstEntity, secondEntity):
    """
        Get the Center-Center distance between two entities...
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

        Unit Test: test_getEntityCC
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
        debug.fatalError(f"Could not find entites for ID from: {fromEntityId} and to: {toEntityId}")

    if entityList[0]["id"] == entityList[1]["id"]:
        debug.fatalError(f"two entities share the same ID: {entityList[0]['id']}")

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


def addCC(sequence, fromEntity, toEntity, distanceToAdd):
    """
        Add distance (centrum-centrum) between two entities.

        Then fromEntity must be before toEntity in the entityList.

        distanceToAdd is the total number of chars to add between them,
        and will be distributed between every inbetween entity.

        TODO: explain how this is done, and why...
        even more 
        TODO: add unit test for this to see how it behaves and fix any inconsistencies.
        because there are probably bugs here. I know because the person who did it is an idiot.
        (hint: it was I <- look! correct grammar!)
    """

    #Aigh then. We gonna need all involved mfs here.
    #Also a good chance I'm off by one (or two here)
    itemList = getItemsBetween(sequence, 
                               fromEntity["id"], 
                               toEntity["id"])

    if distanceToAdd % 2 == 1:
        #Ok. Need one more if uneven to get 1 margin in both directions on signal-content
        distanceToAdd += 1

    #Ok. We can be really clever here, and sort of get the proportional increase per item,
    #or we can go with the easy route and just distribute them evenly.
    #easy route, I choose you

    #CHECKME: what if distanceToAdd is really small, and there are a lot of items in the list?
    #does it still work, and who gets the addage? I think this is wrong as of now :(
    #TODO: fix the above issue that most likely exists...

    distanceToAddEachItem = int(distanceToAdd / len(itemList))

    isFirstEntity = True

    for item in itemList[:-1]:
        if isFirstEntity:
            debug.debugPrint(f"Adding {distanceToAddEachItem} to {item['name']}", "RESIZING")
            item["margin"][1] += distanceToAddEachItem + distanceToAddEachItem % 2

        else:
            #Distribute evently beteween left and right margin. 
            #if uneven. right will get the extra.
            item["margin"][1] += int(distanceToAddEachItem / 2) + distanceToAddEachItem % 2
            item["margin"][3] += int(distanceToAddEachItem / 2)

        
        if item["type"] == "entity":
            resizeEntity(item)

        else:
            resizeContainer(item)

        isFirstEntity = False

    debug.debugPrint(f"Adding {distanceToAddEachItem + distanceToAddEachItem % 2} to {itemList[-1]['name']}", "RESIZING")

    itemList[-1]["margin"][3] += distanceToAddEachItem + distanceToAddEachItem % 2

    if itemList[-1]["type"] == "entity":
        resizeEntity(itemList[-1])

    else:
        resizeContainer(itemList[-1])
    
    #This is a travesty... should really nicen'[tm] things up...
    #I mean, in the CC-calc the family trees are already there. Should mayhaps add familyTrees to
    #the elements themselfs at the start, since it is a static feature.
    familyTreeListList = [getFamiliyTreeList(fromEntity), getFamiliyTreeList(toEntity)]

    commonAncestor = getCommonAncestor(familyTreeListList[0], familyTreeListList[1])

    #This is a bit of a hack I feel like :(
    #But it works, so don't touch :|
    if commonAncestor != None:
        resizeContainer(commonAncestor)
        p = commonAncestor["parent"]
        while p:
            resizeContainer(p)
            p = p["parent"]


def commSorter(i):
    """
        If only I knew how to make lambdas...
        oh, well
    """
    return i["numSpanned"]


def sortCommunicationsByNumberOfSpannedEntities(sequence):
    """
        This will sort communications by the number of entities they span,
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
    anyChanges = False

    entity = getEntityWithId(sequence, variant["toEntityId"])

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
        debug.debugPrint(f"{variant['branchList'][0]['name']} contentWidth is bigg {contentWidth}", "RESIZE")
        variant["right"] += int((toAdd + 1) / 2)
        variant["left"]  += int(toAdd / 2)
        debug.debugPrint(f"{variant['left']} {variant['right']}", "RESIZE")
        anyChanges = True
        
    entitySizeNoCol = entity["size"][0] - 1 #Remove the middle col from the equation


    #now check if we need to add anything to the entity because of sides

    [entityLeft, entityRight] = getEntitySides(entity)

    rightEntitySide = entityRight 
    leftEntitySide  = entityLeft 

    fullLeftSide = variant["left"] + variant["border"][3] + variant["padding"][3] + variant["margin"][3] - 1

    if fullLeftSide > leftEntitySide: 
        #Increase margin to make room for the variant
        entity["margin"][3] += (fullLeftSide - leftEntitySide)
        anyChanges = True
        
    fullRightSide = variant["right"] + variant["border"][1] + variant["padding"][1] + variant["margin"][1] - 1
    
    if fullRightSide > rightEntitySide:
        #Increase margin to make room for the variant
        entity["margin"][1] += (fullRightSide - rightEntitySide) 
        anyChanges = True

    #Change the entity size
    resizeEntity(entity)

    if entity["parent"] != None:
        familyTreeList = getFamiliyTreeList(entity)
        resizeContainer(familyTreeList[-2])

    variant["size"][0] = variantWidth + variantElementWidth 

    debug.debugPrint(f"variantSize: {variant['size']}", "RESIZE")

    return anyChanges 


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
        I think we are trying to figure out if we need to increase
        left margin on fromEntity and right margin on toEntity,
        for the given variant.

        It is not that complicated.

      fromEntity     toEntity
          |             |
          v             v
        +---+  +---+  +---+   <--+
        | A |  | B |  | C |      | items 
        +---+  +---+  +---+   <--+
          |      |      |
       +---+---------------+  <--+
       | V |               |     |
       +---+               |     +-- Variant
       |                   |     |
       +-------------------+  <--+
       <->|      |      |<->
        L |      |      | R


        If L is larger than As' left,
        we must increase As' left accordingly.

        If R is larger than Cs' right,
        we must increase Cs' right accordingly.

        That is what we do here:
        check if L and R sticks out of A and C respectively,
        and if so, corrects it (increasing A and/or C).

        Note that A, and C can be within one or many containers,
        and that B represents one or more entities/containers between A and C.
    """

    #Check if we need to add anything to the entity because of 
    #sides

    debug.debugPrint("resizeByVariantManyEntitites BEGIN", "FUNCTION")

    anyChanges = False

    fromEntity = getEntityWithId(sequence, variant["fromEntityId"])
    toEntity = getEntityWithId(sequence, variant["toEntityId"])


    [entityLeft, _] = getEntitySides(fromEntity)
    [_, entityRight] = getEntitySides(toEntity)

    fullVariantLeft  = getVariantLeft(variant) 
    fullVariantRight = getVariantRight(variant) 

    debug.debugPrint(f"resize variant over many: "\
                     f"from-to {fromEntity['name']} - {toEntity['name']} "\
                     f"entityLeft {entityLeft} entityRight: {entityRight} "\
                     f"fullVariantLeft: {fullVariantLeft} fullVariantRight: {fullVariantRight}", 
                     "VARIANT")

    if fullVariantLeft > entityLeft:
        #Increase margin to make room for the variant

        toAdd = fullVariantLeft - entityLeft
        fromEntity["margin"][3] += toAdd 

        if fromEntity["parent"] != None:
            familyTreeList = getFamiliyTreeList(fromEntity)
            resizeContainer(familyTreeList[-2])

        else:
            resizeEntity(fromEntity)

        #Get the new entityLeft
        [entityLeft, _] = getEntitySides(fromEntity)

        anyChanges = True

        debug.debugPrint(f"add {toAdd} margin on left entity. entityLeft: {entityLeft}", 
                         "VARIANT")
    

    if fullVariantRight > entityRight:
        #Increase margin to make room for the variant
        toAdd = fullVariantRight - entityRight
        toEntity["margin"][1] += toAdd 

        if toEntity["parent"] != None:
            familyTreeList = getFamiliyTreeList(toEntity)
            resizeContainer(familyTreeList[-2])
        else:
            resizeEntity(toEntity)

        #Get the new entityRight
        [_, entityRight] = getEntitySides(toEntity)

        anyChanges = True

        debug.debugPrint(f"add {toAdd} margin on right entity. entityRight: {entityRight}", 
                         "VARIANT")


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

    debug.debugPrint(f"widths: cc: {cc} totalWidthToFitInto: {totalWidthToFitInto} contentWidth: {contentWidth} "\
                     f"variantStyleWidth: {variantStyleWidth} totalVariantWidth: {totalVariantWidth}", 
                         "VARIANT")

    if totalVariantWidth > totalWidthToFitInto:
        #ok increase CC:
        distanceToAdd = totalVariantWidth - totalWidthToFitInto 
        debug.debugPrint(f"increase CC by distanceToAdd: {distanceToAdd}",
                         "VARIANT")
        addCC(sequence, fromEntity, toEntity, distanceToAdd)

        anyChanges = True

    cc = getEntityCC(sequence, 
                     fromEntity, 
                     toEntity)    

    debug.debugPrint(f"{variant['left']} {cc} {variant['right']}", "VARIANT")
    #Ok, this looks extremly retarded. but that's only because it mirrors the author thought-pattern.
    #add 1 for fromEntity middleCol, 1 for toEntity middleCol, but then remove 1 for each side (left, right)...
    variant["size"][0] = variant["left"] + cc + variant["right"] + 1 + 1 + variantStyleWidth - 1 - 1 

    
    debug.debugPrint(f"final variant width: {variant['size'][0]}",
                     "VARIANT")

    debug.debugPrint("resizeByVariantManyEntitites END", "FUNCTION")

    return anyChanges 

    
def resizeByVariant(sequence, variant):
    """
        Resize entities by variants.

        We have already set the height of the variants (see initializeVariant),
        the sides of every variant (recursively),
        and we have already taken into account CC-increasage due to "atomic actions"...

        Thus, all that is left is to check if variants fits on, or between entities,
        given the content length of the variant (the largest branch name),
        and the sides (left, right), since we can end up starting variant quite 
        far away from middle column if we have big "on"-actions,
        or many recursive variants within one another.

        If left or right ends up being to far out (outside of entities width),
        we will increase that entities margin to accomodate the variant.
        Now, that is arbitrary, but probably the simplest solution.


        There are 2 distinct cases:
            1. The variant is over one single entity
            2. The variant is over more than one entity

        They are handled separetly for convenience :)

        Hope this works. Hope leaves us last

    """
    debug.debugPrint("resizeByVariant BEGIN", "FUNCTION")
    
    anyChanges = False

    #Every action resized their respective stuff already.
    for branch in variant["branchList"]:
        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":
                
                anyChanges = anyChanges or resizeByVariant(sequence, branchAction)

    if variant["fromEntityId"] == variant["toEntityId"]:
        anyChanges = anyChanges or resizeByVariantSingleEntity(sequence, variant)

    else:
        anyChanges = anyChanges or resizeByVariantManyEntitites(sequence, variant)

    debug.debugPrint("resizeByVariant END", "FUNCTION")

    return anyChanges


def sizeContainer(container):
    """
        Set the size of the container.
        This is done by first setting the size of all underlying things,
        using the result of this we get the size of the container.

        I.E if the container contains 3 entities with widhts [3, 5, 4]
        this container will be the sum of these in width (plus padding, border, margin),
        in this example 12.     
    """

    sizeItemList(container["itemList"])

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

    debug.debugPrint(f"sizeContainer: container: {container['name']} size: {container['size']}", "SIZING")


def sizeItemList(itemList):
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
            sizeEntity(item)

        elif item["type"] == "container":
            sizeContainer(item)


def resizeContainer(container):
    """
        This is the same as sizeContainer,
        but it has a different debugPrint for easier debbuging.
    """
    sizeBefore = copy.copy(container["size"])

    resizeItemList(container["itemList"])

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

    if sizeBefore[0] != container["size"][0] or sizeBefore[1] != container["size"][1]:
        debug.debugPrint(f"container: {container['name']} size change: {sizeBefore} -> {container['size']}", "RESIZING")


def resizeItemList(itemList):
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
            resizeEntity(item)

        elif item["type"] == "container":
            resizeContainer(item)


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


def resizeItemsByOnActions(sequence):
    """
        Resize items (entities and containers)
        by the corresponding on-actions that exist.

        If an on-action is larger than the entity upon which it sits,
        must increase that entitys' width.
        
        AND if the entity is within a container (within a container within a container....)
        we must also resize that (those, recursively).
    """
    #First. go with the on-actions
    #These will resize their respective entity
    for action in sequence["rawActionList"]:
        if action["type"] == "on":
            entity = getEntityWithId(sequence, action["entityId"])

            if action["width"] > entity["width"]:
                toAddRightMargin = entity["margin"][1] + int((action["width"] - entity["widthNoMargin"]) / 2)
                #Ok. I'm a bit unsure if I should add here or above, but I'll try here :)
                toAddLeftMargin = entity["margin"][3] + int((action["width"] - entity["widthNoMargin"] + 1) / 2)

                entity["margin"][1] = toAddRightMargin
                entity["margin"][3] = toAddLeftMargin 

                debug.debugPrint(f"entity: {entity['name']} is resized due to on-action: {action['content']} " \
                           f"previous size: {entity['size']} " \
                           f"adding: {toAddRightMargin} <- -> {toAddLeftMargin}", 
                           "RESIZING")

                resizeEntity(entity)

                if entity["parent"] != None:
                    familyTreeList = getFamiliyTreeList(entity)
                    resizeContainer(familyTreeList[-2])


def resizeItemsByCommunicationActions(sequence):
    """
        Resize by communications.

        A communication spans 2 or more entities,
        and if it is larger than the space between them,
        we must increase their size.

        TODO: give example
    """
    communicationList = sortCommunicationsByNumberOfSpannedEntities(sequence)

    for action in communicationList:
        if action["type"] == "communication":

            [firstEntity, secondEntity] = getFromAndToEntities(sequence, 
                                                               action["fromEntityId"], 
                                                               action["toEntityId"])

            cc = getEntityCC(sequence, firstEntity, secondEntity)  

            if action["width"] > cc:
                
                distanceToAdd = action["width"] - cc 

                addCC(sequence, firstEntity, secondEntity, distanceToAdd)


def resizeByVariants(sequence):
    """
        Resize entities (and indirectly container) by checking variants.

        This might mean adding to either left, right or both of
        certain entities.

        We must resize until no changes (no new distances between entities, or new entity widths) 
        have been made, since changes in later variant can influence changes
        in previous variants. Thus we try until no new changes have been made.
    """
    debug.debugPrint("resizeByVariants BEGIN", "FUNCTION")

    anyChanges = True

    while anyChanges:
        anyChanges = False

        for action in sequence["actionList"]:
            if action["type"] == "variant":
                anyChanges = anyChanges or resizeByVariant(sequence, action)

    debug.debugPrint("resizeByVariants END", "FUNCTION")


def resizeCommunications(sequence):
    """
        Resize all communications after items in header are resized 
        due to variants and other things.

        The header is always the one making the calls,
        so the distance between entities will decide the width of the communications.

        In other words, if CC has changed due to variant (or other),
        this will be handled here.
    """
    for action in sequence["rawActionList"]:
        if action["type"] == "communication":
            
            [firstEntity, secondEntity] = getFromAndToEntities(sequence, 
                                                               action["fromEntityId"], 
                                                               action["toEntityId"])

            cc = getEntityCC(sequence, firstEntity, secondEntity)    

            if action["size"][0] != cc:
                
                debug.debugPrint(f"communication-action {action['content']} width changed: {action['size'][0]} -> {cc}", 
                            "RESIZING")
    
            action["width"] = cc 
            action["size"][0] = cc


def resizeItemWidth(sequence):
    """
        Go through all actions and see if any entities needs to be resized.

        And if they do need to be resized, resize them :)
        Light weight.
    """
    debug.debugPrint("resizeItemWidth BEGIN", "FUNCTION")

    debug.debugPrint("RESIZING BEGIN", "RESIZING")

    resizeItemsByOnActions(sequence)

    resizeItemsByCommunicationActions(sequence)

    resizeByVariants(sequence)

    resizeCommunications(sequence)

    debug.debugPrint("RESIZING END", "RESIZING")
    debug.debugPrint("resizeItemWidth END", "FUNCTION")


def determineSizeOfContainer(container):
    """
        Determine the size of a container,

        Should this be used to resize later? maybe :)
    """
    sizeContainer(container)


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
        No its not retarded. You can be the retarded. This is beautiful.
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
    debug.debugPrint("initializeEntities BEGIN", "FUNCTION")

    determineSizeOfItemList(sequence["itemList"])

    initializeItemPositions(sequence["itemList"])

    initializeHierarchy(sequence["itemList"])

    initializeEntityList(sequence)

    debug.debugPrint("initializeEntities END", "FUNCTION")


def getFirstEntityInSet(sequence, s):
    """
        Given s is a set of entityIds,
        gives the id from that set that is first found in entityList
    """
    for i in sequence["entityList"]:
        if i["id"] in s:
            return i["id"]

    debug.fatalError(f"Could not get any entity with id in set: {s}")


def getLastEntityInSet(sequence, s):
    """
        Given s is a set of entityIds,
        gives the id from that set that is last found in entityList
    """
    for i in sequence["entityList"][::-1]:
        if i["id"] in s:
            return i["id"]

    debug.fatalError(f"Could not get any entity with id in set: {s}")


def setStartAndEndEntityForVariant(sequence, variant):
    """
        Ok. Get the first and last entity (in the order of header)
        that this variant covers. Does it recursively throughout every branch,
        so all subvariants (variant actions in branches) will also be set.

        After this, variants here will have attributes:

            fromEntityId
            toEntityId

        set, and ready to go!
    """

    debug.debugPrint("setStartAndEndEntityForVariant START", "FUNCTION")

    variant["size"] = [0, 0]

    entityIdSet = set() 
        
    for branch in variant["branchList"]:

        debug.debugPrint(f"BRANCH {branch['name']}", "VARIANT")
        branch["size"] = [0, 0]

        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":
                setStartAndEndEntityForVariant(sequence, branchAction)
    
                entityIdSet.add(branchAction["fromEntityId"])
                entityIdSet.add(branchAction["toEntityId"])

            elif branchAction["type"] == "on":
                entityIdSet.add(branchAction["entityId"])

            elif branchAction["type"] == "communication":
                entityIdSet.add(branchAction["fromEntityId"])
                entityIdSet.add(branchAction["toEntityId"])

            else:
                debug.fatalError(f"type {branchAction['type']}")
    
    variant["fromEntityId"] = getFirstEntityInSet(sequence, entityIdSet)
    variant["toEntityId"]   = getLastEntityInSet(sequence, entityIdSet)

    fromEntity = getEntityWithId(sequence, variant["fromEntityId"])    
    toEntity = getEntityWithId(sequence, variant["toEntityId"])    

    debug.debugPrint(f"from-to {variant['fromEntityId']} - {variant['toEntityId']}"\
                     f" name {fromEntity['name']} - {toEntity['name']}", "VARIANT")

    debug.debugPrint("setStartAndEndEntityForVariant END", "FUNCTION")


def getOnActionSides(onAction):
    """
        Return how much this entity sticks out each side from middle column.
        
        This is including margin, border, padding.
        Example (no left/right-margin):

                 |                  |
                 |                  |
              +----+             +-----+
              |    |             |     |
              +----+             +-----+
                 |                  |

      returns [3, 2]             [3, 3]


        This then means that we are left-aligned(?!). Is this consistent?
    """

    sizeToSplit = onAction["size"][0] - 1 #Remove the middleCol from the equation

    left    = int((sizeToSplit) / 2)
    right   = int((sizeToSplit) / 2)

    if onAction["size"][0] % 2 == 0:
        left += 1

    return [left, right]


def setVariantSides(sequence, variant):
    """
        Set variant left and right addage.
        I.E how far away of middle column of entity this variant have to start.

        so we have an entity, and a variant around it.
        left (L) and right (R) will be as follows:

             +---+
             | E |
             +---+
               |
               | 
         +---+------+ <-+
         | V | |    |   |
         +---+ |    |   +- Variant
         |     |    |   |
         +----------+ <-+
         ^    ^|^   ^
         |    |||   |
         +----+|+---+
           L   |  R

        And if the variant covers multiple entities, the same concept applies,
        but L will be to the left of the left most entity (fromEntityId),
        and R to the right of the right most entity (toEntityId).

        Also the height of the variant will be settled after this it seems...

        Protip: I don't know what I'm doing
    """

    debug.debugPrint(f"setVariantSides START", "FUNCTION")

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

                [vLeft, vRight, leftEntityId, rightEntityId] = setVariantSides(sequence, branchAction)

                if leftEntityId == variant["fromEntityId"]:
                    if vLeft > left:
                        left = vLeft

                if rightEntityId == variant["toEntityId"]:
                    if vRight > right:
                        right = vRight

                branchHeight += branchAction["size"][1]

                #If we are on single entity, need to expand our left and right when we go hard or go home
                #with the name of branches b long
                if variant["fromEntityId"] == variant["toEntityId"]:
                    for subBranch in branchAction["branchList"]:
                        subBranchContentWidth = len(subBranch["name"])
                        if (left + 1 + right - 2) < subBranchContentWidth:
                            toAdd = subBranchContentWidth - (left + 1 + right - 2)

                            left  += int(toAdd / 2)
                            right += int((toAdd + 1) / 2)


            elif branchAction["type"] == "on":
                branchHeight += branchAction["size"][1]

                [onLeft, onRight] = getOnActionSides(branchAction)

                if variant["fromEntityId"] == variant["toEntityId"]:
                    if branchAction["entityId"] == variant["fromEntityId"]:

                        if onLeft > left:
                            left = onLeft

                        if onRight > right:
                            right = onRight

                elif branchAction["entityId"] == variant["fromEntityId"]:
                    if onLeft > left:
                        left = onLeft

                elif branchAction["entityId"] == variant["toEntityId"]:
                    if onRight > right:
                        right = onRight

                else:
                    #This on is in middle somwhere, no action needed :)
                    pass
                    

            elif branchAction["type"] == "communication":
                #A communication take no room on sides (AT LEAST NOT YET!)
                branchHeight += branchAction["size"][1]

            else:
                debug.fatalError(f"ERROR: type {branchAction['type']}")

            branch["size"][1] = branchHeight

        height += branchHeight

    variant["size"][1] = height

            
    #So in essence, left is where this should start left side, 
    #and right where it shall start right side.
    #and by start I mean where the inner element ends + 1
    #and also to clarify, its left of middleCol of fromEntity, and right from middleCol toEntity...
    variant["left"]    = left  + variant["border"][3] + variant["margin"][3] + variant["padding"][3]
    variant["right"]   = right + variant["border"][1] + variant["margin"][1] + variant["padding"][1] 

    #print(f"left: {variant['left']} | | | {variant['right']} ")
    #print(f"{variant['margin']} {variant['border']} {variant['padding']}")

    debug.debugPrint(f"setVariantSides size: {variant['size']} "\
                     f"left: {left} right: {right} "\
                     f"totalLeft: {variant['left']} totalRight: {variant['right']}", "VARIANT")

    debug.debugPrint(f"setVariantSides END", "FUNCTION")

    return [variant["left"], variant["right"], variant["fromEntityId"], variant["toEntityId"]]


def setVariantStyle(variant):
    """
        Initialize the stype for every branch in variant.
        I.E border, margin, and padding.
    """

    setStyle(variant)

    for branch in variant["branchList"]:
        for branchAction in branch["actionList"]:
            if branchAction["type"] == "variant":
                setVariantStyle(branchAction)


def initializeVariant(sequence, variant):
    """
        Initialize a particular variant.

        This includes: 
            Setting default style: border, padding, margin

            Setting fromEntityId and toEntityId 
            (I.E start/leftmost entity, and end/rightmost entity this variant covers)
    
            The left and right addage needed on each side of the variant.
            I.E how far it should be from the fromEntityId and toEntityId's middleCol.

            It also calculates the height of the variant, since that will not change later
    """
    debug.debugPrint("initializeVariant START", "FUNCTION") 

    setVariantStyle(variant)

    setStartAndEndEntityForVariant(sequence, variant)

    setVariantSides(sequence, variant)

    debug.debugPrint("initializeVariant END", "FUNCTION") 


def initializeVariants(sequence):
    """
        Initialize every variant

        Will figure out which entity is the first and last
        of each variant.

        I think this is the only way of doing things.
        And then in the end we can adjust entity width depending on the
        variant configuration
    """
    debug.debugPrint("initializeVariants START", "FUNCTION")
    for a in sequence["actionList"]:
        if a["type"] == "variant":
            initializeVariant(sequence, a)

    debug.debugPrint("initializeVariants END", "FUNCTION")


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
                debug.fatalError(f"Not valid type: {branchAction['type']}. "
                           f"Valid types are: 'variant', 'on', 'communication'")

    return aList


def buildRawActionList(sequence):
    """
        the naming is not perfect... But rawActionList are all non-container-type actions...
        easy right :D 
        I.E all actions not of type variant right now

        So this function builds the list => sequence['rawActionList']
        with all 'atomic' actions in order of appearance.
    
        This will allow us to determine the size of these actions later,
        before we do the 'container'-type actions,
        since the 'container'-type actions sizes depend on the size
        of these... I don't know if this is smart, but it works.
    """
    rawActionList = []

    for action in sequence["actionList"]:
        if action["type"] in ["on", "communication"]:
            rawActionList.append(action)

        elif action["type"] == "variant":
            rawActionList.extend(getActionsInVariant(action))

        else:
            debug.fatalError(f"Unknown action tpe {type['type']}")

    sequence["rawActionList"] = rawActionList        


def initializeActions(sequence):
    """
        Initialize actions

        Put them in a continuous list (because variants...)

        Determine the size of each of them.
        Also the variants, we determine the start and end entity they cover :)
    """
    debug.debugPrint("initializeActions BEGIN", "FUNCTION")

    buildRawActionList(sequence)

    for action in sequence["rawActionList"]:
        setStyle(action) 

    determineSizeOfActions(sequence)

    initializeVariants(sequence)

    debug.debugPrint("initializeActions END", "FUNCTION")


def determineHeightOfSequence(sequence):
    """
        The height of the sequence is the height of the header + some margin to first action 
        + the height of all actions.
    """
    
    totalHeight = sequence["header"]["size"][1] + sequence["marginToFirstAction"] + sequence["marginAfterLastAction"]

    for action in sequence["actionList"]:
        if action["type"] == "on":
            totalHeight += action["height"]

        elif action["type"] == "communication":
            totalHeight += action["height"]

        elif action["type"] == "variant":
            totalHeight += action["size"][1]

        else:
            debug.fatalError(f"unknown action type: {action['type']}")

    sequence["height"] = totalHeight
    

def initializeContainerVim(container):
    """
        Aight, so need to initialize container here,
        but to fill in we need to generate the graph....
        A sadness I cannot overcome easily
    """
    container["borderCoordinateList"] = [] #This 2 must be filled when displaying graph because of timeLine overlapping...
    container["contentCoordinateList"] = [] #Where content exists are placed

    for subItem in container["itemList"]:
        if subItem["type"] == "container":
            initializeContainerVim(subItem)
    

def initializeActionVim(action):
    if "vim" not in action:
        action["vim"] = {}

    action["contentCoordinateList"] = [] #Where content exists are placed

    if action["type"] == "variant":
        action["borderCoordinateList"] = []
        for branch in action["branchList"]:
            branch["borderCoordinateList"] = []
            branch["contentCoordinateList"] = [] #Where content exists are placed
            for branchAction in branch["actionList"]:
                initializeActionVim(branchAction)

    elif action["type"] == "on":
        action["borderCoordinateList"] = []

    elif action["type"] == "communication":
        #Aight, this is bit unique (stupid).
        action["lineCoordinateList"] = []
        

def initializeVim(sequence):
    """
        Initialize the vim-attribute for every entity (should be for every type of thing later...) 
        Also, should be made sort of optional?
    """
    debug.debugPrint("initializeVim BEGIN", "FUNCTION")

    for entity in sequence["entityList"]:
        if "vim" not in entity:
            entity["vim"] = {}
        entity["borderCoordinateList"]      = [] #Where borders are placed
        entity["contentCoordinateList"]     = [] #Where content exists are placed
        entity["timeLineCoordinateList"]    = [] #Where time line exists

    for item in sequence["itemList"]:
        if item["type"] == "container":
            initializeContainerVim(item)

    for action in sequence["actionList"]:
        initializeActionVim(action) 

    debug.debugPrint("initializeVim END", "FUNCTION")


def removeCircularDependenciesContainer(container):
    """
        Remove all references to other elements of this container,
        recursively
    """
    container["nextSibling"]            = None
    container["previousSibling"]        = None
    container["nextEntitySibling"]      = None
    container["previousEntitySibling"]  = None
    container["parent"]                 = None

    for item in container["itemList"]:
        if item["type"] == "entity":
            item["nextSibling"]             = None
            item["previousSibling"]         = None
            item["nextEntitySibling"]       = None
            item["previousEntitySibling"]   = None
            item["parent"]                  = None
            
        elif item["type"] == "container":
            removeCircularDependenciesContainer(item)
    

def removeCircularDependencies(sequence):
    """
        This is needed to be able to json-encode the sequence in the end.
    """
    for item in sequence["itemList"]:
        if item["type"] == "entity":
            item["nextSibling"]             = None
            item["previousSibling"]         = None
            item["nextEntitySibling"]       = None
            item["previousEntitySibling"]   = None
            item["parent"]                  = None

        elif item["type"] == "container":
            removeCircularDependenciesContainer(item)


def applyFunctionOnItem(sequence, item, function):
    """
        Apply function on item. If item is container, 
        apply function recursively on children.
    """

    #Call the function
    function(sequence, item)

    if item["type"] == "container":
        for subItem in item["itemList"]:
            applyFunctionOnItem(sequence, subItem, function)


def applyFunctionOnAllItems(sequence, function):
    for item in sequence["itemList"]:
        applyFunctionOnItem(sequence, item, function)


def applyFunctionOnAction(sequence, action, function):
    """
        Apply function on action recursevly if it is a variant.
    """
    function(sequence, action)

    if action["type"] == "variant":
        for branch in action["branchList"]:
            for subAction in branch["actionList"]:
                applyFunctionOnAction(sequence, subAction, function)


def applyFunctionOnAllActions(sequence, function):
    for action in sequence["actionList"]:
        applyFunctionOnAction(sequence, action, function)
    

def applyFunctionOnAllThings(sequence, function):
    """
        This can be used to apply a function to all entities that
        exists.

        I.E all entities, containers, action

        function should be a function that expects 2 arguments:
        the full sequence, and the 'thing'

        Ex: 
        def myFunction(sequence, thing):
            if 'name' in thing:
                print(thing['name'])
    """
    applyFunctionOnAllItems(sequence, function)

    applyFunctionOnAllActions(sequence, function)


def addCommandFromThing(sequence, thing):
    """
        A callback to be used in applyFunctionOnAllThings
        so that all things with vim-commands add their commands to the
        global vim-command-list to be used later in vim

        vim is love, vim is life
    """
    if "vim" in thing:
        if "commands" in thing["vim"]:
            commands = thing["vim"]["commands"]
            for commandTarget in commands:
                if commandTarget == "content":
                    for commandType in commands[commandTarget]:
                        if commandType not in sequence["vim"]["commands"]:
                            sequence["vim"]["commands"][commandType] = []

                        commandTypeList = sequence["vim"]["commands"][commandType]

                        for coords in thing["contentCoordinateList"]:
                            commandTypeList.append((coords, commands[commandTarget][commandType]))
                            
                    #Must get coordinatelist from content. is already there :O                    
                else:
                    debug.fatalError(f"commands of category: {commandTarget} NOT SUPPORTED")


def initializeVimCommands(sequence):
    """
        build a global vim-field (if not exists) and fill with commands
        from all 'things'.

        Reason for this is to not have vim loop through all 'things'
        every time a command is done...
    """

    if "vim" not in sequence:
        sequence["vim"] = {}

    if "commands" not in sequence["vim"]:
        sequence["vim"]["commands"] = {} 

    applyFunctionOnAllThings(sequence, addCommandFromThing)


def initializeHeader(sequence):
    """
        Initialize values in the header of the sequence.

        The header is the part where entities resides.
        I.E entities and containers with entities within.
    """
    debug.debugPrint("initializeHeader BEGIN", "FUNCTION")
    sequence["header"] = {}
    
    sequence["header"]["size"] = [0, determineHeightsOfHeader(sequence["itemList"])]

    if "marginToFirstAction" not in sequence: #Is header-margin a better name?
        sequence["marginToFirstAction"] = 3

    if "marginAfterLastAction" not in sequence:
        sequence["marginAfterLastAction"] = 3

    debug.debugPrint("initializeHeader END", "FUNCTION")



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

    initializeHeader(sequence)

    initializeActions(sequence)

    initializeVim(sequence)

    resizeItemWidth(sequence)

    determineWidthOfSequence(sequence)

    determineRelativePositions(sequence)

    determineHeightOfSequence(sequence)

    #Must call this, to vimify the json-output... it sucks, but its sexy.
    getSequenceGraph(sequence)    

    #Now we have built: contentCoordinateList (for example) in setSequenceGraph...
    #Lets build the commands 
    initializeVimCommands(sequence)

    return sequence



