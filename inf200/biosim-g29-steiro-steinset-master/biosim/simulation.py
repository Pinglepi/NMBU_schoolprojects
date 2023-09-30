# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from .island import Island
from .graphics import Graphics
import pickle
import ast


class BioSim:
    """
    A simulation class
    """

    def __init__(self, island_map, ini_pop, seed, hist_specs=None, img_base=None,
                 img_fmt=None, ymax_animals=None, cmax_animals=None):
        """Creates a simulation

        :param island_map: A string containing the structure of the island.
        :param ini_pop: A list of dictionaries containing information on where to spawn animals and their attributes.
         on the form [{loc: (x,y}, pop: [{species: 'species', age: age, weight: weight}]}]
        :param seed: An integer that decides how random numbers are generated in the simulation.
        :param hist_specs: Dictionary with the dimensions of the histograms. on the form {attribute: {max, delta}}
        :param img_base: Where the simulation should store images.
        :param img_fmt: Format of the saved images.
        :param ymax_animals: Fixes a y value for the animal count visualization.
        :param cmax_animals: Fixes the values of the color gradient of the visualization.
        """
        self.island = Island(island_map, seed, ini_pop)
        self.maps = self.island.get_maps()
        self._year = 0
        self._num_animals_per_species = {'Herbivore': self.maps[5], 'Carnivore': self.maps[6]}
        self._num_animals = self.maps[5] + self.maps[6]
        self._animal_count_history = {0: [self.maps[5], self.maps[6]]}
        self.graphics = Graphics(island_map, herb_map=self.maps[0], carn_map=self.maps[1], age_map=self.maps[2],
                                 fitness_map=self.maps[3], weight_map=self.maps[4], hist_specs=hist_specs,
                                 animal_count_history=self._animal_count_history,
                                 img_base=img_base, img_fmt=img_fmt, cmax_animals=cmax_animals,
                                 ymax_animals=ymax_animals)

    def save(self):
        """Saves the current simulation in three different files in the saves folder"""
        with open('../saves/save.dat', 'wb') as f:
            pickle.dump(self.island, f, pickle.HIGHEST_PROTOCOL)
        with open('../saves/save.txt', 'w') as f:
            text = "{}\n"
            f.write((text.format(self._animal_count_history)))
        with open('../saves/save_year.txt', 'w') as f:
            f.write(str(self.year))

    def load(self):
        """Loads save information from the saves folder"""
        with open('../saves/save.dat', 'rb') as f:
            self.island = pickle.load(f)
        with open('../saves/save.txt', 'r') as f:
            self._animal_count_history = ast.literal_eval(f.read())
        with open('../saves/save_year.txt', 'r') as f:
            self._year = ast.literal_eval(f.read())

    def set_animal_parameters(self, species, p_dict):
        """
        Sets animal parameters to new values for a whole species.

        :param species: str, either 'Carnivore' or 'Herbivore'
        :param p_dict: dictionary on form {'zeta': value}, where value is the new parameter value
        """
        self.island.change_parameter(species, p_dict)

    def set_landscape_parameters(self, landscape, params):
        """
        Sets new landscape parameter to new value for one type of landscape.

        :param landscape: str, either L or H for Lowland and Highland
        :param params: dictionary on form {'f_max': value}, where value is the new parameter value
        """
        self.island.set_params(landscape, params)

    def add_population(self, population):
        """
        Adds a population of animals to a chosen tile on the island.

        :param population: list containing dictionaries of animals with location,
         weight, age and species.
        """
        self.island.spawn_animal(population)

    def make_movie(self):
        """Create a MPEG4 movie from visualization images saved"""
        self.graphics.make_movie()

    @property
    def year(self):
        """Last year simulated"""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island"""
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island"""
        return self._num_animals_per_species

    def simulate(self, num_years, vis_years=1, img_years=None):
        """Simulates life on the island

        :param num_years: Number of years simulated.
        :param vis_years:  Number of years between each visualization update.
        :param img_years: number of years between each time an image is saved.
        """
        if not img_years:
            img_years = vis_years
        for i in range(num_years):
            self.island.all_eat()
            self.island.all_breed()
            self.island.all_migrate()
            self.island.all_age()
            self.island.all_lose_weight()
            self.island.all_die()
            self._year += 1
            maps = self.island.get_maps()
            self._num_animals_per_species['Herbivore'] = maps[5]
            self._num_animals_per_species['Carnivore'] = maps[6]
            self._num_animals = self.num_animals_per_species['Herbivore'] + self.num_animals_per_species['Carnivore']
            self._animal_count_history[self.year] = [maps[5], maps[6]]
            self.graphics.update_graphics(self.year, herb_map=maps[0], carn_map=maps[1], age_map=maps[2],
                                          fitness_map=maps[3], weight_map=maps[4],
                                          animal_count_history=self._animal_count_history, vis_years=vis_years,
                                          img_years=img_years)

    def simulate_eruption(self, num_years, vis_years=1, img_years=None):
        """Simulates life on the island without access to new food for the herbivores

        :param num_years: Number of years simulated.
        :param vis_years:  Number of years between each visualization update.
        :param img_years: number of years between each time an image is saved.
        """
        if not img_years:
            img_years = vis_years
        for i in range(num_years):
            self.island.all_carnivores_eat()
            self.island.all_breed()
            self.island.all_migrate()
            self.island.all_age()
            self.island.all_lose_weight()
            self.island.all_die()
            self._year += 1
            maps = self.island.get_maps()
            self._num_animals_per_species['Herbivore'] = maps[5]
            self._num_animals_per_species['Carnivore'] = maps[6]
            self._num_animals = self.num_animals_per_species['Herbivore'] + self.num_animals_per_species['Carnivore']
            self._animal_count_history[self.year] = [maps[5], maps[6]]
            self.graphics.update_graphics(self.year, herb_map=maps[0], carn_map=maps[1], age_map=maps[2],
                                          fitness_map=maps[3], weight_map=maps[4],
                                          animal_count_history=self._animal_count_history, vis_years=vis_years,
                                          img_years=img_years)
