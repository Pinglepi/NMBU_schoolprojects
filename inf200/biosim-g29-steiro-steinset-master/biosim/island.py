# -*- coding: utf-8 -*-

__author__ = 'August N Steinset and Sunniva E Daae Steiro'
__email__ = 'augustei@nmbu.no and sunnivas@nmbu.no'

from .terrain import Lowland, Highland, Desert, Water
import random


class Island:
    """
    Implements an island consisting of a certain amount of tiles of different characteristics
    that are set through the Terrain class. This class calls upon all animals on the island to
    do different activities.
    """

    num_herbivores = 0

    def __init__(self, island_text, seed, ini_pop=None):
        """ Create an island

        :param island_text: a string containing lines with the same amount of characters indicating
            terrain type of each tile on the entire island.
        :param seed: sets seed for random functions
        :param ini_pop: list of animals that should be set out on the island when initiated.
            The default is set to None so that an island can be initiated without animals.
        """
        self.island_text = island_text.split()
        self.island = []

        for i, v in enumerate(self.island_text):
            self.island.append([])
            for j in v:
                if j == "L":
                    self.island[i].append(Lowland())
                elif j == "W":
                    self.island[i].append(Water())
                elif j == "H":
                    self.island[i].append(Highland())
                elif j == "D":
                    self.island[i].append(Desert())
                else:
                    raise ValueError("Terrain type undefined")

        # Tests that map lines are consistent
        for i in range(len(self.island) - 1):
            if len(self.island[i]) != len(self.island[i + 1]):
                raise ValueError('All lines of the map must be of same length.')

        self.check_valid_boundaries()

        random.seed(seed)
        if ini_pop:
            for i in ini_pop:
                self.island[i['loc'][0] - 1][i['loc'][1] - 1].spawn_animal(i['pop'])

    def check_valid_boundaries(self):
        """Checks that all boarders of the given map are only water, raises valueError if not."""
        if self.island_text[0] != len(self.island_text[0]) * 'W' or self.island_text[-1] != len(
                self.island_text[0]) * 'W':
            raise ValueError('Boarders must be water')
        for k in range(len(self.island_text)):
            if self.island_text[k][0] != 'W' or self.island_text[k][-1] != 'W':
                raise ValueError('Boarders must be water')

    @staticmethod
    def set_params(landscape, params):
        """
        Updates max value of fodder on lowland, highland and desert
        :param landscape: string of one letter, either H, L or D.
        :param params: dictionary on form {'f_max': value}, where value is an integer
        representing amount of fodder
        """
        if landscape not in ['H', 'L', 'D']:
            raise ValueError('Landscape must be L, D or H.')
        elif landscape == 'L':
            Lowland().set_params(params)
        elif landscape == 'H':
            Highland().set_params(params)
        elif landscape == 'D':
            Desert().set_params(params)

    @staticmethod
    def change_parameter(species, p_dict):
        """
        Updates parameter values for a species. Raises error if species input is incorrect.
        :param species: string, either 'Herbivore' or 'Carnivore'
        :param p_dict: dictionary on form {'zeta': 3.2, 'xi': 1.8}, with parameter
        name as key, and value as new parameter value
        """
        terrain = Lowland()
        terrain.spawn_animal([{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}, {'species': 'Carnivore',
                                               'age': 5,
                                               'weight': 20}])
        if species == 'Herbivore':
            terrain.herbivores_on_tile[0].set_animal_parameters(p_dict)
        elif species == 'Carnivore':
            terrain.carnivores_on_tile[0].set_animal_parameters(p_dict)
        else:
            raise ValueError("Tried to set parameter for a species that does not exist")

    def spawn_animal(self, ini_pop):
        """Places new animals on the island.

        :param ini_pop: dictionary of animals
        """
        for i in ini_pop:
            self.island[i['loc'][0] - 1][i['loc'][1] - 1].spawn_animal(i['pop'])

    def all_eat(self):
        """Make all the animals eat"""
        for i, a in enumerate(self.island):
            for j in range(len(a)):
                self.island[i][j].eat_on_tile()

    def all_carnivores_eat(self):
        """Make all the carnivore on the island eat"""
        for i, a in enumerate(self.island):
            for j in range(len(a)):
                self.island[i][j].carn_eat_on_tile()

    def all_lose_weight(self):
        """ Make all the animals lose weight """
        for i, a in enumerate(self.island):
            for j in range(len(a)):
                self.island[i][j].lose_weight_on_tile()

    def all_age(self):
        """ Make all animals on the island age by one year"""
        for i, a in enumerate(self.island):
            for j in range(len(a)):
                self.island[i][j].age_on_tile()

    def all_die(self):
        """ Check if animals should be killed, and then kills them """
        for i, a in enumerate(self.island):
            for j in range(len(a)):
                self.island[i][j].die_on_tile()

    def all_breed(self):
        """Make all the animals procreate. Iterates through all the tiles of the island"""
        for i, a in enumerate(self.island):
            for j in range(len(a)):
                self.island[i][j].breed_on_tile()

    def all_migrate_herb(self):
        """Make the herbivores migrate"""
        migrated_herb = []
        for i, a in enumerate(self.island):
            temp_herb = []
            for j in range(len(a)):
                if i != 0 and j != 0 and i != len(self.island) - 1 and j != len(a) - 1:
                    legal_moves = [self.island[i - 1][j].movable, self.island[i + 1][j].movable,
                                   self.island[i][j + 1].movable, self.island[i][j - 1].movable]
                    temp_herb.append(self.island[i][j].migration_herb(legal_moves))

                else:
                    temp_herb.append([[], [], [], []])
            migrated_herb.append(temp_herb)
        for i, a in enumerate(migrated_herb):
            for j, b in enumerate(a):
                if i != 0 and j != 0 and i != len(self.island) - 1 and j != len(a) - 1:
                    self.island[i - 1][j].herbivores_on_tile.extend(b[0])
                    self.island[i + 1][j].herbivores_on_tile.extend(b[1])
                    self.island[i][j + 1].herbivores_on_tile.extend(b[2])
                    self.island[i][j - 1].herbivores_on_tile.extend(b[3])

    def all_migrate_carn(self):
        """Make the carnivores migrate"""
        migrated_carn = []
        for i, a in enumerate(self.island):
            temp_carn = []
            for j in range(len(a)):
                if i != 0 and j != 0 and i != len(self.island) - 1 and j != len(a) - 1:
                    legal_moves = [self.island[i - 1][j].movable, self.island[i + 1][j].movable,
                                   self.island[i][j + 1].movable, self.island[i][j - 1].movable]
                    temp_carn.append(self.island[i][j].migration_carn(legal_moves))

                else:
                    temp_carn.append([[], [], [], []])
            migrated_carn.append(temp_carn)
        for i, a in enumerate(migrated_carn):
            for j, b in enumerate(a):
                if i != 0 and j != 0 and i != len(self.island) - 1 and j != len(a) - 1:
                    self.island[i - 1][j].carnivores_on_tile.extend(b[0])
                    self.island[i + 1][j].carnivores_on_tile.extend(b[1])
                    self.island[i][j + 1].carnivores_on_tile.extend(b[2])
                    self.island[i][j - 1].carnivores_on_tile.extend(b[3])

    def all_migrate(self):
        """Make animals of both species migrate"""
        self.all_migrate_carn()
        self.all_migrate_herb()

    def get_maps(self):
        """Gathers up all the valuable information of the island

        returns: Herbivore density, Carnivore density, age of all animals,
        fitness of all animals, weight of all animals, number of herbivores
        on island and number of carnivores on island
        """
        herbivores_map = []
        carnivores_map = []
        age_list = [[], []]
        fitness_list = [[], []]
        weight_list = [[], []]
        num_herb = 0
        num_carn = 0
        for i, a in enumerate(self.island):
            herbivores_map.append([])
            carnivores_map.append([])
            for j in range(len(a)):
                temp_herb = self.island[i][j].count_herbivores()
                temp_carn = self.island[i][j].count_carnivores()
                num_herb += temp_herb
                num_carn += temp_carn
                herbivores_map[i].append(temp_herb)
                carnivores_map[i].append(temp_carn)
                age_list[0].extend(self.island[i][j].get_values_herb()[0])
                fitness_list[0].extend(self.island[i][j].get_values_herb()[1])
                weight_list[0].extend(self.island[i][j].get_values_herb()[2])
                age_list[1].extend(self.island[i][j].get_values_carn()[0])
                fitness_list[1].extend(self.island[i][j].get_values_carn()[1])
                weight_list[1].extend(self.island[i][j].get_values_carn()[2])
        return [herbivores_map, carnivores_map, age_list,
                fitness_list, weight_list, num_herb, num_carn]
