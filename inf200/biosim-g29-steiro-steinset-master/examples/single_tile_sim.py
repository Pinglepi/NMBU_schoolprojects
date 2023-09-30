# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.simulation import BioSim
import textwrap

"""See how the animals act on a single tile! to showcase the save function the simulation saves before the carnivores 
are spawned and loads back to that point, creating an alternative development without carnivores"""
geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 50}
                      for _ in range(40)]}]
sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
             seed=1234578,
             hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                         'age': {'max': 60.0, 'delta': 2},
                         'weight': {'max': 60, 'delta': 2}}
             )

sim.simulate(20, 5)
sim.save()
sim.add_population(ini_carns)
sim.simulate(80, 5)
sim.load()
sim.simulate(80, 5)
