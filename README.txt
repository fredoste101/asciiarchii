
ASCII Archiitecture

Create sequence flows in ascii,
by using JSON-input


At least that's the main idea.
Also get some meta data to feed vim to later be able
to connect the sequence flow to code.


Also, this is stupid, but I've interchanged the usage of line and y,
as well as col and x.
Better to just use one. Which one doesn't matter but just pick one u retard.


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


TODO LIST

*Gitify it. Make it a repo. Keep track of changes. Make it real. Feel it. Hear it. Love it.


*Add unit tests. Its getting to big to not have tests to verify that I don't break shit for myself...


* Add variants as discussed above
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


* syntax highlighting within vim
This should be trivial

* Much friendlier help-page when doing --help



*Sender received for communications. To jump to send-point and receive point with graphical ting

   |            |
  +-+          +-+
  |S| -------> |R|
  +-+          +-+
   |            |

=========================================

Future

Create more ASCII stuff.
Mind Map

deployment

tables

flow-charts

All with the ability to interact with vim later on.
Should rewrite it in lua in the future then...
Maybe in another life...
