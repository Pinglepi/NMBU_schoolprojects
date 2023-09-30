# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.simulation import BioSim
import textwrap
"""This simulation tries to find out what would happen if we change the rate at which animals die, and how much they can
eat"""
geogr = """\
           WWWWWWWWWWWWWWWWWWWWW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHHHHHWWLLLLLLWWW
           WHHHHHLLLLLLLLLLLLWWW
           WHHHHHLLLDDLLLHLLLWWW
           WHHLLLLLDDDLLLHHHHWWW
           WWHHHHLLLDDLLLHWWWWWW
           WHHHLLLLLDDLLLLLLLWWW
           WHHHHLLLLDDLLLLWWWWWW
           WWHHHHLLLLLLLLWWWWWWW
           WWWHHHHLLLLLLLWWWWWWW
           WWWWWWWWWWWWWWWWWWWWW"""
geogr = textwrap.dedent(geogr)
ini_herbs = [{'loc': (5, 10),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]
ini_carns = [{'loc': (5, 10),
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


sim.set_animal_parameters('Herbivore', {'omega': 0.2, 'F': 50})
sim.set_animal_parameters('Carnivore', {'omega': 0.4, 'F': 100})
sim.simulate(150, 5)
sim.add_population(ini_carns)
sim.simulate(150, 5)
