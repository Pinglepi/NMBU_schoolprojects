# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from biosim.simulation import BioSim
import textwrap

"""How would the animals react to a natural catastrophe? a neighbouring island has had an volcanic eruption resulting
in many years of volcanic winter. After the simulation a movie will be generated in the images folder"""
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
ini_herbs = [{'loc': (7, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(100)]}]
ini_carns = [{'loc': (7, 3),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 50}
                      for _ in range(25)]}]
sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
             seed=1234578,
             hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                         'age': {'max': 60.0, 'delta': 2},
                         'weight': {'max': 60, 'delta': 2}}, img_base='../images/', img_fmt='png'
             )

sim.simulate(20, 1)
sim.add_population(ini_carns)
sim.simulate(40, 1)
sim.simulate_eruption(10, 1)
sim.simulate(50, 1)
sim.simulate_eruption(15, 1)
sim.simulate(150, 1)
sim.make_movie()
