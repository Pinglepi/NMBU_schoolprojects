# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.simulation import BioSim
import textwrap
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
                         'weight': {'max': 60, 'delta': 2}}, img_base='../images/', img_fmt='png'
             )

sim.simulate(100, 5, 20)
sim.add_population(ini_carns)
input('Press enter to run more:')
#sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
sim.simulate(100, 5, 20)
