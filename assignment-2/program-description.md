# Program description

The program consists of 2 auxiliary functions, a class definition, and the main program function.
The first auxiliary function's  signature is `parse(file)`. This function aims to extract variables and store them
in list data structures by parsing the input file using simple regular expressions. The function
returns a list of objects locations, vehicles, cargoes, goals in this order.

The second auxiliary function is used to calculate the distance between locations. Assuming that in
the problem the locations are linked circularly, we can calculate distance. There's always a way
to reach one location from others, so we always take the shortest. It’s also used as a helper function
to calculate the distance with an intermediary location.

The class we define _“mprime”_ when it’s instantiated is an object that represents the problem.
Here we deal with the variables and operations defined in the domain of the problem.

Finally, in the main program function, we write a procedure that follows a strategy.
To parse the code we use the module re-included in python. Basically what was done is to
create a data structure that represents the problem once the input file is parsed. Then, the methods:
move, load, unload, donate were hardcoded following the rules stated in the domain file. Hence
by using the data structures created, we can generate the plan applying the same rules and
preconditions. This way we don’t need to input the domain file. I intend to fully explain it, and
give further details on the presentation, which include a running demo.