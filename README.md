# genetic-pygame

Genetic algorithm applied to path finding.
The objective of the ships is to be as closer as possible from the red dot at the end of the allotted time.

The genome is composed of velocity vectors which will be applied to the ship successively during the allotted time.


Parameters:

speed_simulation : reduce allotted time and increase speed to simulate faster
iteration : number of iteration
duration : duration of one iteration in second
genome_size : size of the genome or number of node in the path
size_pop : size of the population
size_surviving_pop : size of the population after selection
