Images of biosim
================

While the visualization of the biosim project is rather simple it can still
give us a good overview of the simulation.

This analysis is made with the default parameters.

.. image:: /images_html/num_animals.png

The graph show the quantity of animals at given year, with herbivores being introduced at year 0
and carnivore at year 100. The herbivores' population explode at the beginning until it reaches a equilibrium
with the amount of fodder the island can provide. When the carnivores are introduced they start reducing the amount
of herbivores on the island until they reach a new equilibrium.

.. image:: /images_html/island.png

The island itself isn't too exiting, but the terrain distribution is
interesting when it comes to further analyzing the species's density.

.. image:: /images_html/herb_density.png

It is very apparent that the herbivore density follows terrain, with there being significantly more animals
on the rich lowland tiles, less on the more sparse highland tiles and only a few traveling animals
on the desert tiles.

.. image:: /images_html/carn_density.png

Unlike the herbivores the carnivores lives more spread out, but there is still signs
of overlap with the herbivores density.

.. image:: /images_html/age_dist.png

Almost no animal of either species reaches a age over 40, but the age distribution before this
cutoff point differs significantly between species. The carnivores suffers from quite intense child mortality,
with their age curve quite front loaded. Whereas the Herbivore dies at a more constant rate. If a carnivore reaches
the age of 10 it probably won't die before it comes close to 40.

.. image:: /images_html/fitness_dist.png

Again the distribution varies quite a lot between the animals. In the carnivores case we can see that quite a lot of
animals achieve excellent fitness, if we were to guess they would probably be the older and heavier animals. Where the
rest of them follows a rather standard bell curve.

The herbivores have a more random seeming distribution with a spike around the fitness value of 0.40 and a major
spike around 0.80. Quite a lot of the herbivores have fitness values ahead of the lower distribution of the carnivores
and would therefore only be potential prey for the apex predator with max fitness.

.. image:: /images_html/weight_dist.png

The weight distribution reinforce the already existing impression, that a lot of carnivores are unable to eat enough in
their youth and thus die off from hunger. The herbivore seems able to eat plenty though, with the majority having a
healthy weight around 27 kg, with their newborns showing up in the first spike.

While most carnivores are quite lightweight a few reaches massive sizes, being almost twice the weight of the
largest herbivores.

