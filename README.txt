
==== ASCII Archiitecture ====

Create sequence flows in ascii,
by using JSON-input


At least that's the main idea.
Also get some meta data to feed vim to later be able
to connect the sequence flow to code.


Also, this is stupid, but I've interchanged the usage of 
 line and y,
as well as 
 col and x.
Better to just use one. Which one doesn't matter but just pick one u retard.


===== Introduction =====


So, it would generate something like this:


+-----------+      +----------+
|  element  |      | element2 |
+-----------+      +----------+
      |                 |
      |    MESSAGE      |
      |---------------->|
      |                 |
      |                 |
                        

So how to do this?


We have a few sections we use as base.


First, the header:


+--------+    <-+
| entity |      |--- This is the height of the header
+--------+    <-+


Then, each element/entity has a width:


+--------+
| entity |
+--------+

^        ^
|        |
+--------+
    |
  This is the width of the element/entity


Then when we have those, its only a matter of placing the uckas.
In the header: place them in center of both measurments sort of.


Some general proposition:
every item has a box-layout with:

(0, 0)                                                                                    (X, 0)

startPos
    |
    v
    +-----------------------------------------------------------------+ <-----+
    |                             margin                              |       |
    |        +-----------------------------------------------+        |       |
    |        |                    border                     |        |       |
    |        |        +-----------------------------+        |        |       |
    |        |        |           padding           |        |        |       |
    |        |        |         +---------+         |        |        |       |
    | margin | border | padding | content | padding | border | margin |       |-- height (size[1])
    |        |        |         +---------+         |        |        |       |
    |        |        |           padding           |        |        |       |
    |        |        +-----------------------------+        |        |       |
    |        |                    border                     |        |       |
    |        +-----------------------------------------------+        |       |
    |                             margin                              |       |
    +-----------------------------------------------------------------+ <-----+
                                                                        \ 
    ^                                                                 ^ endPos
    |                                                                 |
    +-----------------------------------------------------------------+
                                |
                              width (size[0])

(0, Y)                                                                                     (X, Y)

Where:
margin, border, and padding 
all express the size/thickness, and are given by an array:
[top, left, bottom, right]

Moreover we have:
contentStartPos, contentEndPos, borderStartPos, borderEndPos, borderWidth


I think the margin will be a suggested value though,
since when we calculate stuff, it might change later...

I also think that borderWidth will never be used. 
It will look like absolute shit with thick borders.


========================================


Next up, timeLine:

+--------+
| entity |
+--------+
    |
    | <----- That is the timeLine
    |

The timeLine will be in the middle of the entities border-size.



=======================================

Now, actions:
An action might be a onEntity-thing (comment/info/event), 
it might be a communication between entities (signaling),
or it can be communication between outside and an entity (signaling from left or right)

An example of a onEntity-type action:

+--------+
| entity |
+--------+
    |
    |
+-------+
| EVENT |
+-------+
    |
    |


An example of a communication:


+--------+    +---------+     
| entity |    | entity2 |
+--------+    +---------+
    |              |
    |    SIGNAL    |
    |------------->|
    |              |


An example of a outsideCommunication:

+--------+
| entity |
+--------+
    |
    |    SIGNAL
    |<--------------
    |

outsideCommunication is not implemented


============================================

Hierarchies


You can add hierarchical entites, I.E containers.
An example might look like:


                                     +------------------------------------------------------+
                                     | DOMAIN2                                              |
+------------------------------+     |   +-------------+   +-----------------------------+  |
| DOMAIN1                      |     |   |  SUBDOMAIN1 |   | SUBDOMAIN2                  |  |
|   +---------+    +---------+ |     |   | +---------+ |   |  +---------+   +---------+  |  |
|   | entity1 |    | entity2 | |     |   | | entity3 | |   |  | entity4 |   | entity5 |  |  |
|   +---------+    +---------+ |     |   | +---------+ |   |  +---------+   +---------+  |  |
+--------|--------------|------+     |   +------|------+   +-------|-------------|-------+  |
         |              |            +----------|------------------|-------------|----------+
         |              |                       |                  |             | 


With an arbitrary number of nestings :)

=============================================

==== INPUT SYNTAX ====

Syntax is shown in BNF-format (or, at least as well as I can muster).
Note that '[' is the literal '[' while [ is the BNF defined 'optional'-symbol. 
Same with '{' and {

Input is a JSON-file with the following syntax 
(field order is not important, as long as it is valid JSON):

<sequenceConfig> ::= '{' <name>, <itemList>, <actionList>, [<options>] '}'

<name> ::= "name":"<string>"

<itemList> ::= "itemList": '[' <items> ']'

<items> ::= <item> | <item>, <items>

<item> ::= <entity> | <container>

<entity> ::= '{' <name>, "type":"entity", "id":<num> [<entityOptions>] '}'

<container> ::= '{' <name>, "type":"container", [<containerOptions>] '}'

<actionList> ::= "actionList": '[' <actions> ']'

<actions> ::= <action> | <action>, <actionList>

<action> ::= <on> | <communication>

<on> ::= '{' "type":"on", "content":"<string>", "entityId":<num>, [<onOptions>] '}'

<comunication> ::= '{' "type":"communication", "content":"<string>", "fromEntityId":<num>, "toEntityId":<num>, [<communcationOptions>] '}'

<options> ::= ["marginToFirstAction":<num>], ["marginFromLastAction":<num>] 

<entityOptions> ::= [<sizeOptions>]

<containerOptions> ::= [<sizeOptions>]

<onOptions> ::= [<sizeOptions>]

<communicationOptions> ::= NULL

<sizeOptions> ::= [<padding>], [<border>], [<margin>]

<padding> ::= "padding":<sizeArray>

<border> ::= "border":<sizeArray>

<margin> ::= "margin":<sizeArray>

<sizeArray> ::= '[' <top>, <right>, <bottom>, <left> ']'

<top> ::= <num>

<right> ::= <num>

<bottom> ::= <num>

<left> ::= <num>

<string> ::= [a-zA-Z0-9_-]*

<num> ::= [0-9]+


Note also that every json-object can contain whatever json-compliant fields 
that one wants, as long as they are not in presented grammar. I.E one can add:
"myField":3, and that will be ignored, but adding "type":"myType" to an item will
mess up the functionality.

Right... Also there will be some fields created during runtime,
so if any of the exists, they will be overwritten...
Example "entityList" will be created, so if that field exist,
it will be overwritten.


---- EXAMPLE -----
Now, generalized rules are good. 
An example is better:

{
	"name":"test", 
	"itemList":
	[ 
		{"type":"container", "name":"TOP", "padding":[0,1,0,1], 
		"itemList":[
			{"id": 0, "type":"entity", "name":"alice", "margin":[0,0,0,0]}
		]},

		{"id": 1, "type":"entity", "name":"bob", "margin":[0,0,0,5]},
		{"id": 2, "type":"entity", "name":"claire", "margin":[0,0,0,5]},

		{"type":"container", "name":"ANOTHER ONE", "margin":[0,0,0,3], "padding":[0,1,0,1], 
		 "itemList":[
			
			{"id": 3, "type":"entity", "name":"David", "margin":[0,0,0,0]},
			{"type":"container", "name":"DEEPER", "margin":[0,0,0,2], "padding":[0,1,0,1], "itemList":[
				{"type":"entity", "id":4, "name":"Erin"}

			]}
		]},

		{"id": 5, "type":"entity", "name":"fred", "padding":[0,1,0,1], "margin":[0,0,0,5]},
		{"id": 6, "type":"entity", "name":"gina", "margin":[0,0,0,5]},

		{"type":"container", "name":"LAST CONTAINER", "margin":[0,0,0,3], "padding":[0,2,0,2], 
		 "itemList":[
			
			{"id": 7, "type":"entity", "name":"hank", "margin":[0,0,0,0]},
			{"type":"container", "name":"LEVEL1", "margin":[0,2,0,2], "padding":[0,1,0,1], 
			 "itemList":[
				{"type":"entity", "id":8, "name":"iris"},
				{"type":"container", "name":"LEVEL2", "margin":[0,0,0,2], "padding":[0,1,0,1], 
				 "itemList":[
					{"id": 9, "type":"entity", "name":"jon", "margin":[0,2,0,0]},
					{"id": 10, "type":"entity", "name":"karen", "margin":[0,0,0,0]}
				]}

			]},
			{"id": 11, "type":"entity", "name":"lars", "margin":[0,0,0,0]}
		]}
   	], 

	"actionList":
	[
			{"type":"communication", "content": "MESSAGE", "fromEntityId": 11, "toEntityId": 7},
			{"type":"on", "content": "On something", "entityId":5}
	],
	"marginToFirstAction":2,
	"marginAfterLastAction":0
}

This will generate the following diagram:

+---------+     +---+     +------+   +---------------------+        +------+        +----+   +--------------------------------------------------+
| TOP     |     |bob|     |claire|   | ANOTHER ONE         |        | fred |        |gina|   |  LAST CONTAINER                                  |
| +-----+ |     +---+     +------+   | +-----+  +--------+ |        +------+        +----+   |  +----+  +----------------------------+  +----+  |
| |alice| |       |          |       | |David|  | DEEPER | |           |              |      |  |hank|  | LEVEL1                     |  |lars|  |
| +-----+ |       |          |       | +-----+  | +----+ | |           |              |      |  +----+  | +----+  +----------------+ |  +----+  |
+----|----+       |          |       |    |     | |Erin| | |           |              |      |    |     | |iris|  | LEVEL2         | |    |     |
     |            |          |       |    |     | +----+ | |           |              |      |    |     | +----+  | +---+  +-----+ | |    |     |
     |            |          |       |    |     +---|----+ |           |              |      |    |     |   |     | |jon|  |karen| | |    |     |
     |            |          |       +----|---------|------+           |              |      |    |     |   |     | +---+  +-----+ | |    |     |
     |            |          |            |         |                  |              |      |    |     |   |     +---|-------|----+ |    |     |
     |            |          |            |         |                  |              |      |    |     +---|---------|-------|------+    |     |
     |            |          |            |         |                  |              |      +----|---------|---------|-------|-----------|-----+
     |            |          |            |         |                  |              |           |         |         |       |           |      
     |            |          |            |         |                  |              |           |         |         |       |           |      
     |            |          |            |         |                  |              |           |         |     MESSAGE     |           |      
     |            |          |            |         |                  |              |           |<--------------------------------------|      
     |            |          |            |         |                  |              |           |         |         |       |           |      
     |            |          |            |         |           +------------+        |           |         |         |       |           |      
     |            |          |            |         |           |On something|        |           |         |         |       |           |      
     |            |          |            |         |           +------------+        |           |         |         |       |           |





===== TODO LIST =====

* Add variants
This is also a bit tricky. Again, the widths might need to be reavaluated sligthly(TM)

Something like this:

+--------+    +---------+     
| entity |    | entity2 |
+--------+    +---------+
    |              |
  +---------+--------+
  | VARIANT |      | |
  +---------+      | |
  | |              | |
  | |    SIGNAL    | |
  | |------------->| |
  | |              | |
  +------------------+
    |              |
    |              |

This might not be as tricky as I exected though.
Just readjust the margin between if needed and add +1 (or +2) to 
left/right sides of variant... Completly doable in my humble oppionion.
But then again, I am the greatest man alive. IMHO ofcourse.

This sort of works now on single entity...
And also margin and padding is not supported.



* Much friendlier help-page when doing --help
  Also a tourough[sic] explantion of how json should be structured.
  Both a generalized explanation and examples.


* syntax highlighting within vim
This should be trivial... glhf


*Sender received for communications. 
 To jump to send-point and receive point with graphical ting

   |            |
  +-+          +-+
  |S| -------> |R|
  +-+          +-+
   |            |

=========================================
Developing

TODO: some architecture notes. I.E how do things work, how is structure etc...

-----------------------------------------
Testing.
See README.txt in test/ directory

=========================================

Future

Create more ASCII stuff.

flow-charts

trees (for file structures and such)

Mind Map

deployment

tables

graphs (function-curves)

thread-graph ("per core to the right diagram" :) )

All with the ability to interact with vim later on.
Should rewrite it in lua in the future then...
Maybe in another life...


========================================
Author: 
	Fredrik Easterdale
Contact me: 
	fredrik.ostdahl@gmail.com
