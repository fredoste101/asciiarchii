

=== ASCII Archiitecture ===

Create sequence flows in ascii,
by using JSON-input


At least that's the main idea.
Also get some meta data to feed vim to later be able
to connect the sequence flow to code.

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
or
it might be a communication between entities (signaling/message passing/function calling)

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



=== Hierarchies ===


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


=== VARIANTS ===

A variant is basically a label around a certain section in the sequence.
A variant can contain many branches, mimicing different conditions
leading to different actions in the sequence.

A branch in a variant can contain both on and communication actions,
and we can of course have variants within a branch, to do nesting conditions (has this been confirmed?).


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

An example of a variant with 2 branches:

+-----+    +---+    +------+
|alice|    |bob|    |claire|
+-----+    +---+    +------+
   |         |         |    
   |         |         |    
  +----+----------------+   
  |frwd|     |         ||   
  +----+     |         ||   
  || message |         ||   
  ||-------->|         ||   
  ||         |         ||   
  +---------------------+   
  |rvrs|     |         ||   
  +----+     |         ||   
  ||  hello  |         ||   
  ||<--------|         ||   
  ||         |         ||   
  ||         |  world  ||   
  ||         |-------->||   
  ||         |         ||   
  +---------------------+   
   |         |         |    
   |         |         |    

=============================================

=== INPUT SYNTAX ===
See the file inputSyntax.txt in the same directory as this :)


=== TODO LIST ===
Things that I want to do to increase functionality


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

 Should be relativaly straight forward. If on and communication works properly,
 this is just both combined :)

*starting/activation of entity like:

+---+     +---+
| A |     | B |
+---+     +---+
  |
  |  START
  |-------->+
  |         |
  |         |

* outsideCommunication
An example of a outsideCommunication:

+--------+
| entity |
+--------+
    |
    |    SIGNAL
    |<--------------
    |

* onMany - a on type action but covering many entities


* I don't think style works at all with variants.
  It would be nice with margins/padding on variants, to make it a lot nicer looking.
  It tends to become very squished together now when we nestle a lot of them


* yes, well. I don't like stupid things. 
  Remove width and height and replace them with size => [width, height]
  Also, this is stupid, but I've interchanged the usage of 
   line and y,
  as well as 
   col and x.
  Better to just use one. Which one doesn't matter but just pick one u retard.
  

=== Developing ===

Aight, so I like code that is spaced far apart. So what? sue me.
Thus there are a lot of extra spaces, newlines and stuff, where others might not use it.
Also I like to align stuff in columns as well. So what? sue me again. C if I care.


TODO: some architecture notes. I.E how do things work, how is structure etc...

-----------------------------------------


=== Testing ===

See README.txt in test/ directory


=== Future ===

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
