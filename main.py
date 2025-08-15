import json

import argparse

import sys

import copy


def fatalError(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)

doDebuggingPrints = False

def debugPrint(msg):
    if doDebuggingPrints:
        print(f"DEBUG: {msg}")


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


def determineRelativePositionsHeader(sequence):
    """
        My god. How to do this best?
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


        heights are not really accounted for here yet...

        TODO: add relative offset to both x and y
        
    """

    startPos = [0,0]

    currentPos = startPos

    #Build the relative positions for each element in header (I.E entities)
    for item in sequence["itemList"]:
        if item["type"] == "entity":
            [width, height] = setEntityPos(item, currentPos)

            #Move along only x-axis the width of the entity
            currentPos[0] += width

        elif item["type"] == "container":
            [width, height] = setContainerPos(item, currentPos)
            currentPos[0] += width

        else:
            fatalError(f"Unknown type: {item['type']}")

            
    #Now header has been placed, place the timeLines for each entity
    addTimeLines(sequence)

    #Now place the actions
    currentActionRow = sequence["headerHeight"] + sequence["marginToFirstAction"] 

    for action in sequence["actionList"]:
        if action["type"] == "on":
            entity = getEntityWithId(sequence, action["entityId"])

            middleCol = entity["timeLineCol"] 

            startCol = middleCol - int(action["width"] / 2) 

            action["startPos"] = [startCol, currentActionRow]
            action["borderStartPos"] = [startCol, currentActionRow]

            action["endPos"] = [startCol + action["width"], currentActionRow + action["height"] - 1] 
            action["borderEndPos"] = [startCol + action["width"] - 1, \
                                      currentActionRow + action["height"] - 1 - action["margin"][2]] 

            action["contentStartPos"] = [startCol + action["padding"][3] + 1, currentActionRow + 1]
            action["contentEndPos"] = [startCol + action["padding"][3] + len(action["content"]), currentActionRow + 1]

            currentActionRow += action["height"]

        elif action["type"] == "communication":
            fromEntity = getEntityWithId(sequence, action["fromEntityId"])    
            toEntity = getEntityWithId(sequence, action["toEntityId"])    

            fromCol = fromEntity["timeLineCol"]
            toCol   = toEntity["timeLineCol"]

            if fromCol < toCol:
                middleCol = fromCol + int((toCol - fromCol - 1) / 2)

                action["arrowPos"] = [toCol - 1, currentActionRow + 1]
                action["arrowChar"] = ">"

                action["lineStartPos"] = [fromCol + 1, currentActionRow + 1]


                action["lineEndPos"] = [fromCol + action["width"] - 2, currentActionRow + 1]
                
            else:
                middleCol = toCol + int((fromCol - toCol - 1) / 2)

                action["arrowPos"] = [toCol + 1, currentActionRow + 1]
                action["arrowChar"] = "<"

                action["lineStartPos"] = [toCol + 2, currentActionRow + 1]
                action["lineEndPos"] = [toCol + action["width"] - 1, currentActionRow + 1]

            action["contentStartPos"] = [middleCol - int((len(action["content"]) - 1)/2), currentActionRow]
            action["contentEndPos"] = [middleCol + int(len(action["content"])/2), currentActionRow]

            currentActionRow += action["height"]


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

        graphStringListList.append("".join(graphStringList))

    return "\n".join(graphStringListList)


def displayGraph(sequence):
    """
        Print the graph to stdout
    """

    graphString = getSequenceGraph(sequence) 

    print(graphString)



GLOBAL_BORDER_CORNER     = "+"
GLOBAL_BORDER_VERTICAL   = "|"
GLOBAL_BORDER_HORIZONTAL = "-"


def getContentChar(item, x, y):
    if y <= item["contentStartPos"][1] and y >= item["contentEndPos"][1]:
        if x >= item["contentStartPos"][0] and x <= item["contentEndPos"][0]:
            debugPrint(f"{item['contentStartPos']} {item['contentEndPos']}")
            c = item["name"][x - item["contentStartPos"][0]]
            return [True, c]      

    return [False, False]


def getBorderChar(item, x, y):
        if y == item["borderStartPos"][1] and x == item["borderStartPos"][0]:
            return [True, GLOBAL_BORDER_CORNER]
        if y == item["borderEndPos"][1] and x == item["borderEndPos"][0]:
            return [True, GLOBAL_BORDER_CORNER]
        if y == item["borderEndPos"][1] and x == item["borderStartPos"][0]:
            return [True, GLOBAL_BORDER_CORNER]
        if y == item["borderStartPos"][1] and x == item["borderEndPos"][0]:
            return [True, GLOBAL_BORDER_CORNER]

        debugPrint(f"{item['startPos']} {item['endPos']} {x} {y}")

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


def getCharFromAction(action, x, y):
    """
        This should be extracted somehow...
    """

    if action["type"] == "on":
        if y <= action["contentStartPos"][1] and y >= action["contentEndPos"][1]:
            if x >= action["contentStartPos"][0] and x <= action["contentEndPos"][0]:
                debugPrint(f"{action['contentStartPos']} {action['contentEndPos']}")
                c = action["content"][x - action["contentStartPos"][0]]
                return [True, c]      

        #Border:
        r = getBorderChar(action, x, y)

        if r[0]:
            return r 

    elif action["type"] == "communication":
        if [x, y] == action["arrowPos"]:
            return [True, action["arrowChar"]]
        
        if y == action["lineStartPos"][1] and x >= action["lineStartPos"][0] and x <= action["lineEndPos"][0]:
            return [True, "-"]

        if y <= action["contentStartPos"][1] and y >= action["contentEndPos"][1]:
            if x >= action["contentStartPos"][0] and x <= action["contentEndPos"][0]:
                debugPrint(f"DEBUG: {action['contentStartPos']} {action['contentEndPos']}")
                c = action["content"][x - action["contentStartPos"][0]]
                return [True, c]      

    else:
        fatalError("no nothing but on-actions now...")
        return [False, False]

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

    for action in sequence["actionList"]:

        if action["type"] == "on":
            if "border" not in action:
                action["border"] = [1, 1, 1, 1]

            if "padding" not in action:
                action["padding"] = [0, 0, 0, 0]

            if "margin" not in action:
                #Per default only margin at bottom. 
                #Now, it will be the only margin that works in the beginning. Maybe ever.
                action["margin"] = [0, 0, 1, 0]

            width = len(action["content"]) + action["border"][3] + action["border"][1] + action["padding"][1] + action["padding"][3]
            #Now, content is only allowed to be 1 high :/
            contentHeight = 1

            height = contentHeight + action["border"][0] + action["border"][2] + action["padding"][0] + action["padding"][2] + action["margin"][0] + action["margin"][2]

            action["size"] = [width, height]

            action["width"] = width
        
            action["height"] = height


        elif action["type"] == "communication":
            action["width"] = len(action["content"]) + 2 

            if "margin" not in action:
                action["margin"] = [0,0,1,0]

            action["height"] = 2 + action["margin"][2]
            
            
        else:
            #TODO: variants
            fatalError("error mf, only 'on', and 'communication' supported now") 


def getEntityWithId(sequence, id):
    for i in sequence["entityList"]:
        if i["type"] == "entity":
            if i["id"] == id:
                return i

        else:
            fatalError("still only entities allowed")
    
    fatalError("entity with id {id} does not exist")


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
    """
    entitiesToCC = [firstEntity, secondEntity]

    cc = 0

    #Must always add the halfes:

    #Add the second half of A:
    toAdd = entitiesToCC[0]["margin"][1] + int(entitiesToCC[0]["widthNoMargin"] / 2)
    cc += toAdd 

    #Add the first half of B:
    toAdd = entitiesToCC[1]["margin"][3] + int((entitiesToCC[1]["widthNoMargin"] + 1) / 2)
    cc += toAdd

    if entitiesToCC[0]["parent"] == entitiesToCC[1]["parent"]:
        #Trivial case, both mf in the same container
        #Just add all the widths of all inbetweening siblings
        #Well. also if any inbetweeners has another parent, we must krångel a bit

        nextEntitySibling = entitiesToCC[0]["nextEntitySibling"]

        topParent = entitiesToCC[0]["parent"]

        containersCheckedList = []

        while nextEntitySibling != entitiesToCC[1]:

            if nextEntitySibling["parent"] != topParent:
                currentParent = nextEntitySibling["parent"]
                while currentParent["parent"] != topParent:
                    currentParent = currentParent["parent"]
                
                if currentParent not in containersCheckedList: 
                    cc += currentParent["width"]    
                    containersCheckedList.append(currentParent)
        
            else:
                cc += nextEntitySibling["width"]

            nextEntitySibling = nextEntitySibling["nextEntitySibling"]

    else:
        #This one is a bit more tricky.

        #1: First we must find the common ancestor of both entities.
        #Then, we add "inbetweeners" within that common ancestor... 
        #Example:
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

        # The same concept occurs for b, but the left side of parent(s)


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

    for action in sequence["actionList"]:
        if action["type"] == "communication":
            numEntitiesSpanned = getEntitiesSpanned(sequence, action) 
            action["numSpanned"] = numEntitiesSpanned
            communicationsList.append(action)

    communicationsList.sort(key=commSorter)
    return communicationsList 


def resizeEntityWidth(sequence):
    """
        Go through all actions and see if any entities needs to be resized.

        And if they do need to be resized, resize them :)
        Light weight.
    """

    #First. go with the on-actions
    #These will resize their respective entity
    for action in sequence["actionList"]:
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

            if cc < action["width"]:
                #Aigh then. We gonna need all involved mfs here.
                #Also a good chance I'm off by one (or two here)
                itemList = getItemsBetween(sequence, 
                                           action["fromEntityId"], 
                                           action["toEntityId"])

                distanceNeeded = action["width"] - cc 

                if distanceNeeded % 2 == 1:
                    #Ok. Need one more if uneven to get 1 margin in both directions on signal-content
                    distanceNeeded += 1

                #Ok. We can be really clever here, and sort of get the proportional increase per item,
                #or we can go with the easy route and just distribute them evenly.
                #easy route, I choose you
            
                distanceToAddEachItem = int(distanceNeeded / len(itemList))

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

    #Resize all communications now that items in header are resized
    #The header is always the one making the calls
    for action in sequence["actionList"]:
        if action["type"] == "communication":
            
            [firstEntity, secondEntity] = getFromAndToEntities(sequence, 
                                                               action["fromEntityId"], 
                                                               action["toEntityId"])

            cc = getEntityCC(sequence, firstEntity, secondEntity)    
    
            action["width"] = cc 


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
        item["nextSibling"]     = nextItem
        item["previousSibling"] = item


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

    sequence["height"] = totalHeight


def createContentList(sequence):
    """
        What does this do??

        It creates the vim interactive thing I think

    """

    commandList = []

    for i in sequence["itemList"]:
        if i["type"] == "entity":
            if "jumpCmd" in i:
                jump = {"cmd":i["jumpCmd"], "startCoord":i["contentStartPos"], "endCoord":i["contentEndPos"]}
                commandList.append(jump)

            pass

    for a in sequence["actionList"]:
        if a["type"] == "on":
            pass
        
        elif a["type"] == "communication":
            if "jumpCmd" in a:
                jump = {"cmd":a["jumpCmd"], "startCoord":a["contentStartPos"], "endCoord":a["contentEndPos"]}
                commandList.append(jump)
            

    sequence["cmdList"] = commandList


def generateSequence(configFile):
    """
        Generate the sequence.

        1. read in the config file
            1.1 Initialize entities
                1.1.1 determine the header height
            1.2 Set some meta data

        2. Determine the size of the actions in the sequence

        3. resize the width of headers if needed due to action-sizes

        4. Determine the total width of the sequence

        5. Give every element its position

        6. Determine the resulting height of the sequence
    """

    sequence = None

    with open(configFile) as inputfile:
        sequence = json.loads(inputfile.read())

        initializeEntities(sequence)

    sequence["headerHeight"] = determineHeightsOfHeader(sequence["itemList"]) 


    if "marginToFirstAction" not in sequence:
        sequence["marginToFirstAction"] = 3

    if "marginAfterLastAction" not in sequence:
        sequence["marginAfterLastAction"] = 3


    determineSizeOfActions(sequence)

    resizeEntityWidth(sequence)

    determineWidthOfSequence(sequence)

    determineRelativePositions(sequence)

    determineHeightOfSequence(sequence)

    createContentList(sequence)


    return sequence


def main():

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

    cliArgs = argParser.parse_args()

    if not cliArgs.file:
        #Per default use the test.json-file :)
        cliArgs.file = "test.json"

    sequence = generateSequence(cliArgs.file)


    if cliArgs.jsonOut:
        with open(cliArgs.jsonOut, "w") as jsonFile:
            jsonFile.write(json.dumps(sequence, indent=1))


    if cliArgs.display:
        displayGraph(sequence)

    if cliArgs.sequenceOut:
        with open(cliArgs.sequenceOut, "w") as sequenceFile:
            sequenceFile.write(getSequenceGraph(sequence))
            

if __name__ == "__main__":
    main()


