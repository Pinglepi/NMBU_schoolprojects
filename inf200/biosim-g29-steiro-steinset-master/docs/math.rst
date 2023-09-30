Animals math
========================

The Biosim project runs quite a bit of math to calculate the behaviour of the animals. Understanding this math is not
critical to run the simulation, but gives a much deeper insight into how it works.

The core of the simulation is located in the parameter values within the herbivore and carnivore class. Where they are
stored within a dictionary.

The default parameters are as follows:

+--------------+------------+------------+
|Param         |Herbivore   |Carnivore   |
+--------------+------------+------------+
|w_birth       |8.0         |6.0         |
+--------------+------------+------------+
|sigma_birth   |1.5         |1.0         |
+--------------+------------+------------+
|beta          |0.9         |0.75        |
+--------------+------------+------------+
|eta           |0.05        |0.125       |
+--------------+------------+------------+
|a_half        |40.0        |40.0        |
+--------------+------------+------------+
|phi_age       |0.6         |0.3         |
+--------------+------------+------------+
|w_half        |10.0        |4.0         |
+--------------+------------+------------+
|phi_weight    |0.1         |0.4         |
+--------------+------------+------------+
|mu            |0.25        |0.4         |
+--------------+------------+------------+
|gamma         |0.2         |0.8         |
+--------------+------------+------------+
|zeta          |3.5         |3.5         |
+--------------+------------+------------+
|xi            |1.2         |1.1         |
+--------------+------------+------------+
|omega         |0.4         |0.8         |
+--------------+------------+------------+
|F             |10.0        |50.0        |
+--------------+------------+------------+
|DeltaPhiMax   |            |10.0        |
+--------------+------------+------------+

These parameters are quite suitable to be changed, and that change the dynamics of the entire simulation!

In addition the following attributes of the animals are used in the calculations.

+-------+----+-------------+------------------------------------------+
|Weight |Age | Phi(fitness)| N(number of animals on the same terrain) |
+-------+----+-------------+------------------------------------------+

In cases where a herbivore and carnivore compares, the specifier for species is added after an underscore.

Fitness
-------
:math:`phi = \frac{1}{1+e^{phi\_(age*age-age\_half)}}+\frac{1}{1+e^{-phi\_weight*(weight-weight\_half)}}`

Probably the most common calculation in the entire simulation, will give a value between 0 and 1 and is critical in
functions relating to breeding, eating and migrating. If the animal have a weight of 0(or less) it will set a fitness
0



Carnivore eating patterns
-------------------------

+----------------------------------------------------+----------------------------------------------+
| Probability                                        |          if                                  |
+----------------------------------------------------+----------------------------------------------+
|:math:`0`                                           |:math:`phi\_carn   \leq phi\_herb`            |
+----------------------------------------------------+----------------------------------------------+
|:math:`\frac{phi\_carn-phi\_herb}{delta\_phi\_max}` |:math:`0<phi\_carn-phi\_herb<delta\_phi\_max` |
+----------------------------------------------------+----------------------------------------------+
|:math:`1`                                           |          otherwise                           |
+----------------------------------------------------+----------------------------------------------+

Gives a probability that a carnivore will it the carnivore it compare itself to.

Birth_weight
------------
birth\_weight ~ N(w\_birth, sigma\_birth)

Gaussian distribution with mean w\_birth and standard deviation of sigma\_birth

Giving Birth
------------
+----------------------------------------------------+----------------------------------------------+
| Probability                                        |          if                                  |
+----------------------------------------------------+----------------------------------------------+
|:math:`0`                                           |:math:`N<2`                                   |
+----------------------------------------------------+----------------------------------------------+
|:math:`0`                                           |:math:`weight < zeta(w\_birth+sigma\_birth)`  |
+----------------------------------------------------+----------------------------------------------+
|:math:`gamma*phi*(N-1)`                             |:math:`gamma*phi*(N-1)` <= :math:`1`          |
+----------------------------------------------------+----------------------------------------------+
|:math:`1`                                           |:math:`gamma*phi*(N-1)` > :math:`1`           |
+----------------------------------------------------+----------------------------------------------+

Gives the probability that the animal will give birth

Loss of weight
--------------

removes :math:`eta*weight` from current weight

Gaining weight
--------------

adds :math:`food\_eaten*beta` to current weight


Dying
-----
+----------------------------------------------------+----------------------------------------------+
| Probability                                        |          if                                  |
+----------------------------------------------------+----------------------------------------------+
|:math:`1`                                           |:math:`weight \geq 0`                         |
+----------------------------------------------------+----------------------------------------------+
|:math:`omega*(1-phi)`                               |otherwise                                     |
+----------------------------------------------------+----------------------------------------------+

The probability that an animal should die

Migration
---------
Probability of :math:`mu*phi` for the animal too move
