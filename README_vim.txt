=== VIM ===

How do we link the sequence to vim?
By using special json-attributes (or yaml ones), 
we can create:

colors when opening the sequence in vim, (NB! Coloring is turned off, since it slows down everything 2 much)

and

create (custom) commands to be run at certain conditions.


This section needs mopped. 

Yeah, well I need to explain the commands at least.
It might not be super intuitive for someone else I suppose.
To be hones its not intuitive to me either... but its pretty nice.


--- Navigation ---

Now we can navigatate with hjkl to distinct places,
not perfectly yet, but we can traverse the items and actions
in the sequence, in sequence :O

This also allows us to have the Enter key be the primary execute-action
button, instead of previously <leader><something>...
This limits us to 1 action per item,
however, we should still be able to have more actions as previosly.

For example if we stand on specific action,
we could either press enter to get the default command run,
or if exists, press <leader><something> to get some other command. 



--- interactivity ---

By pressing Shift-i (I.E captial i),
we go inteo interactive mode.

This means we have 3 windows:
1. main window where the sequence is
2. header window to not lose track of which entity does what,
   as we traverse down in the sequence
3. target window, where the command on each entity/action will
   happen. This means, opening whatever file associated with action/entity,
   as we enter that one in the sequence.

+--------+---------+
|        |  header |
|        +---------+
| target |         |
|        |   main  |
|        |         | 
+--------+---------+

This is pretty nice,
allowing us to move around in the sequence,
and get live updates on the code which corresponds
to a certain location in the sequence.


