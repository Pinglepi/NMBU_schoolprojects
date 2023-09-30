Class relations
===============

The way the classes relate to one another is quite simple.
You have a simulation, BioSim, consisting of an island, Island, that is grid of terrain, eg. Highland, that contain
animals, e.g Herbivore.

In addition you have a Graphics class that make sure all the graphics are displayed right.

+---------------------------------+
|Simulation                       |
+---------------------------------+
|Island                           |
+--------+---------+-------+------+
|Lowland |Highland |Desert |Water |
+--------+---------+-------+------+
|Herbivores        |Carnivores    |
+------------------+--------------+